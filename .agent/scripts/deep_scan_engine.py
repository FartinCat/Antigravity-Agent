import os
import json
import re

def get_project_tree(root, excludes):
    tree = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter directories
        dirnames[:] = [d for d in dirnames if d not in excludes]
        rel_path = os.path.relpath(dirpath, root)
        if rel_path == '.':
            rel_path = ''
        for f in filenames:
            tree.append(os.path.join(rel_path, f))
    return tree

def check_registry_drift(root):
    install_state_path = os.path.join(root, '.agent', 'aether-agent-install-state.json')
    if not os.path.exists(install_state_path):
        return "MISSING install-state.json"
    
    with open(install_state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    rules_dir = os.path.join(root, '.agent', 'rules')
    skills_dir = os.path.join(root, '.agent', 'skills')
    workflows_dir = os.path.join(root, '.agent', 'workflows')
    agent_skills_dir = os.path.join(root, '.agent', '.agents', 'skills')
    
    rules_on_disk = len([f for f in os.listdir(rules_dir) if f.endswith('.md')])
    skills_on_disk = len([f for f in os.listdir(skills_dir) if f.endswith('.md')])
    workflows_on_disk = len([f for f in os.listdir(workflows_dir) if f.endswith('.md')])
    agent_skills_on_disk = len([d for d in os.listdir(agent_skills_dir) if os.path.isdir(os.path.join(agent_skills_dir, d))])
    
    report = []
    if rules_on_disk != len(state.get('installed_rules', [])):
        report.append(f"rules: {rules_on_disk} on disk, {len(state.get('installed_rules', []))} in registry")
    if skills_on_disk != len(state.get('installed_foundational_skills', [])):
        report.append(f"foundational_skills: {skills_on_disk} on disk, {len(state.get('installed_foundational_skills', []))} in registry")
    if workflows_on_disk != len(state.get('installed_workflows', [])):
        report.append(f"workflows: {workflows_on_disk} on disk, {len(state.get('installed_workflows', []))} in registry")
    if agent_skills_on_disk != len(state.get('installed_skills', [])):
        report.append(f"agent_skills: {agent_skills_on_disk} on disk, {len(state.get('installed_skills', []))} in registry")
    
    return report if report else "IN SYNC"

def check_numbering_collisions(root, path):
    full_path = os.path.join(root, path)
    if not os.path.exists(full_path):
        return f"{path} not found"
    
    items = os.listdir(full_path)
    prefixes = {}
    for item in items:
        match = re.match(r'^(\d+)', item)
        if match:
            prefix = match.group(1)
            if prefix in prefixes:
                prefixes[prefix].append(item)
            else:
                prefixes[prefix] = [item]
    
    collisions = []
    for prefix, files in prefixes.items():
        if len(files) > 1:
            collisions.append(f"{path}: prefix {prefix} shared by {', '.join(files)}")
            
    # Check for gaps
    if prefixes:
        sorted_prefixes = sorted([int(p) for p in prefixes.keys()])
        expected = range(min(sorted_prefixes), max(sorted_prefixes) + 1)
        gaps = [f"{i:02d}" for i in expected if i not in sorted_prefixes]
        if gaps:
            collisions.append(f"{path}: positions {', '.join(gaps)} are missing")
            
    return collisions

def check_root_pollution(root):
    pollution_patterns = [
        r'.*EVALUATION.*\.md',
        r'.*MASTER_PLAN.*\.md',
        r'.*SCAN_REPORT.*\.md',
        r'.*RESEARCH_.*\.md',
        r'.*AUDIT_REPORT.*\.md',
        r'WEEKLY_REVIEW_.*\.md'
    ]
    excludes = ['README.md', 'CLAUDE.md', 'AETHER.md', 'LICENSE.md']
    pollution = []
    for f in os.listdir(root):
        if os.path.isfile(os.path.join(root, f)) and f not in excludes:
            for pattern in pollution_patterns:
                if re.match(pattern, f, re.IGNORECASE):
                    pollution.append(f)
                    break
    return pollution

def check_encoding(root):
    bom_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        if '.git' in dirnames: dirnames.remove('.git')
        for f in filenames:
            if f.endswith('.md') or f.endswith('.json'):
                path = os.path.join(dirpath, f)
                try:
                    with open(path, 'rb') as bf:
                        content = bf.read()
                        if b'\x07' in content:
                            bom_files.append(os.path.relpath(path, root))
                except:
                    pass
    return bom_files

def check_version_consistency(root):
    aether_path = os.path.join(root, 'AETHER.md')
    if not os.path.exists(aether_path):
        return "AETHER.md MISSING"
    
    with open(aether_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Title version
    title_match = re.search(r'^# Aether Agent v([\d\.]+)', content, re.M)
    title_version = title_match.group(1) if title_match else None
    
    # Identity table version
    table_match = re.search(r'\| \*\*Version\*\* \| ([\d\.]+) \|', content)
    table_version = table_match.group(1) if table_match else None
    
    # Metadata version
    meta_match = re.search(r'\*\*Version\*\*: ([\d\.]+)', content)
    meta_version = meta_match.group(1) if meta_match else None
    
    versions = {
        'title': title_version,
        'table': table_version,
        'metadata': meta_version
    }
    
    if len(set(v for v in versions.values() if v is not None)) > 1:
        return versions
    return "IN SYNC"

def main():
    # Attempt to import detect_root from the same directory, or fallback to current working directory
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from detect_root import detect_root
        root = str(detect_root(interactive=False))
    except Exception:
        root = os.getcwd()
    
    excludes = ['.agent', '.git', 'node_modules', '__pycache__', 'target', '.venv', '.claude']
    
    tree = get_project_tree(root, excludes)
    
    print("--- SCAN RESULTS ---")
    print(f"Project Tree: {len(tree)} files")
    
    stack = []
    if os.path.exists(os.path.join(root, 'package.json')): stack.append("Node.js")
    if os.path.exists(os.path.join(root, 'requirements.txt')): stack.append("Python")
    if os.path.exists(os.path.join(root, 'Cargo.toml')): stack.append("Rust")
    print(f"Tech Stack: {', '.join(stack) if stack else 'Unknown'}")
    
    registry = check_registry_drift(root)
    print(f"Registry Drift: {registry}")
    
    collisions = []
    collisions.extend(check_numbering_collisions(root, '.agent/skills'))
    collisions.extend(check_numbering_collisions(root, '.agent/.agents/skills'))
    collisions.extend(check_numbering_collisions(root, '.agent/workflows'))
    print(f"Numbering Collisions/Gaps: {collisions if collisions else 'None'}")
    
    pollution = check_root_pollution(root)
    print(f"Root Pollution: {pollution if pollution else 'None'}")
    
    encoding = check_encoding(root)
    print(f"Encoding Issues (BOM): {encoding if encoding else 'None'}")
    
    version = check_version_consistency(root)
    print(f"Version Consistency: {version}")
    
    # Workflow sequence check
    workflows_dir = os.path.join(root, '.agent', 'workflows')
    wf_items = sorted([f for f in os.listdir(workflows_dir) if f.endswith('.md')])
    wf_nums = [int(f.split('-')[0]) for f in wf_items if '-' in f and f.split('-')[0].isdigit()]
    wf_anomaly = False
    if wf_nums:
        if wf_nums != list(range(1, len(wf_nums) + 1)):
            wf_anomaly = True
    print(f"Workflow Sequence: {'NOMINAL' if not wf_anomaly else 'ANOMALY DETECTED'}")

if __name__ == "__main__":
    main()

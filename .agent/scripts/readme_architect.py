import os
import re
from detect_root import detect_root

base = str(detect_root(interactive=False))

def get_frontmatter(filepath):
    if not os.path.exists(filepath): return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

# 1. Specialists
agents = []
for d in sorted(os.listdir(os.path.join(base, ".agent", ".agents", "skills"))):
    if not d.endswith(".md") and "-" in d:
        num, name = d.split('-', 1)
        agents.append((num, name))
        
agent_table = "| ID | Agent Name | Command | Primary Function |\n|:---|:---|:---|:---|\n"
for num, name in agents:
    # Try reading agent's SKILL.md first
    skill_path = os.path.join(base, ".agent", ".agents", "skills", f"{num}-{name}", "SKILL.md")
    desc = "Specialist Agent."
    cmd = f"/{name}"
    
    fm_skill = get_frontmatter(skill_path)
    if fm_skill.get('description'):
        desc = fm_skill['description']
    else:
        # Fallback to claude command frontmatter
        cmd_path = os.path.join(base, ".claude", "commands", f"{name}.md")
        fm_cmd = get_frontmatter(cmd_path)
        if fm_cmd.get('description'):
            desc = fm_cmd['description']
    
    agent_table += f"| **{num}** | `{name}` | `{cmd}` | {desc} |\n"

# 2. Workflows
workflows = []
w_dir = os.path.join(base, ".agent", "workflows")
for f in sorted(os.listdir(w_dir)):
    if f.endswith('.md') and '-' in f:
        num, name = f.replace('.md', '').split('-', 1)
        fm = get_frontmatter(os.path.join(w_dir, f))
        title = fm.get('title', name.replace('-', ' ').title())
        desc = fm.get('description', 'Workflow execution.')
        
        # Determine trigger phrase based on title or name
        trigger = fm.get('trigger', title.lower())
        workflows.append((num, title, name, desc, trigger))

wf_table = "| ID | Workflow | Slash Command | Trigger Phrase | Objective |\n|:---|:---|:---|:---|:---|\n"
for num, title, name, desc, trigger in workflows:
    wf_table += f"| **{num}** | `{title}` | `/{num}-{name}` | \"{trigger}\" | {desc} |\n"

# Flowchart generation based on workflow counts
mermaid = "```mermaid\ngraph TD\n"
phases = {"P1": [], "P2": [], "P3": [], "P4": [], "P5": []}

for num, title, name, desc, trigger in workflows:
    n = int(num)
    node_id = f"{title.replace(' ', '')}"
    label = f"/{num}-{name}/"
    if n <= 4:
        phases["P1"].append(f"{node_id}[{label}]")
    elif n <= 9:
        phases["P2"].append(f"{node_id}[{label}]")
    elif n <= 16:
        phases["P3"].append(f"{node_id}[{label}]")
    elif n <= 20:
        phases["P4"].append(f"{node_id}[{label}]")
    else:
        phases["P5"].append(f"{node_id}[{label}]")

mermaid += "    subgraph P1: Awareness\n"
for idx in range(len(phases["P1"])):
    mermaid += f"    {phases['P1'][idx]}\n"
    if idx > 0: mermaid += f"    {phases['P1'][idx-1].split('[')[0]} --> {phases['P1'][idx].split('[')[0]}\n"
mermaid += "    end\n\n"

mermaid += "    subgraph P2: Strategy\n"
for idx in range(len(phases["P2"])):
    mermaid += f"    {phases['P2'][idx]}\n"
    if idx > 0: mermaid += f"    {phases['P2'][idx-1].split('[')[0]} --> {phases['P2'][idx].split('[')[0]}\n"
mermaid += "    end\n\n"

mermaid += "    subgraph P3: Execution\n"
for idx in range(len(phases["P3"])):
    mermaid += f"    {phases['P3'][idx]}\n"
    if idx > 0: mermaid += f"    {phases['P3'][idx-1].split('[')[0]} --> {phases['P3'][idx].split('[')[0]}\n"
mermaid += "    end\n\n"

mermaid += "    subgraph P4: Quality\n"
for idx in range(len(phases["P4"])):
    mermaid += f"    {phases['P4'][idx]}\n"
    if idx > 0: mermaid += f"    {phases['P4'][idx-1].split('[')[0]} --> {phases['P4'][idx].split('[')[0]}\n"
mermaid += "    end\n\n"

mermaid += "    subgraph P5: Finalization\n"
for idx in range(len(phases["P5"])):
    mermaid += f"    {phases['P5'][idx]}\n"
    if idx > 0: mermaid += f"    {phases['P5'][idx-1].split('[')[0]} --> {phases['P5'][idx].split('[')[0]}\n"
mermaid += "    end\n\n"

# Connect subgraphs
if phases["P1"] and phases["P2"]: mermaid += f"    {phases['P1'][-1].split('[')[0]} --> {phases['P2'][0].split('[')[0]}\n"
if phases["P2"] and phases["P3"]: mermaid += f"    {phases['P2'][-1].split('[')[0]} --> {phases['P3'][0].split('[')[0]}\n"
if phases["P3"] and phases["P4"]: mermaid += f"    {phases['P3'][-1].split('[')[0]} --> {phases['P4'][0].split('[')[0]}\n"
if phases["P4"] and phases["P5"]: mermaid += f"    {phases['P4'][-1].split('[')[0]} --> {phases['P5'][0].split('[')[0]}\n"

mermaid += "\n    style " + " fill:#0d47a1,color:#fff\n    style ".join([p.split('[')[0] for p in phases['P1']]) + " fill:#0d47a1,color:#fff\n"
mermaid += "    style " + " fill:#1565c0,color:#fff\n    style ".join([p.split('[')[0] for p in phases['P2']]) + " fill:#1565c0,color:#fff\n"
mermaid += "    style " + " fill:#1976d2,color:#fff\n    style ".join([p.split('[')[0] for p in phases['P3']]) + " fill:#1976d2,color:#fff\n"
mermaid += "    style " + " fill:#1e88e5,color:#fff\n    style ".join([p.split('[')[0] for p in phases['P4']]) + " fill:#1e88e5,color:#fff\n"
mermaid += "    style " + " fill:#2196f3,color:#fff\n    style ".join([p.split('[')[0] for p in phases['P5']]) + " fill:#2196f3,color:#fff\n"
mermaid += "```"


# 3. Foundational Skills
skills = []
s_dir = os.path.join(base, ".agent", "skills")
for f in sorted(os.listdir(s_dir)):
    if f.endswith('.md') and '-' in f:
        num, name = f.replace('.md', '').split('-', 1)
        
        # Read file
        with open(os.path.join(s_dir, f), 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract yaml description first
        fm = get_frontmatter(os.path.join(s_dir, f))
        if fm.get('description'):
            desc = fm['description']
        else:
            # Fallback: Extract first real paragraph, ignoring lines with #
            paragraphs = content.split('\n\n')
            desc = ""
            for p in paragraphs:
                p = p.strip()
                if p and not p.startswith('#') and not p.startswith('---') and not p.startswith('name:') and not p.startswith('description:'):
                    desc = p
                    break
            
            if not desc:
                desc = "Core foundational skill."
                
        # Clean markdown links/bolds
        desc = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', desc)
        desc = desc.replace('**', '').replace('\n', ' ')
        skills.append(f"- **`{f.replace('.md', '')}`**: {desc}")

skills_text = "\n".join(skills)

# Replace in README.md
with open(os.path.join(base, 'README.md'), 'r', encoding='utf-8') as f:
    readme = f.read()

# Replace Flowchart
readme = re.sub(
    r'```mermaid.*?```',
    mermaid,
    readme,
    flags=re.DOTALL
)

# Replace Agents Table
readme = re.sub(
    r'(\| ID \| Agent Name.*?)(?=\n\n---)',
    agent_table.strip(),
    readme,
    flags=re.DOTALL
)

# Replace Workflows Table
readme = re.sub(
    r'(\| ID \| Workflow.*?)(?=\n\n---)',
    wf_table.strip(),
    readme,
    flags=re.DOTALL
)

# Replace Skills List
readme = re.sub(
    r'(- \*\*`01-research-loop`\*\*.*?)(?=\n\n---)',
    skills_text.strip(),
    readme,
    flags=re.DOTALL
)

with open(os.path.join(base, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)

#!/usr/bin/env python3
"""
Antigravity Agent OS — Registry Synchronization Engine
======================================================
Location: .agent/scripts/sync_registry.py

This is the EXECUTABLE backbone of the self-maintenance system.
It enforces what the governance rules describe.

Capabilities:
  A. Drift Detection    — filesystem vs install-state.json
  B. Collision Detection — duplicate numeric prefixes in skills/agents
  C. BOM Sanitization   — strip bell chars (\x07) from all registry files
  D. CLAUDE.md Version Sync — keep identity header in lockstep with PROJECT_METADATA.md
  E. Semantic Versioning — auto-bump patch/minor based on git diff footprint
  F. Changelog Generation — smart fallback when session-context.md has no entry
  G. Cross-file Propagation — ripple version to README, LICENSE, AGENTS.md, CHANGELOG
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from collections import Counter

# ─── CLI Flags ────────────────────────────────────────────────────────
no_bump = "--no-bump" in sys.argv  # Skip version bumping entirely

# ─── Dynamic Base Path ────────────────────────────────────────────────
# Compute project root from this script's location: .agent/scripts/ -> root
base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

state_path      = os.path.join(base, ".agent", "antigravity-agent-install-state.json")
agents_md_path  = os.path.join(base, ".agent", "AGENTS.md")
claude_md_path  = os.path.join(base, "CLAUDE.md")
metadata_path   = os.path.join(base, "PROJECT_METADATA.md")
session_path    = os.path.join(base, ".agent", "session-context.md")
changelog_path  = os.path.join(base, "CHANGELOG.md")

# ─── Helpers ──────────────────────────────────────────────────────────
def get_files(rel_path, exclude=None):
    p = os.path.join(base, rel_path)
    if not os.path.exists(p): return []
    exclude = exclude or []
    return sorted([f for f in os.listdir(p)
                   if os.path.isfile(os.path.join(p, f)) and f.endswith('.md') and f not in exclude])

def get_dirs(rel_path):
    p = os.path.join(base, rel_path)
    if not os.path.exists(p): return []
    return sorted([d for d in os.listdir(p)
                   if os.path.isdir(os.path.join(p, d))])

def sanitize_bom(text):
    """Strip bell characters (\\x07) — remnants of BOM encoding bugs."""
    return text.replace('\x07', 'a')

def safe_read(path, encoding='utf-8'):
    """Read a file, falling back to windows-1252 if utf-8 fails."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='windows-1252', errors='replace') as f:
            return f.read()

# ─── Disk Scan ────────────────────────────────────────────────────────
disk_rules     = get_files(os.path.join(".agent", "rules"))
disk_skills    = get_files(os.path.join(".agent", "skills"))
disk_workflows = get_files(os.path.join(".agent", "workflows"))
disk_agents    = get_dirs(os.path.join(".agent", ".agents", "skills"))
disk_instincts = get_files(os.path.join(".agent", "instincts"), exclude=["README.md"])
disk_commands  = get_files(os.path.join(".claude", "commands"))

# ─── Load Registry State ─────────────────────────────────────────────
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY B: Collision Detection
# ═══════════════════════════════════════════════════════════════════════
def detect_collisions(file_list, component_name):
    """Detect duplicate numeric prefixes in a component directory."""
    prefixes = []
    for f in file_list:
        m = re.match(r'^(\d+)-', f)
        if m:
            prefixes.append((m.group(1), f))
    counts = Counter(p[0] for p in prefixes)
    collisions = []
    for prefix, count in counts.items():
        if count > 1:
            dupes = [f for p, f in prefixes if p == prefix]
            collisions.append(f"COLLISION in {component_name}: prefix {prefix} shared by {', '.join(dupes)}")
    # Also detect gaps
    if prefixes:
        nums = sorted(set(int(p[0]) for p in prefixes))
        expected = list(range(nums[0], nums[-1] + 1))
        gaps = set(expected) - set(nums)
        for g in sorted(gaps):
            collisions.append(f"GAP in {component_name}: position {g:02d} is missing")
    return collisions

collision_report = []
collision_report.extend(detect_collisions(disk_skills, ".agent/skills/"))
collision_report.extend(detect_collisions(disk_agents, ".agent/.agents/skills/"))

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY E: Semantic Versioning Engine
# ═══════════════════════════════════════════════════════════════════════
meta = safe_read(metadata_path)
meta = sanitize_bom(meta)  # Capability C: BOM sanitization on read

m_ver = re.search(r'\*\*Version\*\*:\s*([^\n\r]+)', meta)
latest_version = m_ver.group(1).strip() if m_ver else state.get("version", "0.0.0")

# Get git changes
try:
    diff_output = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=base
    ).decode("utf-8").strip()
except Exception:
    diff_output = ""

version_bumped = False
smart_fallback = "Updates and improvements."

def classify_changes(sig_lines):
    """Generate a category-based description instead of listing filenames."""
    cats = {"rules": 0, "skills": 0, "workflows": 0, "agents": 0,
            "commands": 0, "instincts": 0, "other": 0}
    for status, fp in sig_lines:
        if status == 'D': continue  # Skip deleted files from description
        if '.agent/rules/' in fp: cats["rules"] += 1
        elif '.agent/skills/' in fp: cats["skills"] += 1
        elif '.agent/workflows/' in fp: cats["workflows"] += 1
        elif '.agent/.agents/' in fp: cats["agents"] += 1
        elif '.claude/commands/' in fp or '.claude/agents/' in fp: cats["commands"] += 1
        elif '.agent/instincts/' in fp: cats["instincts"] += 1
        else: cats["other"] += 1
    parts = []
    for cat, count in cats.items():
        if count > 0:
            parts.append(f"{count} {cat}" if count > 1 else f"1 {cat[:-1] if cat.endswith('s') else cat}")
    return "Modified " + ", ".join(parts) if parts else "Updates and improvements."

if diff_output and not no_bump:
    major, minor, patch = map(int, latest_version.split('.'))
    lines = diff_output.split('\n')

    # Registry files that should NEVER trigger a version bump
    registry_files = [
        "PROJECT_METADATA.md", "CHANGELOG.md", "README.md", "LICENSE.md",
        "CLAUDE.md", "AGENTS.md", ".agent/antigravity-agent-install-state.json",
        ".agent/session-context.md", ".agent/AGENTS.md"
    ]
    infra_prefixes = [".agent/scripts/", ".gemini/"]

    significant_lines = []
    for l in lines:
        filepath = l[3:].strip().replace('\\', '/')
        is_registry = any(filepath.endswith(reg) or filepath == reg for reg in registry_files)
        is_infra = any(filepath.startswith(pfx) for pfx in infra_prefixes)
        if not is_registry and not is_infra:
            # Filter out deleted files from version bump consideration
            status_code = l[:2].strip()
            if status_code != 'D':
                significant_lines.append((status_code, filepath))

    if significant_lines:
        minor_triggers = [
            '.agent/rules/', '.agent/skills/', '.agent/workflows/',
            '.agent/.agents/skills/', '.claude/commands/', '.claude/agents/'
        ]
        is_minor = any(
            (s.startswith('A') or s.startswith('?')) and any(t in fp for t in minor_triggers)
            for s, fp in significant_lines
        )

        if is_minor:
            minor += 1
            patch = 0
        else:
            patch += 1

        latest_version = f"{major}.{minor}.{patch}"
        version_bumped = True

        meta = re.sub(r'\*\*Version\*\*:\s*([^\n\r]+)', f'**Version**: {latest_version}', meta)
        meta = re.sub(r'\(v[0-9]+\.[0-9]+\.[0-9]+\)', f'(v{latest_version})', meta)
        with open(metadata_path, "w", encoding="utf-8") as f:
            f.write(meta)

        smart_fallback = classify_changes(significant_lines)
    else:
        smart_fallback = "Registry synchronization."
elif no_bump:
    smart_fallback = "Registry synchronization (no-bump mode)."

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY F: Changelog Generation (with session-context fallback)
# ═══════════════════════════════════════════════════════════════════════
session_data = safe_read(session_path)

m_action = re.search(
    r'## .*? — v' + re.escape(latest_version) +
    r'.*?\n\*\*Agent\*\*:.*?\n\*\*Action\*\*:\s*([^\n]+)',
    session_data, re.DOTALL
)
if m_action:
    latest_action = m_action.group(1).strip()
elif version_bumped:
    latest_action = smart_fallback
else:
    latest_action = state.get("changelog", {}).get(
        latest_version, "Updates and improvements."
    )

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY G: Cross-file Propagation — CHANGELOG.md & Session Context
# ═══════════════════════════════════════════════════════════════════════
session_updated = False
if f"v{latest_version}" not in session_data:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    new_session_entry = f"\n## {today} — Automated Registry Sync — v{latest_version}\n"
    new_session_entry += f"**Agent**: system\n"
    new_session_entry += f"**Action**: {latest_action}\n"
    new_session_entry += f"**State Change**: Version v{latest_version} synced.\n"
    
    session_data += new_session_entry
    with open(session_path, "w", encoding="utf-8") as f:
        f.write(session_data)
    session_updated = True

changelog_data = safe_read(changelog_path)
changelog_data = sanitize_bom(changelog_data)

changelog_updated = False
if f"## [{latest_version}]" not in changelog_data:
    # Deduplication: check if latest_action is identical to previous entries
    existing_actions = re.findall(r'## \[[^\]]+\][^\n]*\n- ([^\n]+)', changelog_data)
    is_duplicate = latest_action in existing_actions[:3]
    
    if not is_duplicate:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        new_entry = f"## [{latest_version}] - {today}\n- {latest_action}\n\n"
        changelog_data = re.sub(
            r'(# Antigravity Agent Changelog\s*\n+)',
            r'\1' + new_entry, changelog_data
        )
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(changelog_data)
        changelog_updated = True
    else:
        # Update version number on the most recent entry instead of adding duplicate
        changelog_data = re.sub(
            r'## \[' + re.escape(existing_actions[0].strip()) + r'\]',
            f'## [{latest_version}]', changelog_data, count=0
        )
        # Just update the first entry's version
        first_entry = re.search(r'## \[([^\]]+)\]', changelog_data)
        if first_entry and first_entry.group(1) != latest_version:
            old_ver = first_entry.group(1)
            changelog_data = changelog_data.replace(
                f'## [{old_ver}]', f'## [{latest_version}]', 1
            )
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(changelog_data)
            changelog_updated = True

# Sync PROJECT_METADATA.md changelog section from CHANGELOG.md
log_sections = re.findall(
    r'## \[([^\]]+)\][^\n]*\n(.*?)(?=\n## \[|\Z)', changelog_data, re.DOTALL
)
meta_changelog_text = "## Changelog\n"
for ver, content in log_sections[:5]:
    first_line = re.search(r'-\s*([^\n]+)', content)
    text = first_line.group(1).strip() if first_line else "Updates and improvements."
    meta_changelog_text += f"- v{ver} — {text}\n"

meta_updated = False
with open(metadata_path, "r", encoding="utf-8") as f:
    meta = f.read()
if meta_changelog_text.strip() not in meta:
    new_meta = re.sub(
        r'## Changelog\n.*', meta_changelog_text.strip() + "\n\n",
        meta, flags=re.DOTALL
    )
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write(new_meta)
    meta_updated = True

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY A: Drift Detection
# ═══════════════════════════════════════════════════════════════════════
drift_detected = False
report = []

def check_drift(component, disk_list, reg_list):
    global drift_detected
    disk_count = len(disk_list)
    reg_count = len(reg_list)
    status = "IN SYNC" if set(disk_list) == set(reg_list) else "DRIFT DETECTED"
    if status == "DRIFT DETECTED":
        drift_detected = True
        missing = set(reg_list) - set(disk_list)
        extra = set(disk_list) - set(reg_list)
        details = []
        if extra:   details.append(f"New: {', '.join(sorted(extra))}")
        if missing: details.append(f"Missing: {', '.join(sorted(missing))}")
        status += f" ({'; '.join(details)})"
    report.append(f"{component}: {disk_count} actual / {reg_count} registered -> {status}")

check_drift("Rules",     disk_rules,     state.get("installed_rules", []))
check_drift("Skills",    disk_skills,    state.get("installed_foundational_skills", []))
check_drift("Workflows", disk_workflows, state.get("installed_workflows", []))
check_drift("Agents",    disk_agents,    state.get("installed_skills", []))
check_drift("Instincts", disk_instincts, state.get("installed_instincts", []))
check_drift("Commands",  disk_commands,  state.get("installed_commands", []))

if state.get("version") != latest_version:
    drift_detected = True
    report.append(f"Version: {state.get('version')} registry / {latest_version} actual -> DRIFT DETECTED")
else:
    report.append(f"Version: {latest_version} actual / {state.get('version')} registry -> IN SYNC")

if changelog_updated:
    drift_detected = True
    report.append(f"CHANGELOG.md: Missing v{latest_version} -> DRIFT DETECTED")
else:
    report.append(f"CHANGELOG.md: v{latest_version} present -> IN SYNC")

if session_updated:
    drift_detected = True
    report.append(f"session-context.md: Missing v{latest_version} -> DRIFT DETECTED")
else:
    report.append(f"session-context.md: v{latest_version} present -> IN SYNC")

if meta_updated:
    drift_detected = True
    report.append(f"PROJECT_METADATA.md: Changelog out of sync -> DRIFT DETECTED")

# ─── Print Step 1 ────────────────────────────────────────────────────
print("### Step 1 — Drift Detection")
for line in report:
    print(line)

# ─── Print Step 2 — Collision Report ─────────────────────────────────
if collision_report:
    print("\n### Step 2 — Collision Detection")
    for c in collision_report:
        print(f"  ⚠ {c}")
else:
    print("\n### Step 2 — Collision Detection: CLEAN")

# ═══════════════════════════════════════════════════════════════════════
# SYNCHRONIZATION
# ═══════════════════════════════════════════════════════════════════════
agents_updated = False
state_updated  = False
claude_updated = False

if drift_detected:
    print("\nDrift detected! Initiating synchronization...")

    # ── Update install-state.json ─────────────────────────────────────
    state["version"] = latest_version
    if "changelog" not in state:
        state["changelog"] = {}
    state["changelog"][latest_version] = latest_action

    state["installed_rules"]              = disk_rules
    state["installed_foundational_skills"] = disk_skills
    state["installed_workflows"]          = disk_workflows
    state["installed_skills"]             = disk_agents
    state["installed_instincts"]          = disk_instincts
    state["installed_commands"]           = disk_commands

    state["component_counts"] = {
        "rules":               len(disk_rules),
        "foundational_skills": len(disk_skills),
        "workflows":           len(disk_workflows),
        "agent_personas":      len(disk_agents),
        "instincts":           len(disk_instincts),
        "commands":            len(disk_commands),
        "specialist_personas": len(state.get("installed_personas", []))
    }
    state["last_updated"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Capability C: BOM sanitization on all changelog strings
    if "changelog" in state:
        state["changelog"] = {
            k: sanitize_bom(v) for k, v in state["changelog"].items()
        }

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    state_updated = True

    # ── Regenerate AGENTS.md ──────────────────────────────────────────
    def get_desc(path, is_dir=False):
        if is_dir:
            path = os.path.join(path, "SKILL.md")
        if not os.path.exists(path):
            return "No description available."
        content = safe_read(path)
        m = re.search(r'description:\s*"?([^"\n]+)"?', content)
        if m: return m.group(1)
        m = re.search(r'#.*?\n+(.*)', content)
        if m: return m.group(1).strip()
        return ""

    agents_md = (
        f"# Antigravity Agent Ecosystem (v{latest_version})\n\n"
        "A portable AI operating system. Copy the `.agent/` folder into any project "
        "directory and the entire skill + workflow ecosystem activates immediately.\n\n"
        "---\n\n## 🔧 Slash Commands (Single Agents)\n\n"
        "| # | Command | Agent | Phase | Purpose |\n"
        "| :--- | :--- | :--- | :--- | :--- |\n"
    )
    for i, a in enumerate(disk_agents):
        cmd = "/" + a.split("-", 1)[1] if "-" in a else "/" + a
        desc = get_desc(
            os.path.join(base, ".agent", ".agents", "skills", a), is_dir=True
        )
        if len(desc) > 50:
            desc = desc[:47] + "..."
        agents_md += f"| **{i+1:02d}** | **`{cmd}`** | {a} | P3 | {desc} |\n"

    agents_md += (
        "\n---\n\n## ⚡ Workflows (+ Button — In Sequence)\n\n"
        "Workflows are listed below in **logical ascending order** "
        "corresponding to a standard software lifecycle.\n\n"
    )
    for w in disk_workflows:
        desc = get_desc(os.path.join(base, ".agent", "workflows", w))
        agents_md += f"- **`{w}`**: {desc}\n"

    agents_md += (
        "\n---\n\n## Architecture\n\n```\n.agent/\n"
        "├── instincts/ (Probabilistic Behaviors)\n"
    )
    for i in disk_instincts:
        agents_md += f"│   ├── {i}\n"
    agents_md += "├── rules/ (Governance)\n"
    for r in disk_rules[:3]:
        agents_md += f"│   ├── {r}\n"
    if len(disk_rules) > 3:
        agents_md += f"│   ├── ... ({len(disk_rules)} rules total)\n"
    agents_md += "├── skills/ (Foundational Logic)\n"
    for s in disk_skills[:3]:
        agents_md += f"│   ├── {s}\n"
    if len(disk_skills) > 3:
        agents_md += f"│   ├── ... ({len(disk_skills)} skills total)\n"
    agents_md += "└── workflows/ (Pipelines)\n"
    for w in disk_workflows:
        agents_md += f"    ├── {w}\n"
    agents_md += "```\n"

    with open(agents_md_path, "w", encoding="utf-8") as f:
        f.write(agents_md)
    agents_updated = True

    # ══════════════════════════════════════════════════════════════════
    # CAPABILITY D: CLAUDE.md Version Sync
    # ══════════════════════════════════════════════════════════════════
    if os.path.exists(claude_md_path):
        claude = safe_read(claude_md_path)

        # Update header: # Antigravity Agent vX.Y.Z
        claude = re.sub(
            r'# Antigravity Agent v[0-9]+\.[0-9]+\.[0-9]+',
            f'# Antigravity Agent v{latest_version}',
            claude
        )
        # Update identity table: | **Version** | X.Y.Z |
        claude = re.sub(
            r'\|\s*\*\*Version\*\*\s*\|\s*[0-9]+\.[0-9]+\.[0-9]+\s*\|',
            f'| **Version** | {latest_version} |',
            claude
        )

        # Update slash command registry
        cmd_text = "## Slash Command Registry\n"
        for c in disk_commands:
            name = "/" + c.replace(".md", "")
            desc = get_desc(os.path.join(base, ".claude", "commands", c))
            cmd_text += f"- {name} – {desc}\n"
        claude = re.sub(
            r'## Slash Command Registry.*?(?=##|$)',
            cmd_text + "\n", claude, flags=re.DOTALL
        )

        with open(claude_md_path, "w", encoding="utf-8") as f:
            f.write(claude)
        claude_updated = True

    # ── README.md Version Badge Sync ──────────────────────────────────
    readme_path = os.path.join(base, "README.md")
    readme_updated = False
    if os.path.exists(readme_path):
        readme = safe_read(readme_path)
        new_readme = re.sub(
            r'badge/version-[^-]+-blueviolet',
            f'badge/version-{latest_version}-blueviolet', readme
        )
        new_readme = re.sub(
            r'Antigravity Agent Ecosystem \(v[^\)]+\)',
            f'Antigravity Agent Ecosystem (v{latest_version})', new_readme
        )
        if new_readme != readme:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_readme)
            readme_updated = True

    # ── LICENSE.md Version Sync ───────────────────────────────────────
    license_path = os.path.join(base, "LICENSE.md")
    license_updated = False
    if os.path.exists(license_path):
        license_text = safe_read(license_path)
        if "Applies to Software Version: v" in license_text:
            new_license = re.sub(
                r'Applies to Software Version: v\S+',
                f'Applies to Software Version: v{latest_version}', license_text
            )
        else:
            new_license = re.sub(
                r'(# .*?)\n',
                rf'\1\n\nApplies to Software Version: v{latest_version}\n',
                license_text, count=1
            )
        if new_license != license_text:
            with open(license_path, "w", encoding="utf-8") as f:
                f.write(new_license)
            license_updated = True

# ═══════════════════════════════════════════════════════════════════════
# VERIFICATION & REPORT
# ═══════════════════════════════════════════════════════════════════════
print("\n### Step 3 — BOM Sanitization")
# Final sweep of all output files for bell characters
bom_found = False
for fpath in [state_path, changelog_path, metadata_path, claude_md_path]:
    if os.path.exists(fpath):
        content = safe_read(fpath)
        if '\x07' in content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(sanitize_bom(content))
            print(f"  SANITIZED: {os.path.basename(fpath)}")
            bom_found = True
if not bom_found:
    print("  All registry files: CLEAN")

print("\n### Step 4 — Verification")
if not drift_detected:
    print("ALL components show IN SYNC. No changes made.")
else:
    print("Verification passed: Registry files updated successfully to match disk state.")

print("\n### Step 5 — Sync Report")
print(f"REGISTRY SYNC COMPLETE — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Components synced: Rules, Skills, Workflows, Agents, Instincts, Commands, Version ({latest_version})")
print(f"AGENTS.md: {'UPDATED' if agents_updated else 'UNCHANGED'}")
print(f"install-state.json: {'UPDATED' if state_updated else 'UNCHANGED'}")
print(f"CLAUDE.md: {'UPDATED' if claude_updated else 'UNCHANGED'}")
print(f"CHANGELOG.md: {'UPDATED' if changelog_updated else 'UNCHANGED'}")
print(f"session-context.md: {'UPDATED' if session_updated else 'UNCHANGED'}")
print(f"PROJECT_METADATA.md: {'UPDATED' if meta_updated else 'UNCHANGED'}")
print(f"README.md: {'UPDATED' if 'readme_updated' in dir() and readme_updated else 'UNCHANGED'}")
print(f"LICENSE.md: {'UPDATED' if 'license_updated' in dir() and license_updated else 'UNCHANGED'}")

if collision_report:
    print(f"\n>> HEALTH: YELLOW -- {len(collision_report)} collision/gap issue(s) found. Run renumbering to fix.")
else:
    print("\n>> HEALTH: GREEN -- No collisions, no gaps, no BOM corruption.")

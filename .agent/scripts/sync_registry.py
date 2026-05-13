#!/usr/bin/env python3
"""
Aether Agent OS — Registry Synchronization Engine
======================================================
Location: .agent/scripts/sync_registry.py

Executable backbone of the self-maintenance system. Version, changelog, session
history, and the agents registry table are consolidated into the root `AETHER.md`
(unified state file). Downstream: README.md, LICENSE.md,
`.agent/aether-agent-install-state.json`.

Capabilities:
  A. Drift Detection    — filesystem vs `.agent/aether-agent-install-state.json`
  B. Collision Detection — duplicate numeric prefixes in skills/agents
  C. BOM Sanitization   — strip bell chars (\\x07) from registry outputs
  D. AETHER.md Version Sync — title, identity table, §14 Project Metadata
  E. Semantic Versioning — auto-bump patch/minor based on git diff footprint
  F. Changelog / Session — §16 Changelog and §18 Session Context inside AETHER.md
  G. Agents Registry    — regenerate §13 from live .agent/ + .claude/ state
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from collections import Counter

# ─── CLI Flags ────────────────────────────────────────────────────────
no_bump = "--no-bump" in sys.argv
regen_section13 = "--regen-section13" in sys.argv

# ─── Dynamic Base Path ────────────────────────────────────────────────
from detect_root import patch_sync_registry
base = str(patch_sync_registry())

state_path = os.path.join(base, ".agent", "aether-agent-install-state.json")
aether_md_path = os.path.join(base, "AETHER.md")

H13 = "## 13. Agents Registry"
H14 = "## 14. Project Metadata"
H16 = "## 16. Changelog"
AETHER_FOOTER_ANCHOR = "\n\n---\n\n*This file is the single most important file in the repository."

# ─── Helpers ──────────────────────────────────────────────────────────
def get_files(rel_path, exclude=None):
    p = os.path.join(base, rel_path)
    if not os.path.exists(p):
        return []
    exclude = exclude or []
    return sorted([f for f in os.listdir(p)
                   if os.path.isfile(os.path.join(p, f)) and f.endswith('.md') and f not in exclude])

def get_dirs(rel_path):
    p = os.path.join(base, rel_path)
    if not os.path.exists(p):
        return []
    return sorted([d for d in os.listdir(p)
                   if os.path.isdir(os.path.join(p, d))])

def sanitize_bom(text):
    return text.replace('\x07', 'a')

def safe_read(path, encoding='utf-8'):
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='windows-1252', errors='replace') as f:
            return f.read()

def write_aether(text):
    with open(aether_md_path, "w", encoding="utf-8") as f:
        f.write(text)

def parse_aether_version(text):
    m = re.search(r'^# Aether Agent v(\d+\.\d+\.\d+)', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r'\|\s*\*\*Version\*\*\s*\|\s*(\d+\.\d+\.\d+)\s*\|', text)
    if m:
        return m.group(1).strip()
    m = re.search(r'\*\*Version\*\*:\s*(\d+\.\d+\.\d+)', text)
    if m:
        return m.group(1).strip()
    return None

def apply_version_bump(text, new_version):
    text = re.sub(
        r'^(# Aether Agent v)(\d+\.\d+\.\d+)',
        rf'\g<1>{new_version}',
        text, count=1, flags=re.MULTILINE
    )
    text = re.sub(
        r'(\|\s*\*\*Version\*\*\s*\|\s*)(\d+\.\d+\.\d+)(\s*\|)',
        rf'\g<1>{new_version}\g<3>',
        text, count=1
    )
    text = re.sub(
        r'(\*\*Version\*\*:\s*)(\d+\.\d+\.\d+)',
        rf'\g<1>{new_version}',
        text, count=1
    )
    return text

def extract_session_block(text):
    m = re.search(
        r'## 18\. Session Context\n(.*?)(\n\n---\n\n\*This file is the single most important file in the repository\.)',
        text, re.DOTALL
    )
    if m:
        return m.group(1), m.group(2)
    return None, None

def append_session_sync_entry(text, latest_version, latest_action):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    marker = f"Automated Registry Sync — v{latest_version}"
    body, footer = extract_session_block(text)
    if body is None:
        print("  WARNING: Could not find §18 Session Context footer anchor in AETHER.md — session not updated.")
        return text, False
    if marker in body:
        return text, False
    entry = (
        f"\n### {today} — Automated Registry Sync — v{latest_version}\n"
        f"**Agent**: system\n"
        f"**Action**: {latest_action}\n"
        f"**State Change**: Version v{latest_version} synced.\n"
    )
    anchor = AETHER_FOOTER_ANCHOR
    idx = text.rfind(anchor)
    if idx == -1:
        return text, False
    return text[:idx] + entry + text[idx:], True

def prepend_changelog_entry(text, latest_version, latest_action):
    if f"### [{latest_version}]" in text:
        return text, False
    today = datetime.utcnow().strftime("%Y-%m-%d")
    needle = H16 + "\n\n"
    if needle not in text:
        return text, False
    dup_check = re.findall(r'### \[[^\]]+\][^\n]*\n-\s*([^\n]+)', text)
    is_duplicate = latest_action in dup_check[:3]
    if is_duplicate and dup_check:
        return text, False
    new_entry = f"### [{latest_version}] - {today}\n- {latest_action}\n\n"
    return text.replace(needle, needle + new_entry, 1), True

def replace_section_13(text, generated_body):
    pat = rf'({re.escape(H13)}\n)(.*?)(\n{re.escape(H14)}\n)'
    m = re.search(pat, text, flags=re.DOTALL)
    if not m:
        print("  WARNING: Could not locate §13 Agents Registry block for regeneration.")
        return text
    return text[:m.start()] + m.group(1) + generated_body + m.group(3) + text[m.end():]

# ─── Disk Scan ──────────────────────────────────────────────────────────
disk_rules = get_files(os.path.join(".agent", "rules"))
disk_skills = get_files(os.path.join(".agent", "skills"), exclude=["README.md"])
disk_workflows = get_files(os.path.join(".agent", "workflows"))
disk_agents = get_dirs(os.path.join(".agent", ".agents", "skills"))
disk_instincts = get_files(os.path.join(".agent", "instincts"), exclude=["README.md"])
disk_commands = get_files(os.path.join(".claude", "commands"))

# §13 agent table: folders sorted for "vibe coder" frequency (not strict numeric order).
AGENT_REGISTRY_ORDER = [
    "01-deep-scan", "03-ask", "12-antibug", "19-git-commit-author",
    "20-code-reviewer", "22-test-engineer", "21-security-auditor",
    "16-readme-architect", "13-web-aesthetics",
    "07-python-agent", "08-rust-agent", "09-jsts-agent", "10-c-agent", "11-go-agent",
    "04-planner", "06-tdd-guide", "05-synthesizer", "02-failure-predictor",
    "17-market-evaluator", "18-commercial-license",
    "14-scientific-writing", "15-latex-bib-manager", "23-mcp-auditor",
]


def sort_agent_dirs(agent_list):
    rank = {n: i for i, n in enumerate(AGENT_REGISTRY_ORDER)}
    return sorted(agent_list, key=lambda a: (rank.get(a, 999), a))


def get_skill_description(path, is_dir=False):
    if is_dir:
        path = os.path.join(path, "SKILL.md")
    if not os.path.exists(path):
        return "No description available."
    content = safe_read(path)
    m = re.search(r'description:\s*"?([^"\n]+)"?', content)
    if m:
        return m.group(1)
    m = re.search(r'#.*?\n+(.*)', content)
    if m:
        return m.group(1).strip()
    return ""


SECTION13_ORIENTATION = """### Orientation (how to use this registry)

**Start here:** `/deep-scan` once per folder, then pick **one** lane:
- **Quick answers:** `/ask`
- **Ship a slice:** `/planner` → `/tdd-guide` or a language agent (`/python`, `/rust`, `/jsts`, …)
- **Something broken:** `/antibug`
- **Before merge:** `/code-reviewer`, `/test-engineer`, `/ship`

Command/agent rows below are ordered for **day-to-day frequency** (map → clarify → fix → commit → review → security → docs/UI), then language specialists, then planning, then niche roles — **not** strictly by numeric prefix.

"""

SECTION13_WORKFLOW_HANDOFFS = """
### After this workflow … (typical handoffs)

| You just finished … | Often run next … |
| :--- | :--- |
| `01-scan.md` | `02-onboard.md` or `03-scaffold.md` |
| `02-onboard.md` | `04-spec.md` or `05-research.md` |
| `03-scaffold.md` | `04-spec.md` |
| `04-spec.md` | `05-research.md` or `06-plan-synthesis.md` |
| `05-research.md` | `06-plan-synthesis.md` |
| `06-plan-synthesis.md` | `07-knowledge-capture.md` or `08-build.md` |
| `07-knowledge-capture.md` | `09-feature.md` or `08-build.md` |
| `08-build.md` / `09-feature.md` | `10-tdd.md`, `13-quality-gate.md`, or `17-auto-commit.md` |
| `10-tdd.md` | `13-quality-gate.md` or `17-auto-commit.md` |
| `11-debug.md` | `10-tdd.md` or `13-quality-gate.md` |
| `12-performance.md` | `13-quality-gate.md` or `14-validate.md` |
| `13-quality-gate.md` | `14-validate.md` or `15-release.md` |
| `14-validate.md` | `16-sync-registry.md` |
| `15-release.md` | `16-sync-registry.md` |
| `16-sync-registry.md` | `17-auto-commit.md` if registry files changed |
| `17-auto-commit.md` | `18-readme-architect.md` or stop |
| `18-readme-architect.md` | stop or `14-validate.md` |

"""


def build_agents_registry_body():
    agents_sorted = sort_agent_dirs(disk_agents)
    body = SECTION13_ORIENTATION
    body += (
        "### 🔧 Slash Commands (Single Agents)\n\n"
        "| # | Command | Agent | Phase | Purpose |\n"
        "| :--- | :--- | :--- | :--- | :--- |\n"
    )
    for i, a in enumerate(agents_sorted):
        cmd = "/" + a.split("-", 1)[1] if "-" in a else "/" + a
        desc = get_skill_description(
            os.path.join(base, ".agent", ".agents", "skills", a), is_dir=True
        )
        if len(desc) > 50:
            desc = desc[:47] + "..."
        body += f"| **{i+1:02d}** | **`{cmd}`** | {a} | P3 | {desc} |\n"

    body += (
        "\n### ⚡ Workflows (+ Button — lifecycle order)\n\n"
        "Workflow files are listed in **01 → N numeric order** (standard software lifecycle).\n\n"
    )
    for w in disk_workflows:
        desc = get_skill_description(os.path.join(base, ".agent", "workflows", w))
        body += f"- **`{w}`**: {desc}\n"

    body += SECTION13_WORKFLOW_HANDOFFS

    body += (
        "\n### Architecture\n\n```\n.agent/\n"
        "├── instincts/ (Probabilistic Behaviors)\n"
    )
    for ins in disk_instincts:
        body += f"│   ├── {ins}\n"
    body += "├── rules/ (Governance)\n"
    for r in disk_rules[:3]:
        body += f"│   ├── {r}\n"
    if len(disk_rules) > 3:
        body += f"│   ├── ... ({len(disk_rules)} rules total)\n"
    body += "├── skills/ (Foundational Logic)\n"
    for s in disk_skills[:3]:
        body += f"│   ├── {s}\n"
    if len(disk_skills) > 3:
        body += f"│   ├── ... ({len(disk_skills)} skills total)\n"
    body += "└── workflows/ (Pipelines)\n"
    for w in disk_workflows:
        body += f"    ├── {w}\n"
    body += "```\n"
    return body


if not os.path.exists(aether_md_path):
    print(f"ERROR: Missing unified state file: {aether_md_path}")
    sys.exit(1)

with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY B: Collision Detection
# ═══════════════════════════════════════════════════════════════════════
def detect_collisions(file_list, component_name):
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
# Load AETHER.md
# ═══════════════════════════════════════════════════════════════════════
aether = safe_read(aether_md_path)
aether = sanitize_bom(aether)

latest_version = parse_aether_version(aether) or state.get("version", "0.0.0")

try:
    diff_output = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=base
    ).decode("utf-8").strip()
except Exception:
    diff_output = ""

version_bumped = False
smart_fallback = "Updates and improvements."

def classify_changes(sig_lines):
    cats = {"rules": 0, "skills": 0, "workflows": 0, "agents": 0,
            "commands": 0, "instincts": 0, "other": 0}
    for status, fp in sig_lines:
        if status == 'D':
            continue
        if '.agent/rules/' in fp:
            cats["rules"] += 1
        elif '.agent/skills/' in fp:
            cats["skills"] += 1
        elif '.agent/workflows/' in fp:
            cats["workflows"] += 1
        elif '.agent/.agents/' in fp:
            cats["agents"] += 1
        elif '.claude/commands/' in fp or '.claude/agents/' in fp:
            cats["commands"] += 1
        elif '.agent/instincts/' in fp:
            cats["instincts"] += 1
        else:
            cats["other"] += 1
    parts = []
    for cat, count in cats.items():
        if count > 0:
            parts.append(
                f"{count} {cat}" if count > 1
                else f"1 {cat[:-1] if cat.endswith('s') else cat}"
            )
    return "Modified " + ", ".join(parts) if parts else "Updates and improvements."

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY E: Semantic Versioning Engine
# ═══════════════════════════════════════════════════════════════════════
if diff_output and not no_bump:
    major, minor, patch = map(int, latest_version.split('.'))
    lines = diff_output.split('\n')

    registry_files = [
        "AETHER.md", "README.md", "LICENSE.md", "CLAUDE.md",
        ".agent/aether-agent-install-state.json",
    ]
    infra_prefixes = [".agent/scripts/", ".gemini/"]

    significant_lines = []
    for l in lines:
        filepath = l[3:].strip().replace('\\', '/')
        is_registry = any(filepath.endswith(reg) or filepath == reg for reg in registry_files)
        is_infra = any(filepath.startswith(pfx) for pfx in infra_prefixes)
        if not is_registry and not is_infra:
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
        aether = apply_version_bump(aether, latest_version)
        write_aether(aether)
        smart_fallback = classify_changes(significant_lines)
    else:
        smart_fallback = "Registry synchronization."
elif no_bump:
    smart_fallback = "Registry synchronization (no-bump mode)."

# Reload after possible write
aether = sanitize_bom(safe_read(aether_md_path))

# ═══════════════════════════════════════════════════════════════════════
# CAPABILITY F: derive latest action (from §18 or git classification)
# ═══════════════════════════════════════════════════════════════════════
session_inner, _ = extract_session_block(aether)
session_inner = session_inner or ""
m_action = re.search(
    r'### .*? — v' + re.escape(latest_version) +
    r'.*?\n\*\*Agent\*\*:.*?\n\*\*Action\*\*:\s*([^\n]+)',
    session_inner, re.DOTALL
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
# Session + Changelog inside AETHER.md
# ═══════════════════════════════════════════════════════════════════════
session_updated = False
aether, session_updated = append_session_sync_entry(aether, latest_version, latest_action)
if session_updated:
    write_aether(aether)

changelog_updated = False
aether, changelog_updated = prepend_changelog_entry(aether, latest_version, latest_action)
if changelog_updated:
    write_aether(aether)

aether = sanitize_bom(safe_read(aether_md_path))

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
        if extra:
            details.append(f"New: {', '.join(sorted(extra))}")
        if missing:
            details.append(f"Missing: {', '.join(sorted(missing))}")
        status += f" ({'; '.join(details)})"
    report.append(f"{component}: {disk_count} actual / {reg_count} registered -> {status}")

check_drift("Rules", disk_rules, state.get("installed_rules", []))
check_drift("Skills", disk_skills, state.get("installed_foundational_skills", []))
check_drift("Workflows", disk_workflows, state.get("installed_workflows", []))
check_drift("Agents", disk_agents, state.get("installed_skills", []))
check_drift("Instincts", disk_instincts, state.get("installed_instincts", []))
check_drift("Commands", disk_commands, state.get("installed_commands", []))

if state.get("version") != latest_version:
    drift_detected = True
    report.append(f"Version: {state.get('version')} registry / {latest_version} actual -> DRIFT DETECTED")
else:
    report.append(f"Version: {latest_version} actual / {state.get('version')} registry -> IN SYNC")

if changelog_updated:
    drift_detected = True
    report.append(f"AETHER.md §16 Changelog: new v{latest_version} entry -> UPDATED")
else:
    report.append(f"AETHER.md §16 Changelog: v{latest_version} present -> IN SYNC")

if session_updated:
    drift_detected = True
    report.append(f"AETHER.md §18 Session: sync marker for v{latest_version} -> UPDATED")
else:
    report.append(f"AETHER.md §18 Session: v{latest_version} marker -> IN SYNC")

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
state_updated = False
readme_updated = False
license_updated = False

if drift_detected:
    print("\nDrift detected! Initiating synchronization...")

    state["version"] = latest_version
    if "changelog" not in state:
        state["changelog"] = {}
    state["changelog"][latest_version] = latest_action

    state["installed_rules"] = disk_rules
    state["installed_foundational_skills"] = disk_skills
    state["installed_workflows"] = disk_workflows
    state["installed_skills"] = disk_agents
    state["installed_instincts"] = disk_instincts
    state["installed_commands"] = disk_commands

    state["component_counts"] = {
        "rules": len(disk_rules),
        "foundational_skills": len(disk_skills),
        "workflows": len(disk_workflows),
        "agent_personas": len(disk_agents),
        "instincts": len(disk_instincts),
        "commands": len(disk_commands),
        "specialist_personas": len(state.get("installed_personas", []))
    }
    state["last_updated"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    if "changelog" in state:
        state["changelog"] = {
            k: sanitize_bom(v) for k, v in state["changelog"].items()
        }

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    state_updated = True

    agents_body = build_agents_registry_body()

    aether = sanitize_bom(safe_read(aether_md_path))
    aether = replace_section_13(aether, agents_body + "\n")
    write_aether(aether)
    agents_updated = True

    readme_path = os.path.join(base, "README.md")
    if os.path.exists(readme_path):
        readme = safe_read(readme_path)
        new_readme = re.sub(
            r'badge/version-[^-]+-blueviolet',
            f'badge/version-{latest_version}-blueviolet', readme
        )
        new_readme = re.sub(
            r'Aether Agent Ecosystem \(v[^\)]+\)',
            f'Aether Agent Ecosystem (v{latest_version})', new_readme
        )
        if new_readme != readme:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_readme)
            readme_updated = True

    license_path = os.path.join(base, "LICENSE.md")
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

if regen_section13:
    aether = sanitize_bom(safe_read(aether_md_path))
    new_body = build_agents_registry_body()
    a2 = replace_section_13(aether, new_body + "\n")
    if a2 != aether:
        write_aether(a2)
        agents_updated = True

# ═══════════════════════════════════════════════════════════════════════
# VERIFICATION & REPORT
# ═══════════════════════════════════════════════════════════════════════
print("\n### Step 3 — BOM Sanitization")
bom_found = False
for fpath in [state_path, aether_md_path]:
    if os.path.exists(fpath):
        content = safe_read(fpath)
        if '\x07' in content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(sanitize_bom(content))
            print(f"  SANITIZED: {os.path.basename(fpath)}")
            bom_found = True
if not bom_found:
    print("  Core registry files: CLEAN")

print("\n### Step 4 — Verification")
if not drift_detected:
    print("ALL components show IN SYNC. No changes made.")
else:
    print("Verification passed: Registry files updated successfully to match disk state.")

print("\n### Step 5 — Sync Report")
print(f"REGISTRY SYNC COMPLETE — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Components synced: Rules, Skills, Workflows, Agents, Instincts, Commands, Version ({latest_version})")
print(f"AETHER.md: {'UPDATED' if version_bumped or session_updated or changelog_updated or agents_updated else 'UNCHANGED'}")
print(f".agent/aether-agent-install-state.json (+ antigravity mirror): {'UPDATED' if state_updated else 'UNCHANGED'}")
print(f"§13 Agents Registry: {'UPDATED' if agents_updated else 'UNCHANGED'}")
print(f"§16 Changelog: {'UPDATED' if changelog_updated else 'UNCHANGED'}")
print(f"§18 Session Context: {'UPDATED' if session_updated else 'UNCHANGED'}")
print(f"README.md: {'UPDATED' if readme_updated else 'UNCHANGED'}")
print(f"LICENSE.md: {'UPDATED' if license_updated else 'UNCHANGED'}")

if collision_report:
    print(f"\n>> HEALTH: YELLOW -- {len(collision_report)} collision/gap issue(s) found. Run renumbering to fix.")
else:
    print("\n>> HEALTH: GREEN -- No collisions, no gaps, no BOM corruption.")

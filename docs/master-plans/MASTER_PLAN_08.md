# MASTER PLAN 08 — Project DNA Fingerprinting
**Feature:** Tech-stack fingerprinting that pre-activates skills and suggests workflows based on project type
**Priority:** MEDIUM — makes the system feel intelligent on first session open
**Estimated effort:** 4–5 days
**Depends on:** MASTER_PLAN_03 (flag_scanner.py provides the raw detection), MASTER_PLAN_06 (cache reuses hashes)
**Unlocks:** Plan 09 (telemetry tracks which DNA profiles correlate with best outcomes)

---

## Problem Statement

When you copy .agent/ into a new project, the agent starts blind. It knows nothing about
the project domain, tech stack, or your history with similar projects. Session 1 is always
a discovery session. It reads the files, scans the structure, and begins to understand.

This is wasteful for your fifth FastAPI project. The system already knows from the
first four: which skills are most useful (security-engineering, api-design), which
workflows activate most often (spec-discovery, tdd-guide), which instincts fire most
(INSTINCT-L003 incomplete error paths in async handlers), and what the typical failure
patterns are (database connection pooling, JWT expiry handling).

Project DNA fingerprinting captures this knowledge and reuses it automatically.
The moment /scanner detects "FastAPI + PostgreSQL + React", it pre-activates the
right skill subset, suggests the relevant workflows, and surfaces the top historical
failure patterns for that stack — before you write a single line of code.

---

## Architecture Overview

```
/scanner runs on a new project
        |
        v
flag_scanner.py emits tech_stack + flags
        |
        v
dna_profiler.py computes project fingerprint
  (hash of: languages + frameworks + domain type + complexity tier)
        |
        v
Compare fingerprint against .agent/data/dna_history.json
        |
  MATCH FOUND (similarity > 70%):
    Report: "This looks like a FastAPI + React project (similar to Project-X)"
    Pre-activate: skills 15, 16 (security, api-design)
    Suggest: workflows 13, 06 (spec-discovery, tdd-guide)
    Surface: top 3 historical failure patterns for this stack
        |
  NO MATCH:
    Store new fingerprint in dna_history.json
    Learn from this session for future projects
        |
        v
User confirms or adjusts the pre-activation
        |
        v
Post-session: update dna_history.json with outcome data
```

---

## Phase 1 — Build the DNA Profiler

### Step 1.1 — Create .agent/data/dna_history.json

Initial state (empty, populated by the profiler over time):

```json
{
  "version": "1.0",
  "profiles": [],
  "last_updated": null
}
```

Add to `.gitignore`:
```
.agent/data/dna_history.json
```

DNA history is personal — it accumulates from YOUR project history and should not
be shared in the repo (it contains project names and personal workflow patterns).

### Step 1.2 — Create .agent/scripts/dna_profiler.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Project DNA Profiler
============================================
Location: .agent/scripts/dna_profiler.py

Fingerprints the current project and matches it against historical profiles
to pre-activate relevant skills, suggest workflows, and surface common failure
patterns from similar past projects.

Usage:
  python .agent/scripts/dna_profiler.py profile        # analyze current project
  python .agent/scripts/dna_profiler.py compare        # compare with history
  python .agent/scripts/dna_profiler.py record --name "my-project"  # record session outcome
  python .agent/scripts/dna_profiler.py history        # list all stored profiles
"""
import argparse
import hashlib
import json
import os
from datetime import datetime
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FLAGS_PATH = os.path.join(BASE, ".agent", "data", "project_flags.json")
DNA_HISTORY = os.path.join(BASE, ".agent", "data", "dna_history.json")

SIMILARITY_THRESHOLD = 0.65  # 65% similarity = "similar project"

# Skill pre-activation map: (languages, frameworks, flags) -> [skills to pre-activate]
STACK_SKILL_MAP = {
    ("python", "fastapi"):    ["15-security-engineering", "16-api-design", "19-performance-profiling"],
    ("python", "django"):     ["15-security-engineering", "16-api-design"],
    ("python",):              ["05-code-synthesis", "17-spec-compliance"],
    ("typescript", "react"):  ["20-stitch-ui", "14-context-engineering"],
    ("typescript", "nextjs"): ["20-stitch-ui", "15-security-engineering", "16-api-design"],
    ("typescript", "nestjs"): ["16-api-design", "15-security-engineering"],
    ("go",):                  ["11-go-agent", "19-performance-profiling"],
    ("rust",):                ["08-rust-agent", "19-performance-profiling"],
    ("typescript",):          ["09-jsts-agent", "14-context-engineering"],
}

# Workflow suggestion map: stack -> [workflows most relevant]
STACK_WORKFLOW_MAP = {
    ("python", "fastapi"):    ["13-spec-discovery", "06-tdd", "18-quality-gate"],
    ("typescript", "react"):  ["05a-build-website", "06-tdd", "13-spec-discovery"],
    ("typescript", "nextjs"): ["05a-build-website", "13-spec-discovery", "18-quality-gate"],
    ("go",):                  ["13-spec-discovery", "06-tdd", "17-debug-session"],
    ("python",):              ["13-spec-discovery", "06-tdd", "07-fix-bugs"],
}

# Flag-based additions
FLAG_ADDITIONS = {
    "IS_SECURITY_SENSITIVE": {
        "skills": ["15-security-engineering"],
        "workflows": ["18-quality-gate"],
        "instincts": ["INSTINCT-006 (RACE_WINDOW_TOCTOU)", "INSTINCT-L004 (UNSAFE_DESERIALIZATION)"]
    },
    "HAS_PAYMENTS": {
        "skills": ["15-security-engineering", "17-spec-compliance"],
        "workflows": ["18-quality-gate"],
        "instincts": ["INSTINCT-L005 (PAYMENT_VALIDATION)"]
    },
    "HAS_CONCURRENCY": {
        "skills": ["19-performance-profiling"],
        "instincts": ["INSTINCT-006 (RACE_WINDOW_TOCTOU)"]
    }
}


def load_flags() -> dict:
    if not os.path.exists(FLAGS_PATH):
        return {}
    with open(FLAGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_history() -> dict:
    if not os.path.exists(DNA_HISTORY):
        return {"version": "1.0", "profiles": [], "last_updated": None}
    with open(DNA_HISTORY, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: dict):
    os.makedirs(os.path.dirname(DNA_HISTORY), exist_ok=True)
    history["last_updated"] = datetime.utcnow().isoformat()
    with open(DNA_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def compute_fingerprint(flags_data: dict) -> dict:
    """Generate a DNA fingerprint from project flag data."""
    flags = flags_data.get("flags", {})
    tech = flags_data.get("tech_stack", {})

    languages = sorted(tech.get("languages", []))
    frameworks = sorted(tech.get("frameworks", []))
    file_counts = flags_data.get("file_counts", {})

    # Complexity tier based on file count
    total_files = file_counts.get("source", 0)
    complexity = "A"  # tiny
    if total_files > 20:   complexity = "B"  # small
    if total_files > 100:  complexity = "C"  # medium
    if total_files > 500:  complexity = "D"  # large
    if total_files > 2000: complexity = "E"  # enterprise

    # Domain type from flags
    domain = "general"
    if flags.get("HAS_PAYMENTS"):           domain = "fintech"
    elif flags.get("IS_SECURITY_SENSITIVE"): domain = "secure-web"
    elif flags.get("IS_FRONTEND_ONLY"):      domain = "frontend"
    elif flags.get("IS_CLI_TOOL"):           domain = "cli-tool"
    elif flags.get("IS_LIBRARY"):            domain = "library"
    elif flags.get("IS_FULLSTACK"):          domain = "fullstack"

    # Generate hash
    hash_input = f"{languages}{frameworks}{domain}{complexity}"
    fingerprint_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    return {
        "hash": fingerprint_hash,
        "languages": languages,
        "frameworks": frameworks,
        "domain": domain,
        "complexity_tier": complexity,
        "active_flags": [k for k, v in flags.items() if v],
        "source_file_count": total_files
    }


def compute_similarity(fp_a: dict, fp_b: dict) -> float:
    """
    Compute similarity between two fingerprints.
    Weighted: languages (40%) + frameworks (30%) + domain (20%) + complexity (10%)
    """
    score = 0.0

    # Language similarity (Jaccard)
    langs_a = set(fp_a.get("languages", []))
    langs_b = set(fp_b.get("languages", []))
    if langs_a or langs_b:
        lang_sim = len(langs_a & langs_b) / len(langs_a | langs_b) if (langs_a | langs_b) else 0
        score += lang_sim * 0.40

    # Framework similarity (Jaccard)
    fw_a = set(fp_a.get("frameworks", []))
    fw_b = set(fp_b.get("frameworks", []))
    if fw_a or fw_b:
        fw_sim = len(fw_a & fw_b) / len(fw_a | fw_b) if (fw_a | fw_b) else 0
        score += fw_sim * 0.30
    else:
        score += 0.15  # partial credit if neither has frameworks

    # Domain match
    if fp_a.get("domain") == fp_b.get("domain"):
        score += 0.20

    # Complexity tier match (adjacent tiers get partial credit)
    tier_a = fp_a.get("complexity_tier", "B")
    tier_b = fp_b.get("complexity_tier", "B")
    if tier_a == tier_b:
        score += 0.10
    elif abs(ord(tier_a) - ord(tier_b)) == 1:
        score += 0.05  # adjacent tier

    return round(score, 3)


def find_best_match(fingerprint: dict, history: dict) -> Optional[dict]:
    """Find the closest historical profile."""
    best_score = 0.0
    best_profile = None

    for profile in history.get("profiles", []):
        score = compute_similarity(fingerprint, profile.get("fingerprint", {}))
        if score > best_score:
            best_score = score
            best_profile = profile

    if best_profile and best_score >= SIMILARITY_THRESHOLD:
        return {"profile": best_profile, "similarity": best_score}
    return None


def get_recommendations(fingerprint: dict) -> dict:
    """Generate skill and workflow recommendations for this stack."""
    languages = tuple(sorted(fingerprint.get("languages", [])))
    frameworks = tuple(sorted(fingerprint.get("frameworks", [])))
    flags = {f: True for f in fingerprint.get("active_flags", [])}

    skills = set()
    workflows = set()
    instincts = set()

    # Stack-based recommendations
    for stack_key, stack_skills in STACK_SKILL_MAP.items():
        if all(s in languages or s in frameworks for s in stack_key):
            skills.update(stack_skills)

    for stack_key, stack_workflows in STACK_WORKFLOW_MAP.items():
        if all(s in languages or s in frameworks for s in stack_key):
            workflows.update(stack_workflows)

    # Flag-based additions
    for flag, additions in FLAG_ADDITIONS.items():
        if flags.get(flag):
            skills.update(additions.get("skills", []))
            workflows.update(additions.get("workflows", []))
            instincts.update(additions.get("instincts", []))

    return {
        "pre_activate_skills": sorted(skills),
        "suggested_workflows": sorted(workflows),
        "relevant_instincts": sorted(instincts)
    }


def profile_project() -> dict:
    """Full profile of the current project."""
    flags_data = load_flags()
    if not flags_data:
        return {"error": "Run /scanner first to generate project flags."}

    fingerprint = compute_fingerprint(flags_data)
    recommendations = get_recommendations(fingerprint)
    history = load_history()
    match = find_best_match(fingerprint, history)

    return {
        "fingerprint": fingerprint,
        "recommendations": recommendations,
        "historical_match": match
    }


def record_profile(project_name: str, outcome_notes: str = ""):
    """Record the current session's project profile to history."""
    flags_data = load_flags()
    if not flags_data:
        print("ERROR: No project flags. Run /scanner first.")
        return

    fingerprint = compute_fingerprint(flags_data)
    recommendations = get_recommendations(fingerprint)
    history = load_history()

    profile = {
        "project_name": project_name,
        "recorded_at": datetime.utcnow().isoformat(),
        "fingerprint": fingerprint,
        "recommendations_used": recommendations,
        "outcome_notes": outcome_notes,
        "session_count": 1
    }

    # Check if similar profile already exists
    match = find_best_match(fingerprint, history)
    if match and match["similarity"] > 0.90:
        # Update existing instead of adding duplicate
        for i, p in enumerate(history["profiles"]):
            if compute_similarity(fingerprint, p["fingerprint"]) > 0.90:
                history["profiles"][i]["session_count"] = p.get("session_count", 0) + 1
                history["profiles"][i]["last_seen"] = datetime.utcnow().isoformat()
                print(f"Updated existing profile: {p['project_name']} (now {history['profiles'][i]['session_count']} sessions)")
                break
    else:
        history["profiles"].append(profile)
        print(f"New profile recorded: {project_name}")

    save_history(history)


def main():
    parser = argparse.ArgumentParser(description="Project DNA Profiler")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("profile", help="Profile current project and show recommendations")
    sub.add_parser("compare", help="Compare current project with history")

    p_record = sub.add_parser("record", help="Record current project to DNA history")
    p_record.add_argument("--name", required=True, help="Project name")
    p_record.add_argument("--notes", default="", help="Outcome notes")

    sub.add_parser("history", help="List all stored profiles")

    args = parser.parse_args()

    if args.cmd == "profile" or args.cmd == "compare":
        result = profile_project()

        if "error" in result:
            print(f"ERROR: {result['error']}")
            return

        fp = result["fingerprint"]
        rec = result["recommendations"]

        print(f"Project DNA Fingerprint: {fp['hash']}")
        print(f"  Languages:   {', '.join(fp['languages']) or 'none detected'}")
        print(f"  Frameworks:  {', '.join(fp['frameworks']) or 'none detected'}")
        print(f"  Domain:      {fp['domain']}")
        print(f"  Complexity:  Tier {fp['complexity_tier']} ({fp['source_file_count']} source files)")
        print()

        if result["historical_match"]:
            match = result["historical_match"]
            p = match["profile"]
            print(f"HISTORICAL MATCH: {p['project_name']} ({match['similarity']:.0%} similar)")
            print(f"  Recorded: {p['recorded_at'][:10]}")
            print(f"  Sessions: {p.get('session_count', 1)}")
            print()

        print("PRE-ACTIVATE SKILLS:")
        for skill in rec["pre_activate_skills"]:
            print(f"  Load: .agent/skills/{skill}.md")

        print("\nSUGGESTED WORKFLOWS:")
        for wf in rec["suggested_workflows"]:
            print(f"  Consider: /{wf.split('-', 1)[-1] if '-' in wf else wf}")

        if rec["relevant_instincts"]:
            print("\nRELEVANT INSTINCTS:")
            for instinct in rec["relevant_instincts"]:
                print(f"  Activate: {instinct}")

    elif args.cmd == "record":
        record_profile(args.name, args.notes)

    elif args.cmd == "history":
        history = load_history()
        profiles = history.get("profiles", [])
        if not profiles:
            print("No profiles recorded yet. Run /scanner then 'dna_profiler.py record --name project-name'")
            return
        print(f"DNA History: {len(profiles)} profiles")
        for p in profiles:
            fp = p.get("fingerprint", {})
            print(f"  {p['project_name']:30s} | {fp.get('domain','?'):15s} | "
                  f"{', '.join(fp.get('languages',[]))[:20]:20s} | "
                  f"{p.get('session_count',1)} sessions")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Phase 2 — Update the Scanner Workflow

### Step 2.1 — Update .agent/workflows/01-scanner.md

After Step 7 (emit project flags), add:

```markdown
### Step 8 — DNA Fingerprint and Historical Comparison
Run the DNA profiler:
  python .agent/scripts/dna_profiler.py profile

If HISTORICAL MATCH found:
  Report to user:
  "This project resembles your past work on [project_name] ([similarity]% similar).
   Pre-activating: [skill list]
   Suggested workflows: [workflow list]"

  Then load the pre-activated skills at session start.

If NO MATCH:
  Report: "New project type detected. Recording DNA fingerprint for future reference."
  Suggest running: python .agent/scripts/dna_profiler.py record --name "[project-name]"

Add to SCAN_REPORT:
## Project DNA
Fingerprint: [hash]
Domain: [domain]
Complexity: Tier [X]
Historical match: [project name or "None"]
Pre-activated skills: [list]
```

---

## Phase 3 — Update DEPLOY.md With DNA Instructions

Add to DEPLOY.md:

```markdown
### Project DNA History
After your first session with any new project, record its DNA profile:
  python .agent/scripts/dna_profiler.py record --name "your-project-name"

Over time, the DNA history builds a map of your project patterns. The system
will automatically pre-activate the right skills when it detects a familiar stack.

View your history:
  python .agent/scripts/dna_profiler.py history
```

---

## Phase 4 — Create the /dna Command

Create `.claude/commands/dna.md`:

```markdown
---
description: Fingerprint the current project and match against historical profiles for auto-configuration
---

Analyze project DNA to pre-activate skills and suggest workflows.

Sub-commands:
  /dna profile   — Analyze current project, show recommendations
  /dna compare   — Compare with historical profiles
  /dna record    — Save this project's profile to history
  /dna history   — List all recorded project profiles

For profile:
  python .agent/scripts/dna_profiler.py profile

For record (run at end of session):
  Ask user: "Project name for DNA history? (used to recognize similar projects later)"
  python .agent/scripts/dna_profiler.py record --name "$USER_RESPONSE"

Always run /dna profile at session start after /scanner.
Always run /dna record at session end for new project types.
```

---

## Phase 5 — Session-End Protocol Update

### Step 5.1 — Update CLAUDE.md Section 10 (Self-Improvement Loop)

Add:

```markdown
### DNA Recording (session end)
If this is a new project type (no historical match from /dna profile at start):
  python .agent/scripts/dna_profiler.py record --name "[project name]"

If this is a known project type:
  No action needed — session count updated automatically.
```

---

## Verification

```bash
# 1. Run /scanner first to generate flags
python .agent/scripts/flag_scanner.py

# 2. Profile the current project
python .agent/scripts/dna_profiler.py profile
# Expected: Fingerprint + recommendations for current stack

# 3. Record the profile
python .agent/scripts/dna_profiler.py record --name "antigravity-agent-os"

# 4. Check history
python .agent/scripts/dna_profiler.py history
# Expected: 1 profile listed

# 5. Run profile again (should find the match at 100%)
python .agent/scripts/dna_profiler.py compare
# Expected: HISTORICAL MATCH: antigravity-agent-os (100% similar)

# 6. Test similarity scoring with modified flags
# Temporarily edit project_flags.json to simulate a different project
# Run: python .agent/scripts/dna_profiler.py compare
# Expected: partial similarity score
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/scripts/dna_profiler.py` | NEW |
| `.agent/data/dna_history.json` | NEW (gitignored) |
| `.claude/commands/dna.md` | NEW |
| `.agent/workflows/01-scanner.md` | UPDATED (Step 8 — DNA fingerprint) |
| `CLAUDE.md` | UPDATED (Section 10 — DNA recording at session end) |
| `DEPLOY.md` | UPDATED (DNA history instructions) |

---

## Learning Resources
- Python hashlib: https://docs.python.org/3/library/hashlib.html
- Jaccard similarity: https://en.wikipedia.org/wiki/Jaccard_index
- scikit-learn (upgrade path for ML-based similarity): https://scikit-learn.org/
- ChromaDB (vector similarity, future upgrade): https://github.com/chroma-core/chroma

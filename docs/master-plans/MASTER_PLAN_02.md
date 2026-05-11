# MASTER PLAN 02 — Human Override Learning System
**Feature:** Git-hook-based capture of human corrections that feeds back into skill improvement
**Priority:** HIGH — closes the feedback loop that makes the system genuinely self-improving
**Estimated effort:** 4–5 days
**Depends on:** MASTER_PLAN_01 (overrides stored in failure_db.py overrides table)
**Unlocks:** The self-improvement loop described in Rule 13 becomes executable

---

## Problem Statement

Right now when the agent writes code or generates a document and you edit it manually,
that correction is invisible to the system. The agent will make the same mistake next
session. Rule 13 says the agent should learn from overrides. But there is no mechanism
to capture what was overridden or how it was corrected.

The fix is a Git pre-commit hook that runs before every commit, detects files that were
modified after an agent produced them, computes the diff, classifies the change magnitude,
and logs the override to the failure database. When the same class of override happens
3+ times, the system proposes a skill update.

This is the difference between an agent that talks about improving and one that actually does.

---

## Architecture Overview

```
Agent produces output (code, markdown, config)
        |
        v
You edit the file manually
        |
        v
You run git add + git commit
        |
        v
.git/hooks/pre-commit fires
        |
        v
override_capture.py runs:
  - Identifies which files were agent-produced (reads .agent/data/agent_outputs.log)
  - Computes diff for each agent-produced file that was modified
  - Classifies change magnitude (trivial/minor/significant/major)
  - Extracts override pattern (what category of change was made)
        |
        v
If magnitude >= minor:
  Logs to failure_db.py overrides table
  Checks promotion threshold
        |
        v
If 3+ overrides of same pattern:
  Proposes skill update in .agent/data/skill_candidates/
  Prints SKILL UPDATE ALERT at commit time
        |
        v
Commit proceeds normally
```

---

## Phase 1 — Agent Output Tracking

Before capturing overrides, the system needs to know which files were agent-produced.
Every time an agent writes a file, it logs that fact.

### Step 1.1 — Create .agent/data/agent_outputs.log

This is an append-only JSONL file:

```jsonl
{"timestamp":"2026-05-09T10:00:00Z","file":"src/auth.ts","agent":"code-reviewer","workflow":"16-feature-development","session":"abc123","content_hash":"sha256hex"}
{"timestamp":"2026-05-09T10:01:00Z","file":"docs/specs/SPEC_auth_00.md","agent":"spec","workflow":"13-spec-discovery","session":"abc123","content_hash":"sha256hex"}
```

Add `.agent/data/agent_outputs.log` to `.gitignore`.

### Step 1.2 — Create .agent/scripts/track_output.py

```python
#!/usr/bin/env python3
"""
Track which files were produced by agents.
Called by every agent/workflow that creates or modifies files.

Usage:
  python .agent/scripts/track_output.py --file src/auth.ts --agent code-reviewer --workflow 16-feature-development
"""
import argparse
import hashlib
import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_PATH = os.path.join(BASE, ".agent", "data", "agent_outputs.log")


def hash_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return "missing"
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def track(filepath: str, agent: str, workflow: str, session: str = "unknown"):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "file": filepath,
        "agent": agent,
        "workflow": workflow,
        "session": session,
        "content_hash": hash_file(os.path.join(BASE, filepath))
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def get_agent_produced_files() -> dict:
    """Returns {filepath: latest_record} for all tracked agent-produced files."""
    if not os.path.exists(LOG_PATH):
        return {}
    produced = {}
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                produced[record["file"]] = record
            except json.JSONDecodeError:
                continue
    return produced


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--workflow", default="unknown")
    parser.add_argument("--session", default="unknown")
    args = parser.parse_args()
    track(args.file, args.agent, args.workflow, args.session)
    print(f"Tracked: {args.file} (agent: {args.agent})")


if __name__ == "__main__":
    main()
```

---

## Phase 2 — Build the Override Capture Script

### Step 2.1 — Create .agent/scripts/override_capture.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Human Override Capture
=============================================
Location: .agent/scripts/override_capture.py

Detects when humans manually edit agent-produced files and logs the
correction pattern to the failure memory database.

Designed to run as a Git pre-commit hook.

Usage:
  python .agent/scripts/override_capture.py          # run as hook
  python .agent/scripts/override_capture.py --report # show override statistics
"""
import argparse
import difflib
import json
import os
import subprocess
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE, ".agent", "scripts"))

try:
    import failure_db
    HAS_FAILURE_DB = True
except ImportError:
    HAS_FAILURE_DB = False


MAGNITUDE_THRESHOLDS = {
    "trivial":     (0, 2),      # 1-2 line changes (typo fixes, formatting)
    "minor":       (3, 10),     # 3-10 line changes (small corrections)
    "significant": (11, 40),    # 11-40 line changes (meaningful rewrites)
    "major":       (41, 9999),  # 40+ line changes (fundamental rethink)
}

OVERRIDE_PATTERNS = {
    "added_error_handling":   ["try", "catch", "except", "finally", "error", "throw"],
    "added_types":            ["type ", ": string", ": number", ": bool", "Optional[", "-> "],
    "simplified_code":        ["removed", "deleted", "shorter", "simpler"],
    "added_comments":         ["#", "//", "/*", "\"\"\"", "'''"],
    "changed_naming":         [],  # detected by proportion of identifier changes
    "structural_change":      ["class ", "def ", "function ", "interface ", "struct "],
    "security_hardening":     ["sanitize", "validate", "escape", "parameterize", "hash"],
    "performance_improvement":["cache", "memo", "index", "batch", "async", "await"],
}


def get_staged_files() -> list[str]:
    """Get files staged for commit using git diff --cached."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True, cwd=BASE
    )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def get_original_content(filepath: str) -> str:
    """Get the original git-tracked content (HEAD version)."""
    result = subprocess.run(
        ["git", "show", f"HEAD:{filepath}"],
        capture_output=True, text=True, cwd=BASE
    )
    if result.returncode != 0:
        return ""  # New file — no original
    return result.stdout


def get_staged_content(filepath: str) -> str:
    """Get the staged (about-to-be-committed) content."""
    result = subprocess.run(
        ["git", "show", f":{filepath}"],
        capture_output=True, text=True, cwd=BASE
    )
    return result.stdout


def compute_diff_stats(original: str, modified: str) -> dict:
    """Compute detailed diff statistics."""
    orig_lines = original.splitlines()
    mod_lines = modified.splitlines()

    diff = list(difflib.unified_diff(orig_lines, mod_lines, lineterm=""))
    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
    total_changed = added + removed

    # Classify magnitude
    magnitude = "trivial"
    for level, (lo, hi) in MAGNITUDE_THRESHOLDS.items():
        if lo <= total_changed <= hi:
            magnitude = level
            break

    return {
        "lines_added": added,
        "lines_removed": removed,
        "total_changed": total_changed,
        "magnitude": magnitude,
        "diff_excerpt": "\n".join(diff[:30])  # first 30 lines of diff
    }


def detect_pattern(diff_text: str, original: str, modified: str) -> list[str]:
    """Classify what kind of override this is."""
    combined = diff_text.lower()
    detected = []
    for pattern, keywords in OVERRIDE_PATTERNS.items():
        if keywords and any(kw in combined for kw in keywords):
            detected.append(pattern)
    if not detected:
        detected.append("general_correction")
    return detected


def run_capture():
    """Main hook logic — runs on git pre-commit."""
    staged_files = get_staged_files()
    if not staged_files:
        sys.exit(0)

    # Load agent-produced file registry
    log_path = os.path.join(BASE, ".agent", "data", "agent_outputs.log")
    agent_produced = {}
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line.strip())
                    agent_produced[r["file"]] = r
                except Exception:
                    continue

    overrides_captured = 0

    for filepath in staged_files:
        if filepath not in agent_produced:
            continue  # Not an agent-produced file — skip

        original = get_original_content(filepath)
        if not original:
            continue  # New file, no original to compare

        modified = get_staged_content(filepath)
        stats = compute_diff_stats(original, modified)

        if stats["magnitude"] == "trivial":
            continue  # Trivial changes not worth logging

        agent_record = agent_produced[filepath]
        patterns = detect_pattern(stats["diff_excerpt"], original, modified)

        print(f"[OVERRIDE DETECTED] {filepath}")
        print(f"  Agent: {agent_record['agent']} | Magnitude: {stats['magnitude']}")
        print(f"  Changed: +{stats['lines_added']} -{stats['lines_removed']} lines")
        print(f"  Pattern: {', '.join(patterns)}")

        if HAS_FAILURE_DB:
            for pattern in patterns:
                failure_db.log_failure(
                    pattern_type=f"human_override:{pattern}",
                    context=f"File: {filepath}, Agent: {agent_record['agent']}",
                    root_cause=f"Agent output required human correction ({stats['magnitude']} change)",
                    fix_applied=f"Human modified: {stats['lines_added']} lines added, {stats['lines_removed']} removed",
                    outcome="resolved",
                    agent_used=agent_record["agent"]
                )
            overrides_captured += 1

    if overrides_captured > 0:
        print(f"\n[MEMORY] {overrides_captured} override(s) logged to failure memory.")
        print("[RUN] python .agent/scripts/failure_db.py summary — to see patterns")

    sys.exit(0)  # Always allow the commit to proceed


def print_report():
    """Print override statistics."""
    if not HAS_FAILURE_DB:
        print("failure_db.py not available")
        return
    s = failure_db.get_summary()
    print(f"Override Summary (last {s['period_days']} days)")
    print(f"  Override-type patterns: checking...")
    results = failure_db.query_similar("human_override", top_n=20)
    overrides = [r for r in results if "human_override" in r.get("pattern_type", "")]
    print(f"  Total overrides captured: {len(overrides)}")
    if s["pending_skill_proposals"] > 0:
        print(f"  Skill proposals pending: {s['pending_skill_proposals']}")
        print("  Run: python .agent/scripts/failure_db.py summary")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    if args.report:
        print_report()
    else:
        run_capture()


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Install the Git Hook

### Step 3.1 — Create the hook installer script

Create `.agent/scripts/install_hooks.py`:

```python
#!/usr/bin/env python3
"""
Install Antigravity Git hooks into .git/hooks/
Run once after cloning or upgrading.
"""
import os
import stat
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOOKS_DIR = os.path.join(BASE, ".git", "hooks")

PRE_COMMIT_CONTENT = """#!/bin/bash
# Antigravity Agent OS — Override Capture Hook
# Installed by: python .agent/scripts/install_hooks.py

PYTHON=$(which python3 || which python)
SCRIPT=".agent/scripts/override_capture.py"

if [ -f "$SCRIPT" ]; then
  $PYTHON "$SCRIPT"
fi

exit 0
"""


def install():
    if not os.path.exists(HOOKS_DIR):
        print(f"ERROR: .git/hooks directory not found at {HOOKS_DIR}")
        print("Are you in the root of a git repository?")
        sys.exit(1)

    hook_path = os.path.join(HOOKS_DIR, "pre-commit")

    if os.path.exists(hook_path):
        with open(hook_path, "r") as f:
            existing = f.read()
        if "override_capture" in existing:
            print("Hook already installed.")
            return
        # Append to existing hook
        with open(hook_path, "a") as f:
            f.write("\n# Antigravity override capture\n")
            f.write('python3 .agent/scripts/override_capture.py\n')
        print(f"Appended to existing pre-commit hook: {hook_path}")
    else:
        with open(hook_path, "w") as f:
            f.write(PRE_COMMIT_CONTENT)
        os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IEXEC)
        print(f"Installed pre-commit hook: {hook_path}")


def main():
    install()
    print("Done. Override capture is now active on every git commit.")
    print("Human corrections to agent-produced files will be logged automatically.")


if __name__ == "__main__":
    main()
```

### Step 3.2 — Add hook installation to DEPLOY.md

In DEPLOY.md, add to the Installation section:

```markdown
### Optional: Override Learning (Recommended)
After setup, install the Git override capture hook:

  python .agent/scripts/install_hooks.py

This hook runs on every `git commit` and logs human corrections to agent-produced
files into the failure memory database. Over time, this builds a pattern library
that improves agent output quality.
```

---

## Phase 4 — Create the /self-improve Command

Create `.claude/commands/self-improve.md`:

```markdown
---
description: Review pending skill promotion proposals from failure memory and integrate accepted ones
---

Run the self-improvement review loop.

STEP 1 — Check pending proposals:
  python .agent/scripts/failure_db.py summary

STEP 2 — Review each pending skill candidate:
  python .agent/scripts/failure_db.py export --output /tmp/failure_review.md
  Read /tmp/failure_review.md

STEP 3 — For each proposal the user accepts:
  Ask: "What should this skill be called?"
  Ask: "Write the skill content or should I draft it from the failure patterns?"

  If drafting:
    Read the failure records for this pattern
    Synthesize: what is the pattern? what is the correct response?
    Draft a new skill file using the standard skill format
    Save to .agent/skills/[next-number]-[skill-name].md

STEP 4 — Update rejection record:
  For proposals the user rejects:
    Log the rejection reason in the skill_candidates table
    The pattern will not be re-proposed for 30 days

STEP 5 — Run /sync-registry to register any new skill files.

STEP 6 — Install hooks if not already installed:
  python .agent/scripts/install_hooks.py
```

---

## Phase 5 — Track Agent Outputs in Workflows

### Step 5.1 — Add tracking calls to key workflows

In `.agent/workflows/16-feature-development.md`, after each code generation step, add:

```markdown
**Track output:** After writing any file, log it:
  python .agent/scripts/track_output.py --file [filepath] --agent [agent-name] --workflow 16-feature-development
```

Add the same tracking call to:
- `13-spec-discovery.md` (tracks SPEC files)
- `05a-build-website.md` (tracks generated code)
- `05b-build-app.md` (tracks generated code)
- `07-fix-bugs.md` (tracks bug fix files)

---

## Phase 6 — Update Rule 13 (Self-Improvement)

### Step 6.1 — Update .agent/rules/13-self-improvement.md

Add a section at the end:

```markdown
## Executable Self-Improvement (v5.0+)

The self-improvement loop is now operational via three scripts:

### Override Capture (automatic)
The .git/hooks/pre-commit hook runs override_capture.py on every commit.
No manual action required. Overrides are logged automatically.

### Failure Memory (manual at session end)
At the end of any debug or fix session, run:
  python .agent/scripts/failure_db.py log --pattern "..." --context "..." --cause "..." --fix "..." --outcome resolved

### Skill Promotion (run /self-improve)
When failure_db reports SKILL PROMOTION ALERT:
  Run /self-improve to review proposals and integrate accepted patterns as new skills.

### Cadence
- After every session: /failure-memory log
- Weekly: /failure-memory summary (integrated into /weekly-review)
- Monthly: /self-improve to process accumulated proposals
```

---

## Verification

```bash
# 1. Install the hook
python .agent/scripts/install_hooks.py
# Expected: "Installed pre-commit hook: .git/hooks/pre-commit"

# 2. Create and track a test file
echo "original content" > /tmp/test_tracked.py
python .agent/scripts/track_output.py --file /tmp/test_tracked.py --agent test --workflow test

# 3. Modify the file and commit
echo "corrected content with error handling" >> /tmp/test_tracked.py
# In a real repo: git add + git commit would trigger the hook

# 4. Run override capture manually
python .agent/scripts/override_capture.py --report
# Expected: Override summary

# 5. Check failure DB has override records
python .agent/scripts/failure_db.py query --keywords "human override"
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/scripts/override_capture.py` | NEW |
| `.agent/scripts/track_output.py` | NEW |
| `.agent/scripts/install_hooks.py` | NEW |
| `.agent/data/agent_outputs.log` | NEW (gitignored) |
| `.claude/commands/self-improve.md` | NEW |
| `.agent/rules/13-self-improvement.md` | UPDATED |
| `.agent/workflows/16-feature-development.md` | UPDATED |
| `DEPLOY.md` | UPDATED |
| `.git/hooks/pre-commit` | INSTALLED |

---

## Learning Resources
- Git hooks guide: https://git-scm.com/docs/githooks
- Python difflib: https://docs.python.org/3/library/difflib.html
- Claude Code hooks (Anthropic): https://docs.anthropic.com/claude-code/hooks
- Python watchdog (filesystem events): https://github.com/gorakhargosh/watchdog

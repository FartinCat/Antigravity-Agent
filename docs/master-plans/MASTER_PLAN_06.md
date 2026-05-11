# MASTER PLAN 06 — Agent Output Caching Engine
**Feature:** Hash-based cache that reuses agent outputs when project files haven't changed
**Priority:** MEDIUM — reduces token cost and latency for repeated operations
**Estimated effort:** 3–4 days
**Depends on:** MASTER_PLAN_03 (flag_scanner.py provides project hash inputs)
**Unlocks:** Plan 09 (DNA fingerprinting reuses the hash infrastructure)

---

## Problem Statement

If you run /scanner at 10am and run it again at 10:05am without changing any project files,
you pay the same token cost twice and wait twice as long. The output would be identical.
This is pure waste.

The same problem applies to: /ag-refresh on an unchanged codebase, the failure-predictor
on files that haven't been modified, the readme-architect on a project with no new content.

Agent output caching invalidates based on file system fingerprinting. If the relevant
input files haven't changed since the last run, the cached output is returned immediately.
This is how build systems (Make, Gradle, Bazel) work — they cache build artifacts and
only rebuild when inputs change. The same principle applies to agent outputs.

No file-based agentic system has implemented this. They all re-run every time.

---

## Architecture Overview

```
Agent command invoked (e.g. /scanner)
        |
        v
agent_cache.py: compute_project_hash()
        |
        v
Check .agent/data/agent_cache.json for existing entry
        |
  CACHE HIT (hash matches + TTL not expired):
    Return cached output path
    Print: "CACHE HIT — returning cached output from [timestamp]"
    Skip agent execution
        |
  CACHE MISS (hash differs OR no entry OR TTL expired):
    Execute agent normally
    Store new output path + hash in cache
    Print: "CACHE MISS — running fresh analysis"
        |
        v
Output delivered to user
```

---

## Phase 1 — Build the Cache Engine

### Step 1.1 — Create .agent/scripts/agent_cache.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Agent Output Cache
==========================================
Location: .agent/scripts/agent_cache.py

Caches agent outputs based on project file hash.
Invalidates when relevant input files change.

Usage:
  python .agent/scripts/agent_cache.py check --agent scanner
  python .agent/scripts/agent_cache.py store --agent scanner --output docs/scan-reports/SCAN_REPORT_03.md
  python .agent/scripts/agent_cache.py invalidate --agent scanner
  python .agent/scripts/agent_cache.py stats
  python .agent/scripts/agent_cache.py clear
"""
import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE_PATH = os.path.join(BASE, ".agent", "data", "agent_cache.json")

# Cache TTL (time-to-live) per agent type in seconds
AGENT_TTL = {
    "scanner":           300,    # 5 min — project structure changes often
    "failure-predictor": 600,    # 10 min — risk analysis
    "market-evaluator":  86400,  # 24 hours — market data changes slowly
    "readme-architect":  3600,   # 1 hour — README generation
    "mcp-auditor":       1800,   # 30 min — MCP config check
    "spec-drift":        3600,   # 1 hour — drift check
    "ag-refresh":        1800,   # 30 min — knowledge base rebuild
    "security-auditor":  0,      # NEVER cache security audits — always fresh
    "default":           300,    # 5 min default
}

# Which file patterns are relevant for each agent's cache invalidation
AGENT_INPUT_PATTERNS = {
    "scanner": [
        "**/*.py", "**/*.ts", "**/*.tsx", "**/*.js", "**/*.go",
        "**/*.rs", "package.json", "pyproject.toml", "Cargo.toml",
        "go.mod", ".gitignore"
    ],
    "failure-predictor": ["**/*.py", "**/*.ts", "**/*.js", "**/*.go"],
    "market-evaluator":  ["README.md", "PROJECT_METADATA.md"],
    "readme-architect":  ["README.md", "**/*.py", "**/*.ts", "package.json"],
    "mcp-auditor":       [".mcp.json", "**/*.json"],
    "spec-drift":        ["docs/specs/**/*.md", "**/*.py", "**/*.ts"],
    "ag-refresh":        ["**/*.py", "**/*.ts", "**/*.md"],
    "default":           ["**/*.py", "**/*.ts", "**/*.js", "**/*.go"]
}

EXCLUDED_DIRS = {
    ".git", ".agent", "node_modules", "__pycache__", ".venv",
    "venv", "archived", "docs", "dist", "build", ".next"
}


def compute_hash(agent_id: str) -> str:
    """
    Compute a hash of the input files relevant to this agent.
    Hash changes when any relevant file is modified.
    """
    patterns = AGENT_INPUT_PATTERNS.get(agent_id, AGENT_INPUT_PATTERNS["default"])
    hasher = hashlib.sha256()

    file_count = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = sorted([d for d in dirs
                          if d not in EXCLUDED_DIRS and not d.startswith(".")])
        for fname in sorted(files):
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, BASE).replace("\\", "/")

            if not _matches_patterns(rel, patterns):
                continue

            try:
                stat = os.stat(filepath)
                # Hash: relative path + size + modification time
                entry = f"{rel}:{stat.st_size}:{int(stat.st_mtime)}"
                hasher.update(entry.encode())
                file_count += 1
            except OSError:
                continue

    # Include file count in hash to detect deletions
    hasher.update(f"count:{file_count}".encode())
    return hasher.hexdigest()[:24]


def _matches_patterns(rel_path: str, patterns: list[str]) -> bool:
    """Simple glob-style pattern matching."""
    import fnmatch
    for pattern in patterns:
        # Handle ** glob
        if "**" in pattern:
            # Split on ** and check if parts match
            parts = pattern.split("**")
            if len(parts) == 2:
                prefix, suffix = parts
                prefix = prefix.rstrip("/")
                suffix = suffix.lstrip("/")
                if prefix and not rel_path.startswith(prefix):
                    continue
                if suffix and not rel_path.endswith(suffix):
                    continue
                return True
        else:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(
                os.path.basename(rel_path), pattern
            ):
                return True
    return False


def load_cache() -> dict:
    if not os.path.exists(CACHE_PATH):
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache: dict):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def check(agent_id: str) -> dict:
    """
    Check if a valid cache entry exists for this agent.
    Returns: {hit: bool, output_path: str|None, age_seconds: int, reason: str}
    """
    # Security auditor is never cached
    if agent_id == "security-auditor":
        return {"hit": False, "output_path": None, "reason": "Security audits are never cached"}

    cache = load_cache()
    entry = cache.get(agent_id)

    if not entry:
        return {"hit": False, "output_path": None, "reason": "No cache entry found"}

    # Check TTL
    ttl = AGENT_TTL.get(agent_id, AGENT_TTL["default"])
    if ttl == 0:
        return {"hit": False, "output_path": None, "reason": "TTL is 0 (never cache)"}

    cached_at = datetime.fromisoformat(entry["cached_at"])
    age_seconds = int((datetime.utcnow() - cached_at).total_seconds())

    if age_seconds > ttl:
        return {
            "hit": False,
            "output_path": None,
            "age_seconds": age_seconds,
            "reason": f"Cache expired (age={age_seconds}s, TTL={ttl}s)"
        }

    # Check input hash
    current_hash = compute_hash(agent_id)
    if current_hash != entry.get("input_hash"):
        return {
            "hit": False,
            "output_path": None,
            "reason": "Input files changed (hash mismatch)"
        }

    # Check output file still exists
    output_path = entry.get("output_path", "")
    if output_path and not os.path.exists(os.path.join(BASE, output_path)):
        return {
            "hit": False,
            "output_path": None,
            "reason": f"Cached output file missing: {output_path}"
        }

    return {
        "hit": True,
        "output_path": output_path,
        "age_seconds": age_seconds,
        "cached_at": entry["cached_at"],
        "reason": f"Cache valid (age={age_seconds}s)"
    }


def store(agent_id: str, output_path: str, metadata: Optional[dict] = None):
    """Store a cache entry for an agent output."""
    cache = load_cache()
    input_hash = compute_hash(agent_id)

    cache[agent_id] = {
        "agent_id": agent_id,
        "cached_at": datetime.utcnow().isoformat(),
        "input_hash": input_hash,
        "output_path": output_path,
        "ttl_seconds": AGENT_TTL.get(agent_id, AGENT_TTL["default"]),
        "metadata": metadata or {}
    }

    save_cache(cache)
    print(f"CACHED: {agent_id} -> {output_path} (hash: {input_hash[:8]}...)")


def invalidate(agent_id: str):
    """Manually invalidate a cache entry."""
    cache = load_cache()
    if agent_id in cache:
        del cache[agent_id]
        save_cache(cache)
        print(f"INVALIDATED: {agent_id}")
    else:
        print(f"No cache entry for: {agent_id}")


def get_stats() -> dict:
    """Return cache statistics."""
    cache = load_cache()
    stats = {"entries": len(cache), "agents": []}

    for agent_id, entry in cache.items():
        cached_at = datetime.fromisoformat(entry["cached_at"])
        age_seconds = int((datetime.utcnow() - cached_at).total_seconds())
        ttl = entry.get("ttl_seconds", 300)
        is_valid = age_seconds <= ttl

        stats["agents"].append({
            "agent": agent_id,
            "age_seconds": age_seconds,
            "ttl": ttl,
            "valid": is_valid,
            "output": entry.get("output_path", "N/A")
        })

    return stats


def main():
    parser = argparse.ArgumentParser(description="Antigravity Agent Output Cache")
    sub = parser.add_subparsers(dest="cmd")

    p_check = sub.add_parser("check")
    p_check.add_argument("--agent", required=True)

    p_store = sub.add_parser("store")
    p_store.add_argument("--agent", required=True)
    p_store.add_argument("--output", required=True)

    p_inv = sub.add_parser("invalidate")
    p_inv.add_argument("--agent", required=True)

    sub.add_parser("stats")
    sub.add_parser("clear")

    args = parser.parse_args()

    if args.cmd == "check":
        result = check(args.agent)
        if result["hit"]:
            print(f"CACHE HIT — {args.agent}")
            print(f"  Output:  {result['output_path']}")
            print(f"  Age:     {result['age_seconds']}s")
            print(f"  Cached:  {result.get('cached_at', 'unknown')}")
        else:
            print(f"CACHE MISS — {args.agent}: {result['reason']}")

    elif args.cmd == "store":
        store(args.agent, args.output)

    elif args.cmd == "invalidate":
        invalidate(args.agent)

    elif args.cmd == "stats":
        stats = get_stats()
        print(f"Agent Cache: {stats['entries']} entries")
        for a in stats["agents"]:
            status = "✓ VALID" if a["valid"] else "✗ EXPIRED"
            print(f"  {a['agent']:25s} {status:12s} age={a['age_seconds']}s TTL={a['ttl']}s")

    elif args.cmd == "clear":
        save_cache({})
        print("Cache cleared.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Phase 2 — Integrate Cache Into Slash Commands

### Step 2.1 — Update .claude/commands/scanner.md

Add at the very beginning, before any other content:

```markdown
## Cache Check (runs first)

Before executing the scan, check if a valid cache exists:
  python .agent/scripts/agent_cache.py check --agent scanner

If CACHE HIT:
  Report: "CACHE HIT — Project unchanged since [cached_at]. Returning cached scan."
  Read and display the cached output file.
  Ask: "Force fresh scan? (yes/no)"
  If yes: continue with full scan. If no: stop here.

If CACHE MISS:
  Continue with full scan below.

## After Scan Completes (runs last)

Store result in cache:
  python .agent/scripts/agent_cache.py store --agent scanner --output docs/scan-reports/SCAN_REPORT_{NN}.md
```

Apply the same cache check pattern to:
- `.claude/commands/ag-refresh.md` (agent: ag-refresh)
- `.claude/commands/web-aesthetics.md` (agent: readme-architect, partial)
- Any workflow that runs the failure-predictor or market-evaluator

### Step 2.2 — Cache-aware commands that NEVER cache

Add to `.claude/agents/security-auditor.md` (Composition Rules):

```markdown
7. Security audit outputs are NEVER cached. Every audit must be fresh.
   The cache engine has TTL=0 for security-auditor — this cannot be overridden.
```

---

## Phase 3 — Create the /cache Command

Create `.claude/commands/cache.md`:

```markdown
---
description: Manage the agent output cache — check status, invalidate entries, or clear all
---

Manage the Antigravity agent output cache.

Sub-commands:
  /cache stats      — Show all cache entries with age and validity
  /cache check      — Check if cache hit for specific agent
  /cache invalidate — Force next run to be fresh for specific agent
  /cache clear      — Clear all cache entries (use after major project changes)

For stats:
  python .agent/scripts/agent_cache.py stats

For check:
  python .agent/scripts/agent_cache.py check --agent $ARGUMENTS

For invalidate:
  python .agent/scripts/agent_cache.py invalidate --agent $ARGUMENTS

For clear:
  Confirm with user first: "Clear ALL cached outputs? This cannot be undone. (yes/no)"
  If yes: python .agent/scripts/agent_cache.py clear

When to use /cache clear:
  - After major refactors that touch many files
  - After switching branches
  - After renaming/moving many files
  - If you suspect cached outputs are stale
```

---

## Phase 4 — Add Cache Stats to Weekly Review

Update `.agent/workflows/20-weekly-review.md`:

```markdown
### Step N — Cache Performance Report
  python .agent/scripts/agent_cache.py stats

Include in weekly review:
- Which agents have valid cached outputs
- Estimated token savings from cache hits this week
  (track cache hits in .agent/data/cache_hits.log if Plan 09 telemetry is implemented)
```

---

## Phase 5 — Add to .gitignore

```
.agent/data/agent_cache.json
```

The cache is local — it depends on local file modification times and local output files.
It must NOT be committed to git.

---

## Phase 6 — Integrate With sync_registry.py

Add to sync_registry.py run sequence:

```python
# Invalidate affected caches when registry changes
cache_script = os.path.join(".agent", "scripts", "agent_cache.py")
if os.path.exists(cache_script):
    # When scanner output changes, invalidate scanner cache
    if "scanner" in changed_components:
        subprocess.run([sys.executable, cache_script, "invalidate", "--agent", "scanner"])
```

---

## Verification

```bash
# 1. Check scanner cache (should be MISS on first run)
python .agent/scripts/agent_cache.py check --agent scanner
# Expected: CACHE MISS — No cache entry found

# 2. Store a fake result
python .agent/scripts/agent_cache.py store --agent scanner --output docs/scan-reports/SCAN_REPORT_00.md
# Expected: CACHED: scanner -> docs/scan-reports/SCAN_REPORT_00.md

# 3. Check again immediately (should be HIT)
python .agent/scripts/agent_cache.py check --agent scanner
# Expected: CACHE HIT with age ~0s

# 4. Modify a source file and check again (should be MISS)
touch src/test_cache_invalidation.py  # or any .py file
python .agent/scripts/agent_cache.py check --agent scanner
# Expected: CACHE MISS — Input files changed

# 5. View stats
python .agent/scripts/agent_cache.py stats

# 6. Test security auditor is never cached
python .agent/scripts/agent_cache.py check --agent security-auditor
# Expected: CACHE MISS — Security audits are never cached

# 7. Clear cache
python .agent/scripts/agent_cache.py clear
python .agent/scripts/agent_cache.py stats
# Expected: Agent Cache: 0 entries
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/scripts/agent_cache.py` | NEW |
| `.agent/data/agent_cache.json` | NEW (gitignored, generated) |
| `.claude/commands/cache.md` | NEW |
| `.claude/commands/scanner.md` | UPDATED (cache check/store added) |
| `.claude/commands/ag-refresh.md` | UPDATED (cache check/store added) |
| `.agent/workflows/20-weekly-review.md` | UPDATED (cache stats step) |
| `.gitignore` | UPDATED |

---

## Learning Resources
- Python hashlib: https://docs.python.org/3/library/hashlib.html
- Build system caching concepts: https://bazel.build/basics/artifact-based-builds
- Make dependency tracking: https://www.gnu.org/software/make/manual/make.html
- Python fnmatch (glob patterns): https://docs.python.org/3/library/fnmatch.html

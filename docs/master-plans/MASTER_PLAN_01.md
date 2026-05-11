# MASTER PLAN 01 — Episodic Failure Memory
**Feature:** SQLite-backed failure database with pattern recognition across sessions
**Priority:** HIGH — makes Rule 13 (self-improvement) real instead of aspirational
**Estimated effort:** 5–7 days
**Depends on:** MASTER_PLAN_00 (typed contracts feed structured data into the DB)
**Unlocks:** Plans 02 (override learning), 07 (intent mapping uses failure history)

---

## Problem Statement

Every agentic session today starts from zero. The agent debugs a null-pointer dereference,
finds the root cause (missing await in async handler), writes the fix. Next week, a different
project has the exact same bug. The agent debugs it again from scratch. Same 15 minutes wasted.

No file-based agentic system has a structured failure database. They have session logs
(like Antigravity's session-context.md) — but those are prose narratives, not queryable
records. You cannot ask session-context.md "have I seen this error pattern before?"

MemGPT (Letta) has long-term memory but it is expensive, cloud-dependent, and requires
their entire framework. This plan builds a local, offline, zero-cost SQLite failure memory
that lives inside .agent/ and requires no external service.

---

## Architecture Overview

```
Bug encountered in session
        |
        v
17-debug-session.md workflow: Step 0 — Query failure_db.py
        |
        v
failure_db.py searches for similar past failures
        |
  FOUND: Return top 3 similar cases with their root causes and fixes
  NOT FOUND: Continue with fresh analysis
        |
        v
Agent resolves bug
        |
        v
17-debug-session.md: Final Step — Log resolution to failure_db.py
        |
        v
failure_db.py checks: Has this pattern appeared 3+ times?
        |
  YES: Propose new skill candidate in .agent/skills/
  NO:  Store record and continue
        |
        v
Weekly review workflow queries failure_db for pattern summary
```

---

## Phase 1 — Create the Data Directory

### Step 1.1 — Create directories

```bash
mkdir -p .agent/data
mkdir -p .agent/data/backups
```

Add to `.gitignore`:
```
.agent/data/failure_memory.db
.agent/data/backups/
```

The database contains project-specific failure history. It should NOT be committed to git
(it's personal/team data, not OS configuration). Add a note in DEPLOY.md:
"The failure memory database (.agent/data/failure_memory.db) is gitignored and local only.
It accumulates over time — do not delete it."

---

## Phase 2 — Build the Failure Memory Database

### Step 2.1 — Create .agent/scripts/failure_db.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Episodic Failure Memory
===============================================
Location: .agent/scripts/failure_db.py

A SQLite-backed database that stores, queries, and promotes recurring failure
patterns. Turns the self-improvement instinct (Rule 13) into executable reality.

Usage:
  python .agent/scripts/failure_db.py log --pattern "null pointer" --context "async handler" --cause "missing await" --fix "add await before call" --outcome resolved
  python .agent/scripts/failure_db.py query --keywords "null pointer async"
  python .agent/scripts/failure_db.py summary
  python .agent/scripts/failure_db.py promote --id 14 --skill-name "async-null-guard"
  python .agent/scripts/failure_db.py export --output docs/audit-reports/FAILURE_SUMMARY_00.md
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE, ".agent", "data", "failure_memory.db")
SKILL_DIR = os.path.join(BASE, ".agent", "skills")

PROMOTION_THRESHOLD = 3   # appearances before skill promotion suggestion
SIMILARITY_THRESHOLD = 0.3  # keyword overlap ratio for "similar" match


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize database schema on first run."""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS failures (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            project     TEXT,
            pattern_type TEXT NOT NULL,
            context     TEXT NOT NULL,
            keywords    TEXT NOT NULL,
            root_cause  TEXT NOT NULL,
            fix_applied TEXT NOT NULL,
            outcome     TEXT NOT NULL CHECK(outcome IN ('resolved','partial','failed')),
            agent_used  TEXT,
            session_id  TEXT,
            promoted    INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS skill_candidates (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            failure_ids     TEXT NOT NULL,
            skill_name      TEXT NOT NULL,
            pattern_summary TEXT NOT NULL,
            proposed_at     TEXT NOT NULL,
            status          TEXT DEFAULT 'proposed'
                CHECK(status IN ('proposed','accepted','rejected','integrated'))
        );

        CREATE TABLE IF NOT EXISTS overrides (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT NOT NULL,
            agent_id        TEXT NOT NULL,
            original_output TEXT NOT NULL,
            corrected_output TEXT NOT NULL,
            diff_summary    TEXT NOT NULL,
            pattern_detected TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_failures_keywords
            ON failures(keywords);

        CREATE INDEX IF NOT EXISTS idx_failures_pattern
            ON failures(pattern_type);

        CREATE INDEX IF NOT EXISTS idx_failures_timestamp
            ON failures(timestamp);
    """)
    conn.commit()
    conn.close()


def extract_keywords(text: str) -> list[str]:
    """
    Simple keyword extraction without external NLP libraries.
    Splits on whitespace, lowercases, removes common stop words,
    keeps tokens >= 4 chars.
    """
    stop_words = {
        'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they',
        'their', 'there', 'when', 'what', 'which', 'into', 'also', 'more',
        'than', 'then', 'some', 'will', 'would', 'could', 'should', 'does',
        'after', 'before', 'during', 'while', 'about', 'because', 'where',
        'error', 'line', 'file', 'code', 'function', 'method', 'class'
    }
    words = text.lower().replace(',', ' ').replace('.', ' ').replace(':', ' ').split()
    return list({w for w in words if len(w) >= 4 and w not in stop_words})


def keyword_similarity(kw_a: list[str], kw_b: list[str]) -> float:
    """Jaccard similarity between two keyword lists."""
    set_a, set_b = set(kw_a), set(kw_b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def log_failure(
    pattern_type: str,
    context: str,
    root_cause: str,
    fix_applied: str,
    outcome: str,
    project: Optional[str] = None,
    agent_used: Optional[str] = None,
    session_id: Optional[str] = None
) -> int:
    """
    Log a new failure resolution to the database.
    Returns the new record ID.
    """
    init_db()
    keywords = extract_keywords(f"{pattern_type} {context} {root_cause}")
    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO failures
            (timestamp, project, pattern_type, context, keywords,
             root_cause, fix_applied, outcome, agent_used, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        project or os.path.basename(BASE),
        pattern_type,
        context,
        json.dumps(keywords),
        root_cause,
        fix_applied,
        outcome,
        agent_used or "unknown",
        session_id or "unknown"
    ))

    new_id = cursor.lastrowid
    conn.commit()

    # Check promotion threshold
    similar_count = _count_similar(conn, keywords, pattern_type)
    if similar_count >= PROMOTION_THRESHOLD:
        _propose_skill_promotion(conn, pattern_type, new_id)

    conn.close()
    return new_id


def query_similar(keywords_text: str, top_n: int = 3) -> list[dict]:
    """
    Query for similar past failures using keyword overlap.
    Returns top_n matches sorted by similarity score.
    """
    init_db()
    query_keywords = extract_keywords(keywords_text)
    conn = get_connection()

    rows = conn.execute("""
        SELECT id, timestamp, pattern_type, context, root_cause,
               fix_applied, outcome, keywords, agent_used
        FROM failures
        WHERE outcome IN ('resolved', 'partial')
        ORDER BY timestamp DESC
        LIMIT 200
    """).fetchall()

    conn.close()

    scored = []
    for row in rows:
        stored_kw = json.loads(row["keywords"])
        score = keyword_similarity(query_keywords, stored_kw)
        if score >= SIMILARITY_THRESHOLD:
            scored.append({
                "id": row["id"],
                "score": round(score, 3),
                "pattern_type": row["pattern_type"],
                "context": row["context"],
                "root_cause": row["root_cause"],
                "fix_applied": row["fix_applied"],
                "outcome": row["outcome"],
                "timestamp": row["timestamp"][:10],
                "agent_used": row["agent_used"]
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def _count_similar(conn: sqlite3.Connection, keywords: list[str], pattern_type: str) -> int:
    rows = conn.execute(
        "SELECT keywords FROM failures WHERE pattern_type = ?", (pattern_type,)
    ).fetchall()
    count = 0
    for row in rows:
        stored = json.loads(row["keywords"])
        if keyword_similarity(keywords, stored) >= SIMILARITY_THRESHOLD:
            count += 1
    return count


def _propose_skill_promotion(conn: sqlite3.Connection, pattern_type: str, triggering_id: int):
    """Propose a new skill when a failure pattern crosses the threshold."""
    existing = conn.execute(
        "SELECT id FROM skill_candidates WHERE pattern_summary LIKE ? AND status = 'proposed'",
        (f"%{pattern_type}%",)
    ).fetchone()

    if existing:
        return  # Already proposed

    skill_name_suggestion = pattern_type.lower().replace(" ", "-")[:40]

    conn.execute("""
        INSERT INTO skill_candidates
            (failure_ids, skill_name, pattern_summary, proposed_at)
        VALUES (?, ?, ?, ?)
    """, (
        str(triggering_id),
        f"auto-{skill_name_suggestion}",
        f"Pattern '{pattern_type}' has appeared {PROMOTION_THRESHOLD}+ times. "
        f"Consider creating a skill to handle it systematically.",
        datetime.utcnow().isoformat()
    ))
    conn.commit()

    print(f"\n[SKILL PROMOTION ALERT]")
    print(f"Pattern '{pattern_type}' has appeared {PROMOTION_THRESHOLD}+ times.")
    print(f"Proposed skill name: auto-{skill_name_suggestion}")
    print(f"Run: python .agent/scripts/failure_db.py promote --id {triggering_id} --skill-name <name>")
    print()


def get_summary(days: int = 30) -> dict:
    """Return a statistical summary of failures in the last N days."""
    init_db()
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM failures WHERE timestamp > ?", (since,)
    ).fetchone()[0]

    resolved = conn.execute(
        "SELECT COUNT(*) FROM failures WHERE timestamp > ? AND outcome = 'resolved'", (since,)
    ).fetchone()[0]

    top_patterns = conn.execute("""
        SELECT pattern_type, COUNT(*) as cnt
        FROM failures
        WHERE timestamp > ?
        GROUP BY pattern_type
        ORDER BY cnt DESC
        LIMIT 5
    """, (since,)).fetchall()

    proposals = conn.execute(
        "SELECT COUNT(*) FROM skill_candidates WHERE status = 'proposed'"
    ).fetchone()[0]

    conn.close()

    return {
        "period_days": days,
        "total_failures": total,
        "resolved": resolved,
        "resolution_rate": f"{(resolved/total*100):.0f}%" if total > 0 else "N/A",
        "top_patterns": [{"pattern": r["pattern_type"], "count": r["cnt"]} for r in top_patterns],
        "pending_skill_proposals": proposals
    }


def export_report(output_path: str):
    """Export a markdown summary report."""
    summary = get_summary()
    init_db()
    conn = get_connection()

    proposals = conn.execute(
        "SELECT * FROM skill_candidates WHERE status = 'proposed'"
    ).fetchall()

    recent = conn.execute("""
        SELECT pattern_type, root_cause, fix_applied, timestamp
        FROM failures
        WHERE outcome = 'resolved'
        ORDER BY timestamp DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    lines = [
        f"# Failure Memory Report",
        f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Period:** Last {summary['period_days']} days",
        "",
        "## Summary",
        f"- Total failures logged: {summary['total_failures']}",
        f"- Resolved: {summary['resolved']} ({summary['resolution_rate']})",
        f"- Pending skill proposals: {summary['pending_skill_proposals']}",
        "",
        "## Top Recurring Patterns",
    ]

    for p in summary["top_patterns"]:
        lines.append(f"- `{p['pattern']}` — {p['count']} occurrences")

    if proposals:
        lines.extend(["", "## Skill Promotion Proposals"])
        for p in proposals:
            lines.append(f"- **{p['skill_name']}**: {p['pattern_summary']}")

    lines.extend(["", "## Recent Resolutions"])
    for r in recent:
        lines.append(f"### {r['pattern_type']} ({r['timestamp'][:10]})")
        lines.append(f"**Root cause:** {r['root_cause']}")
        lines.append(f"**Fix:** {r['fix_applied']}")
        lines.append("")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report written to: {output_path}")


def main():
    init_db()
    parser = argparse.ArgumentParser(description="Antigravity Failure Memory Database")
    sub = parser.add_subparsers(dest="command")

    # log
    p_log = sub.add_parser("log", help="Log a new failure resolution")
    p_log.add_argument("--pattern", required=True)
    p_log.add_argument("--context", required=True)
    p_log.add_argument("--cause", required=True)
    p_log.add_argument("--fix", required=True)
    p_log.add_argument("--outcome", required=True, choices=["resolved", "partial", "failed"])
    p_log.add_argument("--agent", default="unknown")

    # query
    p_query = sub.add_parser("query", help="Find similar past failures")
    p_query.add_argument("--keywords", required=True)
    p_query.add_argument("--top", type=int, default=3)

    # summary
    sub.add_parser("summary", help="Print statistical summary")

    # export
    p_export = sub.add_parser("export", help="Export markdown report")
    p_export.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "log":
        record_id = log_failure(
            args.pattern, args.context, args.cause,
            args.fix, args.outcome, agent_used=args.agent
        )
        print(f"Logged failure #{record_id}: {args.pattern}")

    elif args.command == "query":
        results = query_similar(args.keywords, top_n=args.top)
        if not results:
            print("No similar past failures found.")
        else:
            print(f"Found {len(results)} similar failure(s):\n")
            for r in results:
                print(f"[#{r['id']} | score={r['score']} | {r['timestamp']}]")
                print(f"  Pattern:    {r['pattern_type']}")
                print(f"  Root cause: {r['root_cause']}")
                print(f"  Fix:        {r['fix_applied']}")
                print(f"  Outcome:    {r['outcome']}")
                print()

    elif args.command == "summary":
        s = get_summary()
        print(f"Failure Memory Summary (last {s['period_days']} days)")
        print(f"  Total: {s['total_failures']} | Resolved: {s['resolved']} ({s['resolution_rate']})")
        print(f"  Skill proposals pending: {s['pending_skill_proposals']}")
        if s["top_patterns"]:
            print("  Top patterns:")
            for p in s["top_patterns"]:
                print(f"    {p['pattern']}: {p['count']}x")

    elif args.command == "export":
        export_report(args.output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Integrate Into Debug Workflow

### Step 3.1 — Update .agent/workflows/17-debug-session.md

Add these two steps around the existing content:

**NEW Step 0 — Memory Query (insert BEFORE existing Step 1):**
```markdown
### Step 0 — Query Failure Memory
Before any diagnosis, search for similar past failures:

  python .agent/scripts/failure_db.py query --keywords "[error message + context keywords]"

If results found:
  Report: "MEMORY HIT — Found [N] similar past failure(s):"
  For each result: show pattern, root cause, fix applied, and outcome
  Ask: "Start with the historical fix? (yes/no)"
  If yes: apply the historical fix first, then verify

If no results:
  Continue to Step 1 with fresh analysis.

The purpose of this step is to avoid diagnosing the same bug twice.
```

**NEW Final Step — Log Resolution (insert AFTER existing final step):**
```markdown
### Final Step — Log to Failure Memory
After resolution, log the outcome:

  python .agent/scripts/failure_db.py log \
    --pattern "[error type / pattern name]" \
    --context "[what was happening when bug appeared]" \
    --cause "[root cause identified]" \
    --fix "[exact fix applied]" \
    --outcome "resolved|partial|failed" \
    --agent "[which agent resolved it]"

If the CLI prints a SKILL PROMOTION ALERT:
  Report to user: "This pattern has appeared 3+ times. Recommend creating a skill.
  Run /self-improve to draft the skill candidate."
```

---

## Phase 4 — Integrate Into Weekly Review

### Step 4.1 — Update .agent/workflows/20-weekly-review.md

Add a new step before the final output:

```markdown
### Step N — Failure Memory Report
Generate weekly failure summary:

  python .agent/scripts/failure_db.py summary

Include in the weekly review output:
- Resolution rate for the week
- Top recurring patterns
- Any pending skill promotion proposals

If pending proposals exist:
  "ACTION REQUIRED: [N] failure patterns are ready for skill promotion.
   Run /self-improve to review and integrate them."
```

---

## Phase 5 — Create the /failure-memory Slash Command

Create `.claude/commands/failure-memory.md`:

```markdown
---
description: Query, log, and summarize the episodic failure memory database
---

Interact with the Antigravity failure memory system.

Available sub-commands:
  /failure-memory query [error keywords]   — Find similar past failures
  /failure-memory summary                  — Statistical summary of recent failures
  /failure-memory export                   — Generate markdown failure report
  /failure-memory log                      — Manually log a failure (guided)

For query:
  python .agent/scripts/failure_db.py query --keywords "$ARGUMENTS"

For summary:
  python .agent/scripts/failure_db.py summary

For export:
  Determine next sequence number in docs/audit-reports/
  python .agent/scripts/failure_db.py export --output docs/audit-reports/FAILURE_REPORT_{NN}.md

For log (guided):
  Ask the user for: pattern type, context, root cause, fix applied, outcome
  Then run: python .agent/scripts/failure_db.py log --pattern ... --context ... --cause ... --fix ... --outcome ...
```

---

## Phase 6 — Update sync_registry.py

Add to the disk scan in sync_registry.py:

```python
# Check failure memory database health
db_path = os.path.join(".agent", "data", "failure_memory.db")
if os.path.exists(db_path):
    db_size_kb = os.path.getsize(db_path) / 1024
    print(f"  Failure memory DB: {db_size_kb:.1f} KB")
else:
    print("  Failure memory DB: NOT INITIALIZED (first run will create it)")
```

---

## Verification

```bash
# 1. Initialize and log a test failure
python .agent/scripts/failure_db.py log \
  --pattern "null pointer async" \
  --context "React useEffect with async fetch" \
  --cause "Missing await before data.json() call" \
  --fix "Add await: const data = await response.json()" \
  --outcome resolved
# Expected: "Logged failure #1: null pointer async"

# 2. Query for similar
python .agent/scripts/failure_db.py query --keywords "null pointer async React"
# Expected: Shows failure #1 with similarity score

# 3. Check summary
python .agent/scripts/failure_db.py summary
# Expected: Total 1, Resolved 1 (100%)

# 4. Export report
python .agent/scripts/failure_db.py export --output docs/audit-reports/FAILURE_REPORT_00.md
# Expected: Report file created

# 5. Log 2 more of the same pattern to trigger promotion alert
python .agent/scripts/failure_db.py log --pattern "null pointer async" --context "Vue3 composition API" --cause "Missing await" --fix "Add await" --outcome resolved
python .agent/scripts/failure_db.py log --pattern "null pointer async" --context "Express middleware" --cause "Missing await" --fix "Add await" --outcome resolved
# Expected: SKILL PROMOTION ALERT printed on 3rd occurrence
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/data/failure_memory.db` | NEW (gitignored) |
| `.agent/scripts/failure_db.py` | NEW |
| `.claude/commands/failure-memory.md` | NEW |
| `.agent/workflows/17-debug-session.md` | UPDATED (Step 0 + Final Step) |
| `.agent/workflows/20-weekly-review.md` | UPDATED (failure summary step) |

---

## Learning Resources
- MemGPT / Letta (long-term memory architecture): https://github.com/cpacker/MemGPT
- SQLite full-text search: https://www.sqlite.org/fts5.html
- Case-based reasoning theory: search "case based reasoning AI" on Google Scholar
- Zep structured memory: https://github.com/getzep/zep

# MASTER PLAN 09 — Observable Agent Telemetry Dashboard
**Feature:** JSONL telemetry log + Python dashboard showing agent usage, token cost, and system health
**Priority:** MEDIUM — makes the system legible and measurable; enables data-driven improvement
**Estimated effort:** 4–5 days
**Depends on:** Plans 00-08 (all emit events that telemetry captures)
**Unlocks:** This is the final plan — it surfaces the value of all prior plans in one dashboard

---

## Problem Statement

You have no idea which agents are being called most, how many tokens each workflow
consumes, which rules fire most often, or whether the system is getting better over
time. Every agentic system is a black box. You build it, it runs, you hope it's working.

Without measurement, you cannot improve. You cannot tell if the failure memory database
is saving you time. You cannot tell if the model router is actually reducing costs.
You cannot tell which workflows are used daily versus never used.

This plan adds an append-only telemetry log and a Python dashboard script that
turns raw events into an actionable weekly summary. The dashboard becomes the
"health report" of your entire Antigravity OS.

---

## Architecture Overview

```
Every agent, workflow, and script emits events
        |
        v
.agent/data/telemetry.jsonl  (append-only, gitignored)
        |
        v
telemetry.py aggregates events
        |
        v
/dashboard command runs telemetry.py --report
        |
        v
Terminal dashboard showing:
  - Most used workflows this week
  - Token cost estimate by model
  - Instinct fire rate
  - Cache hit rate
  - Override rate
  - System health trend: GREEN / YELLOW / RED
  - Recommendations: "You haven't used /spec-drift in 14 days"
```

---

## Phase 1 — Define the Event Schema

### Step 1.1 — Telemetry Event Types

Every event written to telemetry.jsonl follows this structure:

```json
{
  "ts":        "2026-05-09T10:00:00Z",
  "event":     "workflow_start",
  "workflow":  "05-spec-discovery",
  "tokens":    800,
  "model":     "claude-sonnet-4-6",
  "session":   "abc123",
  "meta":      {}
}
```

Event type catalog:

| Event | Fields | Emitted by |
|---|---|---|
| `workflow_start` | workflow, tokens_estimate, model | Every workflow start |
| `workflow_end` | workflow, status, artifacts, duration_sec | Every workflow end |
| `agent_invoked` | agent_id, workflow, model | Every agent/persona call |
| `instinct_fired` | instinct_id, instinct_name, fired_at | Rule 03 instinct fires |
| `cache_hit` | agent_id, age_seconds | agent_cache.py hit |
| `cache_miss` | agent_id, reason | agent_cache.py miss |
| `human_override` | agent_id, magnitude, pattern | override_capture.py |
| `failure_logged` | pattern_type, outcome | failure_db.py log |
| `skill_promoted` | skill_name, trigger_count | failure_db.py promotion |
| `model_routed` | task_type, model_chosen, cost_usd | model_router.py |
| `intent_classified` | top_workflow, confidence, redirected | intent_mapper.py |
| `drift_detected` | component, disk_count, registry_count | sync_registry.py |
| `registry_synced` | components_updated | sync_registry.py |
| `validation_passed` | agent_id | validate_output.py |
| `validation_failed` | agent_id, errors, retry_count | validate_output.py |
| `session_start` | project, flags_active | CLAUDE.md boot |
| `session_end` | duration_minutes, tasks_completed | session end |

---

## Phase 2 — Build the Telemetry Engine

### Step 2.1 — Create .agent/scripts/telemetry.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Telemetry Engine
========================================
Location: .agent/scripts/telemetry.py

Records agent events to an append-only JSONL log and generates
dashboard reports showing system health and usage patterns.

Usage:
  python .agent/scripts/telemetry.py emit --event workflow_start --workflow 05-spec-discovery --tokens 800
  python .agent/scripts/telemetry.py emit --event cache_hit --agent scanner
  python .agent/scripts/telemetry.py report                    # full dashboard
  python .agent/scripts/telemetry.py report --days 7           # last 7 days
  python .agent/scripts/telemetry.py export --output docs/audit-reports/TELEMETRY_00.md
  python .agent/scripts/telemetry.py sessions                  # list recent sessions
"""
import argparse
import json
import os
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TELEMETRY_LOG = os.path.join(BASE, ".agent", "data", "telemetry.jsonl")
SESSION_ID_FILE = os.path.join(BASE, ".agent", "data", "current_session.txt")

# Model cost per 1M tokens (input + output)
MODEL_COST = {
    "clara:latest":      0.00,
    "claude-sonnet-4-6": 3.00,
    "claude-opus-4-6":   75.00,
    "unknown":           3.00,  # Assume sonnet if unknown
}


def get_session_id() -> str:
    """Get or create the current session ID."""
    if os.path.exists(SESSION_ID_FILE):
        with open(SESSION_ID_FILE, "r") as f:
            return f.read().strip()
    new_id = str(uuid.uuid4())[:8]
    os.makedirs(os.path.dirname(SESSION_ID_FILE), exist_ok=True)
    with open(SESSION_ID_FILE, "w") as f:
        f.write(new_id)
    return new_id


def new_session():
    """Force a new session ID (call at session start)."""
    new_id = str(uuid.uuid4())[:8]
    os.makedirs(os.path.dirname(SESSION_ID_FILE), exist_ok=True)
    with open(SESSION_ID_FILE, "w") as f:
        f.write(new_id)
    return new_id


def emit(event_type: str, model: str = "unknown", **kwargs) -> dict:
    """Emit a telemetry event."""
    os.makedirs(os.path.dirname(TELEMETRY_LOG), exist_ok=True)
    record = {
        "ts": datetime.utcnow().isoformat(),
        "event": event_type,
        "session": get_session_id(),
        "model": model,
        **kwargs
    }
    with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


def load_events(days: int = 30) -> list[dict]:
    """Load events from the last N days."""
    if not os.path.exists(TELEMETRY_LOG):
        return []
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    events = []
    with open(TELEMETRY_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("ts", "") >= since:
                    events.append(record)
            except json.JSONDecodeError:
                continue
    return events


def compute_stats(events: list[dict]) -> dict:
    """Compute aggregate statistics from events."""
    stats = {
        "total_events": len(events),
        "sessions": set(),
        "workflow_usage": Counter(),
        "agent_usage": Counter(),
        "model_usage": Counter(),
        "token_estimate": defaultdict(int),
        "cache_hits": 0,
        "cache_misses": 0,
        "human_overrides": 0,
        "override_magnitudes": Counter(),
        "instincts_fired": Counter(),
        "failures_logged": 0,
        "skills_promoted": 0,
        "validation_passed": 0,
        "validation_failed": 0,
        "validation_retries": 0,
        "drift_detected": 0,
        "registry_syncs": 0,
        "intent_redirects": 0,
        "cost_by_model": defaultdict(float),
    }

    for event in events:
        ev = event.get("event", "")
        model = event.get("model", "unknown")
        session = event.get("session", "unknown")
        stats["sessions"].add(session)
        stats["model_usage"][model] += 1

        # Token cost
        tokens = event.get("tokens", event.get("tokens_estimate", 0))
        if tokens:
            stats["token_estimate"][model] += tokens
            cost_per_m = MODEL_COST.get(model, MODEL_COST["unknown"])
            stats["cost_by_model"][model] += (tokens / 1_000_000) * cost_per_m

        if ev == "workflow_start":
            workflow = event.get("workflow", "unknown")
            stats["workflow_usage"][workflow] += 1

        elif ev == "agent_invoked":
            stats["agent_usage"][event.get("agent_id", "unknown")] += 1

        elif ev == "cache_hit":
            stats["cache_hits"] += 1

        elif ev == "cache_miss":
            stats["cache_misses"] += 1

        elif ev == "human_override":
            stats["human_overrides"] += 1
            stats["override_magnitudes"][event.get("magnitude", "unknown")] += 1

        elif ev == "instinct_fired":
            stats["instincts_fired"][event.get("instinct_id", "unknown")] += 1

        elif ev == "failure_logged":
            stats["failures_logged"] += 1

        elif ev == "skill_promoted":
            stats["skills_promoted"] += 1

        elif ev == "validation_passed":
            stats["validation_passed"] += 1

        elif ev == "validation_failed":
            stats["validation_failed"] += 1
            stats["validation_retries"] += event.get("retry_count", 0)

        elif ev == "drift_detected":
            stats["drift_detected"] += 1

        elif ev == "registry_synced":
            stats["registry_syncs"] += 1

        elif ev == "intent_classified":
            if event.get("redirected", False):
                stats["intent_redirects"] += 1

    stats["sessions"] = len(stats["sessions"])
    return stats


def compute_health(stats: dict, days: int) -> str:
    """Compute overall system health: GREEN / YELLOW / RED."""
    issues = []

    # Cache performance
    total_cache = stats["cache_hits"] + stats["cache_misses"]
    if total_cache > 10:
        hit_rate = stats["cache_hits"] / total_cache
        if hit_rate < 0.3:
            issues.append("LOW cache hit rate")

    # Override rate (agent quality signal)
    total_agent_calls = sum(stats["agent_usage"].values())
    if total_agent_calls > 5 and stats["human_overrides"] / max(total_agent_calls, 1) > 0.30:
        issues.append("HIGH override rate (agent quality may need improvement)")

    # Validation failures
    total_validations = stats["validation_passed"] + stats["validation_failed"]
    if total_validations > 5 and stats["validation_failed"] / total_validations > 0.20:
        issues.append("HIGH validation failure rate (personas may need schema updates)")

    # Registry drift
    if stats["drift_detected"] > stats["registry_syncs"] * 2:
        issues.append("Registry drift not being resolved promptly")

    if len(issues) == 0:
        return "GREEN"
    elif len(issues) <= 2:
        return "YELLOW"
    else:
        return "RED"


def generate_report(events: list[dict], days: int = 30) -> str:
    """Generate a formatted dashboard report."""
    stats = compute_stats(events)
    health = compute_health(stats, days)
    health_emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}.get(health, "⚪")
    total_cost = sum(stats["cost_by_model"].values())

    lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║        ANTIGRAVITY AGENT OS — TELEMETRY DASHBOARD        ║",
        "╚══════════════════════════════════════════════════════════╝",
        f"Period: Last {days} days  |  Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        f"System Health: {health_emoji} {health}",
        "",
        "━━━ USAGE SUMMARY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"Sessions:        {stats['sessions']}",
        f"Total events:    {stats['total_events']}",
        f"Estimated cost:  ${total_cost:.4f} total",
    ]

    # Cost breakdown
    for model, cost in sorted(stats["cost_by_model"].items(), key=lambda x: -x[1]):
        tokens = stats["token_estimate"].get(model, 0)
        lines.append(f"  {model:35s} ${cost:.4f}  (~{tokens:,} tokens)")

    # Cache performance
    total_cache = stats["cache_hits"] + stats["cache_misses"]
    if total_cache > 0:
        hit_rate = stats["cache_hits"] / total_cache * 100
        lines.extend([
            "",
            "━━━ CACHE PERFORMANCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"Cache hits:      {stats['cache_hits']} ({hit_rate:.0f}% hit rate)",
            f"Cache misses:    {stats['cache_misses']}",
        ])

    # Workflow usage
    if stats["workflow_usage"]:
        lines.extend([
            "",
            "━━━ TOP WORKFLOWS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ])
        for wf, count in stats["workflow_usage"].most_common(8):
            bar = "█" * min(count, 20)
            lines.append(f"  {wf:35s} {bar} {count}")

    # Agent usage
    if stats["agent_usage"]:
        lines.extend([
            "",
            "━━━ TOP AGENTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ])
        for agent, count in stats["agent_usage"].most_common(6):
            lines.append(f"  {agent:35s} {count}x")

    # Quality signals
    lines.extend([
        "",
        "━━━ QUALITY SIGNALS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"Human overrides:  {stats['human_overrides']}",
        f"Failures logged:  {stats['failures_logged']}",
        f"Skills promoted:  {stats['skills_promoted']}",
        f"Validation pass:  {stats['validation_passed']}",
        f"Validation fail:  {stats['validation_failed']}",
        f"Intent redirects: {stats['intent_redirects']} (times user corrected classifier)",
    ])

    # Top instincts
    if stats["instincts_fired"]:
        lines.extend([
            "",
            "━━━ TOP INSTINCTS FIRED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ])
        for instinct, count in stats["instincts_fired"].most_common(5):
            lines.append(f"  {instinct:35s} {count}x")

    # Recommendations
    recommendations = []
    total_agent = sum(stats["agent_usage"].values())
    if total_agent > 0 and stats["human_overrides"] / total_agent > 0.25:
        recommendations.append("Override rate is high — consider running /self-improve to address recurring patterns")
    if stats["skills_promoted"] > 0:
        recommendations.append(f"{stats['skills_promoted']} skill(s) ready for promotion — run /self-improve")
    if stats["drift_detected"] > 5:
        recommendations.append("Frequent registry drift — consider running /sync-registry more often")
    if stats["validation_failed"] > stats["validation_passed"] * 0.15:
        recommendations.append("Validation failure rate elevated — review persona output schemas")

    if recommendations:
        lines.extend(["", "━━━ RECOMMENDATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"])
        for rec in recommendations:
            lines.append(f"  ▸ {rec}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Antigravity Telemetry Engine")
    sub = parser.add_subparsers(dest="cmd")

    p_emit = sub.add_parser("emit", help="Emit a telemetry event")
    p_emit.add_argument("--event", required=True)
    p_emit.add_argument("--model", default="unknown")
    p_emit.add_argument("--workflow")
    p_emit.add_argument("--agent")
    p_emit.add_argument("--tokens", type=int, default=0)
    p_emit.add_argument("--status")
    p_emit.add_argument("--meta", default="{}")

    p_report = sub.add_parser("report", help="Show telemetry dashboard")
    p_report.add_argument("--days", type=int, default=30)

    p_export = sub.add_parser("export", help="Export report to markdown")
    p_export.add_argument("--output", required=True)
    p_export.add_argument("--days", type=int, default=30)

    sub.add_parser("new-session", help="Start a new session (call at Claude Code open)")
    sub.add_parser("stats", help="Quick stats summary")

    args = parser.parse_args()

    if args.cmd == "emit":
        kwargs = {}
        if args.workflow: kwargs["workflow"] = args.workflow
        if args.agent: kwargs["agent_id"] = args.agent
        if args.tokens: kwargs["tokens"] = args.tokens
        if args.status: kwargs["status"] = args.status
        try:
            kwargs["meta"] = json.loads(args.meta)
        except Exception:
            pass
        record = emit(args.event, model=args.model, **kwargs)
        print(f"Event: {record['event']} @ {record['ts'][:19]}")

    elif args.cmd == "report":
        events = load_events(args.days)
        if not events:
            print(f"No telemetry events in last {args.days} days.")
            print("Events are emitted automatically as you use Antigravity commands.")
            return
        print(generate_report(events, args.days))

    elif args.cmd == "export":
        events = load_events(args.days)
        report = generate_report(events, args.days)
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"```\n{report}\n```\n")
        print(f"Report exported to: {args.output}")

    elif args.cmd == "new-session":
        session_id = new_session()
        emit("session_start", session=session_id)
        print(f"New session: {session_id}")

    elif args.cmd == "stats":
        events = load_events(7)  # Last 7 days
        stats = compute_stats(events)
        health = compute_health(stats, 7)
        health_emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}.get(health, "⚪")
        print(f"Health: {health_emoji} {health} | Sessions: {stats['sessions']} | "
              f"Events: {stats['total_events']} | Cost: ${sum(stats['cost_by_model'].values()):.4f}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Integrate Telemetry Across All Scripts

### Step 3.1 — Add telemetry emit calls to existing scripts

For each existing script, add the relevant emit calls:

**sync_registry.py** — add at start and end:
```python
import subprocess, sys
subprocess.run([sys.executable, ".agent/scripts/telemetry.py", "emit",
    "--event", "registry_synced", "--meta", json.dumps({"components": len(changed)})])
```

**agent_cache.py** — add in check():
```python
# After determining hit/miss:
event = "cache_hit" if is_hit else "cache_miss"
subprocess.run([sys.executable, ".agent/scripts/telemetry.py", "emit",
    "--event", event, "--agent", agent_id])
```

**failure_db.py** — add in log_failure():
```python
subprocess.run([sys.executable, ".agent/scripts/telemetry.py", "emit",
    "--event", "failure_logged", "--meta", json.dumps({"outcome": outcome})])
```

**model_router.py** — add in _log_routing():
```python
subprocess.run([sys.executable, ".agent/scripts/telemetry.py", "emit",
    "--event", "model_routed", "--model", decision["model_id"],
    "--meta", json.dumps({"cost": decision["estimated_cost_usd"]})])
```

**validate_output.py** — add after validation:
```python
event = "validation_passed" if is_valid else "validation_failed"
subprocess.run([sys.executable, ".agent/scripts/telemetry.py", "emit",
    "--event", event, "--agent", agent_id])
```

---

## Phase 4 — Create the /dashboard Command

Create `.claude/commands/dashboard.md`:

```markdown
---
description: Show Antigravity system telemetry dashboard — usage, cost, health, quality signals
---

Display the Antigravity OS telemetry dashboard.

Default (last 30 days):
  python .agent/scripts/telemetry.py report

Last 7 days:
  python .agent/scripts/telemetry.py report --days 7

Export to file (for documentation):
  Determine next sequence number in docs/audit-reports/
  python .agent/scripts/telemetry.py export --output docs/audit-reports/TELEMETRY_{NN}.md

Quick health check:
  python .agent/scripts/telemetry.py stats

After displaying: review any RECOMMENDATIONS sections and address them.
If skills_promoted > 0: run /self-improve.
If override rate HIGH: run /self-improve.
```

---

## Phase 5 — Update CLAUDE.md Boot Sequence

### Step 5.1 — Add session telemetry to CLAUDE.md

In CLAUDE.md Section 2 (Boot Sequence), add as Step 0 (before anything else):

```markdown
## 0. Session Telemetry (run first)
Start a new telemetry session:
  python .agent/scripts/telemetry.py new-session

This ensures all subsequent events are grouped under this session ID.
```

In CLAUDE.md Section 10 (Self-Improvement Loop), add:

```markdown
### Session End Telemetry
  python .agent/scripts/telemetry.py emit --event session_end \
    --meta '{"tasks_completed": N}'
```

---

## Phase 6 — Integrate Into Weekly Review

### Step 6.1 — Update .agent/workflows/20-weekly-review.md

Make the dashboard a primary output of the weekly review:

```markdown
### Step 1 — System Telemetry Dashboard (run this FIRST)
  python .agent/scripts/telemetry.py report --days 7

Read the full dashboard output. The health indicator (GREEN/YELLOW/RED)
sets the tone for the rest of the review.

Include the full dashboard output in the WEEKLY_REVIEW_{date}.md file.

If RED: address the top issue before proceeding with other review steps.
If YELLOW: note the issues and add them to next week's priorities.
If GREEN: proceed with normal review.
```

---

## Phase 7 — Add to .gitignore

```
.agent/data/telemetry.jsonl
.agent/data/current_session.txt
```

---

## Verification

```bash
# 1. Emit test events
python .agent/scripts/telemetry.py emit --event workflow_start --workflow 05-spec-discovery --tokens 800 --model claude-sonnet-4-6
python .agent/scripts/telemetry.py emit --event cache_hit --agent scanner
python .agent/scripts/telemetry.py emit --event cache_miss --agent readme-architect --model unknown
python .agent/scripts/telemetry.py emit --event human_override --agent code-reviewer --meta '{"magnitude":"significant"}'
python .agent/scripts/telemetry.py emit --event validation_passed --agent code-reviewer
python .agent/scripts/telemetry.py emit --event instinct_fired --meta '{"instinct_id":"INSTINCT-006","instinct_name":"RACE_WINDOW_TOCTOU"}'

# 2. View the dashboard
python .agent/scripts/telemetry.py report --days 1
# Expected: Full dashboard with all emitted events reflected

# 3. Quick stats
python .agent/scripts/telemetry.py stats
# Expected: One-line health summary

# 4. Export report
python .agent/scripts/telemetry.py export --output docs/audit-reports/TELEMETRY_00.md

# 5. New session
python .agent/scripts/telemetry.py new-session
# Expected: New session ID printed
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/scripts/telemetry.py` | NEW |
| `.agent/data/telemetry.jsonl` | NEW (gitignored) |
| `.agent/data/current_session.txt` | NEW (gitignored) |
| `.claude/commands/dashboard.md` | NEW |
| `CLAUDE.md` | UPDATED (Section 0 session start, Section 10 session end) |
| `.agent/workflows/20-weekly-review.md` | UPDATED (dashboard as Step 1) |
| `.agent/scripts/sync_registry.py` | UPDATED (emit registry_synced) |
| `.agent/scripts/agent_cache.py` | UPDATED (emit cache_hit/miss) |
| `.agent/scripts/failure_db.py` | UPDATED (emit failure_logged) |
| `.agent/scripts/model_router.py` | UPDATED (emit model_routed) |
| `.agent/scripts/validate_output.py` | UPDATED (emit validation events) |
| `.gitignore` | UPDATED |

---

## The Complete Picture — All 10 Plans Together

After all 10 master plans are implemented, the Antigravity Agent OS has:

### Python Script Engine (9 scripts)
| Script | Purpose |
|---|---|
| `sync_registry.py` | Self-maintaining documentation sync |
| `validate_output.py` | Typed agent output validation (Plan 00) |
| `failure_db.py` | Episodic failure memory (Plan 01) |
| `override_capture.py` | Human correction learning (Plan 02) |
| `track_output.py` | Agent output tracking (Plan 02) |
| `install_hooks.py` | Git hook installation (Plan 02) |
| `flag_scanner.py` | Project flag detection (Plan 03) |
| `workflow_composer.py` | Conditional workflow injection (Plan 03) |
| `model_router.py` | Multi-model routing (Plan 04) |
| `spec_drift.py` | Spec-to-implementation drift (Plan 05) |
| `agent_cache.py` | Agent output caching (Plan 06) |
| `intent_mapper.py` | Semantic intent classification (Plan 07) |
| `dna_profiler.py` | Project DNA fingerprinting (Plan 08) |
| `telemetry.py` | Observable telemetry dashboard (Plan 09) |
| `readme_architect.py` | README generation (existing) |

### New Data Files (all gitignored)
`.agent/data/`: failure_memory.db, agent_outputs.log, agent_cache.json,
project_flags.json, workflow_signatures.json, routing_log.jsonl,
intent_log.jsonl, dna_history.json, telemetry.jsonl, current_session.txt

### New Schema Contracts
`.agent/schemas/`: base-output, code-review, security-audit, test-analysis,
ship-decision, project-flags

### New Commands (15 total added across all plans)
validate, failure-memory, self-improve, spec-drift, cache, route-task,
intent, dna, dashboard, sync-registry (plus existing 15 = 30 total commands)

---

## Learning Resources
- JSONL format: https://jsonlines.org/
- Rich Python library (terminal dashboards): https://github.com/Textualize/rich
- OpenTelemetry (enterprise upgrade path): https://opentelemetry.io/
- Prometheus + Grafana (visual dashboard upgrade): https://prometheus.io/
- Python collections.Counter: https://docs.python.org/3/library/collections.html

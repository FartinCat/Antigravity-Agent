# MASTER PLAN 04 — Multi-Model Routing Engine
**Feature:** Intelligent task routing between Clara (local Qwen), Claude Sonnet, and Claude Opus
**Priority:** HIGH — uniquely enabled by your Clara setup, no other public repo can replicate this story
**Estimated effort:** 5–7 days
**Depends on:** MASTER_PLAN_03 (project flags inform routing decisions)
**Unlocks:** Plan 09 (DNA fingerprinting uses routing history)

---

## Problem Statement

You have something genuinely rare: a local fine-tuned model (Clara, Qwen2.5-Coder-3B via
Ollama in WSL) alongside access to Claude Sonnet and Claude Opus. Every other developer
either uses a single commercial model or a single local model. You have both.

The problem: you are currently using them independently, manually deciding which to use.
There is no logic for: "this task is mechanical — use Clara, it's free and fast" or
"this is a high-stakes architecture decision — use Opus, cost justified" or "this contains
proprietary business logic — route to Clara, never send to external API."

The Multi-Model Routing Engine makes this decision automatically based on task type,
cost sensitivity, and privacy requirements. No other file-based agent system has
documented this pattern, because nobody else has both a local fine-tuned model and
commercial API access wired into the same workflow system.

---

## Architecture Overview

```
User invokes a command or workflow
        |
        v
Task classifier reads: task_type, flags, privacy_level
        |
        v
model_router.py consults .agent/rules/24-model-routing.md
        |
        v
Returns: recommended_model, reasoning, fallback_model, estimated_cost
        |
        v
Agent uses recommended model for the task
        |
        v
Result logged to .agent/data/routing_log.jsonl
```

---

## Phase 1 — Create Rule 24

Create `.agent/rules/24-model-routing.md`:

```markdown
---
rule: 24-model-routing
priority: HIGH
---
# Rule 24: Multi-Model Routing

## The Law
Route tasks to the most cost-effective model that meets the quality threshold.
Never route privacy-sensitive data to external APIs without explicit user approval.

## Available Models
| Model | ID | Context | Speed | Cost | Privacy |
|---|---|---|---|---|---|
| Clara (local) | clara:latest | 32k | Fast | Free | Private |
| Claude Sonnet | claude-sonnet-4-6 | 200k | Medium | $$ | External |
| Claude Opus | claude-opus-4-6 | 200k | Slow | $$$$ | External |

## The Routing Matrix

### Route to Clara (local, free, private)
- Registry synchronization (sync_registry.py output explanation)
- File counting, BOM detection, encoding fixes
- Simple git operations and commit message formatting
- Boilerplate code generation (CRUD endpoints, test scaffolding)
- Format conversion (JSON → CSV, markdown formatting)
- Quick syntax checks and linting explanations
- Changelog entry generation from git diff
- README section updates (badges, installation commands)
- ANY task flagged IS_PROPRIETARY (see below)

### Route to Claude Sonnet
- Code generation for non-trivial logic (>50 lines or complex algorithms)
- Bug root-cause analysis (initial investigation)
- Spec writing and requirement clarification
- Code review (single-pass, non-critical paths)
- Research synthesis from web sources
- Test case generation for known patterns
- Documentation writing for public APIs
- Architecture proposals (medium complexity)

### Route to Claude Opus
- Architecture decisions with long-term implications
- Security audit (always — never downgrade)
- Complex debugging with multiple interacting systems
- Spec review for payment/auth/compliance systems
- Cross-system refactoring proposals
- Novel algorithm design
- Ambiguous requirements that need nuanced interpretation
- ANY task where IS_SECURITY_SENSITIVE flag is set AND code will touch production

## Privacy Routing
The following automatically routes to Clara regardless of task complexity:
- Files containing: api_key, private_key, SECRET_, PASSWORD_, PRIVATE_
- Files in: /secrets/, /credentials/, /certs/, .env files
- Proprietary business logic (user explicitly sets IS_PROPRIETARY)
- Internal company data (database dumps, user lists, financial records)

## Override Protocol
User can override routing with explicit intent:
  "Use Opus for this" → forces Opus regardless of matrix
  "Use Clara" → forces local model regardless of complexity
  "Use Sonnet" → forces Sonnet

## Cost Awareness
Before routing to Opus for tasks >5000 tokens estimated input:
  Report: "This task will use Claude Opus (~$X estimated). Proceed? (yes/sonnet/clara)"
  Default timeout: proceed with Sonnet if no response within 10s.
```

---

## Phase 2 — Build the Model Router

### Step 2.1 — Create .agent/scripts/model_router.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Multi-Model Router
==========================================
Location: .agent/scripts/model_router.py

Routes tasks to the appropriate AI model based on task type, complexity,
and privacy requirements.

Usage:
  python .agent/scripts/model_router.py --task "debug async race condition" --tokens 2000
  python .agent/scripts/model_router.py --task "format changelog entry" --tokens 200
  python .agent/scripts/model_router.py --task "security audit auth module" --tokens 5000
  python .agent/scripts/model_router.py --classify "write unit tests for login function"
"""
import argparse
import json
import os
from datetime import datetime
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FLAGS_PATH = os.path.join(BASE, ".agent", "data", "project_flags.json")
ROUTING_LOG = os.path.join(BASE, ".agent", "data", "routing_log.jsonl")

# Model identifiers
CLARA = "clara:latest"          # local Ollama
SONNET = "claude-sonnet-4-6"    # Claude Sonnet
OPUS = "claude-opus-4-6"        # Claude Opus

# Approximate cost per 1M tokens (input+output combined) in USD
MODEL_COST = {
    CLARA:  0.00,
    SONNET: 3.00,
    OPUS:   75.00,
}

# Task classification: keywords → (model, reasoning)
TASK_ROUTES = {
    # CLARA routes — mechanical, formatting, boilerplate
    "clara": {
        "keywords": [
            "format", "lint", "bom", "encoding", "sync registry", "count files",
            "changelog entry", "badge", "gitignore", "readme badge", "rename",
            "move file", "create directory", "generate uuid", "timestamp",
            "sort imports", "trailing whitespace", "conventional commit"
        ],
        "reasoning": "Mechanical task — Clara handles this free and fast"
    },
    # SONNET routes — standard development tasks
    "sonnet": {
        "keywords": [
            "write code", "implement", "generate", "test case", "unit test",
            "spec", "requirement", "documentation", "api docs", "research",
            "explain", "summarize", "refactor", "review code", "debug",
            "bug fix", "feature", "endpoint", "component", "migration"
        ],
        "reasoning": "Standard development task — Sonnet provides good quality/cost ratio"
    },
    # OPUS routes — high-stakes, complex, or sensitive
    "opus": {
        "keywords": [
            "security audit", "architecture", "design system", "threat model",
            "performance optimization complex", "critical bug production",
            "payment", "auth system", "oauth", "cryptography", "compliance",
            "hipaa", "pci", "gdpr", "novel algorithm", "distributed system"
        ],
        "reasoning": "High-stakes task requiring maximum reasoning capability"
    }
}

# Privacy-sensitive keywords that force local routing
PRIVACY_KEYWORDS = [
    "api_key", "secret_key", "private_key", "password", "credential",
    "access_token", "refresh_token", "database_url", "connection_string",
    "proprietary", "confidential", "internal only", "trade secret"
]


def load_project_flags() -> dict:
    if not os.path.exists(FLAGS_PATH):
        return {}
    with open(FLAGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flags", {})


def is_privacy_sensitive(task_description: str) -> bool:
    task_lower = task_description.lower()
    return any(kw in task_lower for kw in PRIVACY_KEYWORDS)


def classify_task(task_description: str) -> str:
    """Classify task into: clara, sonnet, or opus."""
    task_lower = task_description.lower()

    # Privacy check always overrides
    if is_privacy_sensitive(task_lower):
        return "clara"

    # Check opus first (highest priority keywords)
    for kw in TASK_ROUTES["opus"]["keywords"]:
        if kw in task_lower:
            return "opus"

    # Check clara (mechanical tasks)
    for kw in TASK_ROUTES["clara"]["keywords"]:
        if kw in task_lower:
            return "clara"

    # Default to sonnet
    return "sonnet"


def estimate_cost(model: str, token_count: int) -> float:
    cost_per_million = MODEL_COST.get(model, 0)
    return (token_count / 1_000_000) * cost_per_million


def route(task_description: str, estimated_tokens: int = 1000,
          user_override: Optional[str] = None) -> dict:
    """
    Main routing function. Returns routing decision.
    """
    flags = load_project_flags()

    # User override takes priority
    if user_override:
        model_map = {"clara": CLARA, "sonnet": SONNET, "opus": OPUS}
        chosen = model_map.get(user_override.lower(), SONNET)
        result = {
            "model": chosen,
            "model_id": chosen,
            "reasoning": f"User override: '{user_override}'",
            "fallback": SONNET if chosen == OPUS else CLARA,
            "estimated_cost_usd": estimate_cost(chosen, estimated_tokens),
            "privacy_sensitive": is_privacy_sensitive(task_description),
            "token_estimate": estimated_tokens
        }
        _log_routing(task_description, result)
        return result

    # Flag-based overrides
    if flags.get("IS_SECURITY_SENSITIVE") and "security" in task_description.lower():
        tier = "opus"
    elif is_privacy_sensitive(task_description):
        tier = "clara"
    else:
        tier = classify_task(task_description)

    model_map = {"clara": CLARA, "sonnet": SONNET, "opus": OPUS}
    model = model_map[tier]
    cost = estimate_cost(model, estimated_tokens)

    # Cost warning for Opus
    warning = None
    if model == OPUS and cost > 0.10:  # >$0.10 triggers warning
        warning = f"Opus estimated cost: ${cost:.3f}. Consider using Sonnet instead."

    result = {
        "model": tier,
        "model_id": model,
        "reasoning": TASK_ROUTES.get(tier, {}).get("reasoning", "Default routing"),
        "fallback": SONNET if tier == "opus" else CLARA,
        "estimated_cost_usd": cost,
        "privacy_sensitive": is_privacy_sensitive(task_description),
        "token_estimate": estimated_tokens,
        "warning": warning
    }

    _log_routing(task_description, result)
    return result


def _log_routing(task: str, decision: dict):
    """Append routing decision to log."""
    os.makedirs(os.path.dirname(ROUTING_LOG), exist_ok=True)
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "task_summary": task[:100],
        "model": decision["model"],
        "cost": decision["estimated_cost_usd"],
        "privacy": decision["privacy_sensitive"]
    }
    with open(ROUTING_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def routing_summary(days: int = 30) -> dict:
    """Summarize routing decisions from the log."""
    if not os.path.exists(ROUTING_LOG):
        return {"error": "No routing log found. Run some commands first."}

    from datetime import timedelta
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()

    counts = {"clara": 0, "sonnet": 0, "opus": 0}
    total_cost = 0.0
    clara_savings = 0.0

    with open(ROUTING_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line.strip())
                if r["timestamp"] < since:
                    continue
                model = r.get("model", "sonnet")
                counts[model] = counts.get(model, 0) + 1
                total_cost += r.get("cost", 0)
                # What sonnet would have cost if we used it instead of clara
                if model == "clara":
                    clara_savings += estimate_cost(SONNET, 1000)
            except Exception:
                continue

    return {
        "period_days": days,
        "model_usage": counts,
        "total_cost_usd": round(total_cost, 4),
        "estimated_clara_savings_usd": round(clara_savings, 4),
        "total_routed": sum(counts.values())
    }


def main():
    parser = argparse.ArgumentParser(description="Antigravity Multi-Model Router")
    sub = parser.add_subparsers(dest="cmd")

    p_route = sub.add_parser("route", help="Route a task to the best model")
    p_route.add_argument("--task", required=True)
    p_route.add_argument("--tokens", type=int, default=1000)
    p_route.add_argument("--override", help="Force a specific model: clara/sonnet/opus")

    p_classify = sub.add_parser("classify", help="Just classify without full routing logic")
    p_classify.add_argument("--task", required=True)

    sub.add_parser("summary", help="Show routing statistics")

    args = parser.parse_args()

    if args.cmd == "route":
        decision = route(args.task, args.tokens, args.override)
        print(f"Recommended model:  {decision['model'].upper()} ({decision['model_id']})")
        print(f"Reasoning:          {decision['reasoning']}")
        print(f"Fallback:           {decision['fallback']}")
        print(f"Estimated cost:     ${decision['estimated_cost_usd']:.4f}")
        print(f"Privacy sensitive:  {decision['privacy_sensitive']}")
        if decision.get("warning"):
            print(f"WARNING:            {decision['warning']}")

    elif args.cmd == "classify":
        tier = classify_task(args.task)
        print(f"Task classification: {tier.upper()}")

    elif args.cmd == "summary":
        s = routing_summary()
        print(f"Model Routing Summary (last {s['period_days']} days)")
        print(f"  Clara (local): {s['model_usage'].get('clara', 0)} tasks (FREE)")
        print(f"  Sonnet:        {s['model_usage'].get('sonnet', 0)} tasks")
        print(f"  Opus:          {s['model_usage'].get('opus', 0)} tasks")
        print(f"  Total API cost: ${s['total_cost_usd']}")
        print(f"  Saved by Clara: ~${s['estimated_clara_savings_usd']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Create the /route-task Command

Create `.claude/commands/route-task.md`:

```markdown
---
description: Suggest which AI model to use for the current task based on complexity, privacy, and cost
---

Before starting any substantial task, run the router to get the optimal model recommendation.

Usage:
  /route-task [description of what you're about to do]

Execution:
  python .agent/scripts/model_router.py route \
    --task "$ARGUMENTS" \
    --tokens [estimate tokens needed]

After routing decision is returned:
  Display: "Using [MODEL] for this task. Reason: [reasoning]"
  If WARNING is present: show it and ask user to confirm

Special cases:
  If user says "use Clara" → add --override clara
  If user says "use Opus" → add --override opus
  If IS_SECURITY_SENSITIVE flag is set → always confirm before using external model

Show routing summary after 10+ tasks:
  python .agent/scripts/model_router.py summary
```

---

## Phase 4 — Integrate Into CLAUDE.md

### Step 4.1 — Add to CLAUDE.md Section 7 (Workflow Auto-Detection)

Add after the existing auto-detection table:

```markdown
### Model Routing (automatic)
Before any substantial task, consult the model router:
  python .agent/scripts/model_router.py route --task "[brief task description]"

Quick reference:
- Mechanical tasks (format, rename, sync) → Clara (local, free)
- Standard development (code, tests, docs) → Sonnet
- High-stakes (security, architecture, payments) → Opus
- ANY private/proprietary data → Clara (never external)

Clara requires Ollama running in WSL:
  ollama serve  (in WSL terminal)
  ollama list   (verify clara:latest is loaded)
```

---

## Phase 5 — Update .agent/data to gitignore routing log

Add to `.gitignore`:
```
.agent/data/routing_log.jsonl
.agent/data/project_flags.json
.agent/data/failure_memory.db
.agent/data/agent_outputs.log
.agent/data/backups/
```

---

## Phase 6 — Weekly Cost Report in /weekly-review

Update `.agent/workflows/20-weekly-review.md` to include:

```markdown
### Step N — Model Routing Cost Report
  python .agent/scripts/model_router.py summary

Include in weekly review:
- Total API cost this week
- How many tasks routed to Clara (cost savings)
- Any tasks that could have been Clara but used Sonnet/Opus
```

---

## Verification

```bash
# 1. Basic routing
python .agent/scripts/model_router.py route --task "format the changelog entry"
# Expected: CLARA recommended

python .agent/scripts/model_router.py route --task "perform security audit on auth module"
# Expected: OPUS recommended

python .agent/scripts/model_router.py route --task "write unit tests for login function" --tokens 2000
# Expected: SONNET recommended

# 2. Privacy detection
python .agent/scripts/model_router.py route --task "update the api_key configuration file"
# Expected: CLARA (privacy sensitive)

# 3. Classification only
python .agent/scripts/model_router.py classify --task "complex distributed system architecture review"
# Expected: opus

# 4. Summary (after some routing)
python .agent/scripts/model_router.py summary
# Expected: Usage breakdown and cost estimate

# 5. User override
python .agent/scripts/model_router.py route --task "any task" --override clara
# Expected: CLARA regardless of classification
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/rules/24-model-routing.md` | NEW |
| `.agent/scripts/model_router.py` | NEW |
| `.agent/data/routing_log.jsonl` | NEW (gitignored) |
| `.claude/commands/route-task.md` | NEW |
| `CLAUDE.md` | UPDATED (Section 7) |
| `.agent/workflows/20-weekly-review.md` | UPDATED |
| `.gitignore` | UPDATED |

---

## Learning Resources
- litellm (unified LLM API): https://github.com/BerriAI/litellm
- FrugalGPT paper (model cascading): https://arxiv.org/abs/2305.05176
- Ollama API docs: https://github.com/ollama/ollama/blob/main/docs/api.md
- Clara fine-tuning reference: your existing D:\Claude\Clara\ project

# MASTER PLAN 07 — Semantic Intent Mapping With Confidence Scores
**Feature:** Natural language task classification that outputs ranked workflow candidates
**Priority:** MEDIUM — replaces brittle keyword matching with probabilistic routing
**Estimated effort:** 4–5 days
**Depends on:** MASTER_PLAN_01 (failure history improves intent scoring)
**Unlocks:** Makes CLAUDE.md Section 7 auto-detection dramatically more accurate

---

## Problem Statement

The current auto-detection in CLAUDE.md Section 7 is keyword matching. The rules say:
"User says 'fix bug' → run /antibug." But "I noticed the API is returning 500 errors
on authenticated endpoints after the last deploy" does not contain "fix" or "bug" — it
contains "API", "500 errors", "authenticated", "endpoints", "after deploy". The correct
response is security-auditor + antibug + test-engineer. The keyword system misses this.

Even worse: "I need to build the login page" could be /spec (new feature), /build-web
(implementation), or /web-aesthetics (design review) depending on project state. Keyword
matching picks one arbitrarily. Confidence scoring surfaces all three with probabilities
so the user can confirm.

This plan builds intent_mapper.py — a probabilistic classifier that:
1. Takes natural language input
2. Scores it against workflow signatures
3. Returns ranked candidates with confidence percentages
4. Incorporates failure history to improve scores over time

---

## Architecture Overview

```
User types: "I noticed the auth endpoint is throwing 500 errors"
        |
        v
intent_mapper.py classifies the input
  - keyword overlap scoring (40% weight)
  - context signal scoring (40% weight)
  - historical success rate from failure_db (20% weight)
        |
        v
Returns ranked candidates:
  /antibug        (68%) — error pattern in auth context
  /security-auditor (24%) — auth + 500 errors combination
  /quality-gate   (8%)  — general code quality implied
        |
        v
Agent reports: "Interpreting your request as /antibug (68%).
                Say 'redirect to [command]' to change."
        |
        v
Proceeds with top candidate
        |
        v
On session end: log which interpretation was correct to failure_db
(improves future scoring via historical weight)
```

---

## Phase 1 — Define Workflow Signatures

### Step 1.1 — Create .agent/data/workflow_signatures.json

```json
{
  "version": "1.0",
  "generated": "2026-05-09",
  "signatures": {
    "/spec": {
      "description": "Write a structured specification before coding",
      "primary_keywords": ["new feature", "want to build", "design", "spec", "requirements", "plan", "need a", "create a system"],
      "context_signals": ["no existing code", "beginning of project", "discovery phase"],
      "anti_keywords": ["bug", "error", "fix", "broken", "failing"],
      "typical_input_length": "medium",
      "triggers_on": ["creation intent", "planning intent"]
    },
    "/plan": {
      "description": "Break spec into tasks with acceptance criteria",
      "primary_keywords": ["plan", "task list", "breakdown", "steps", "what do i need to do", "how should i", "sequence"],
      "context_signals": ["SPEC.md exists", "post-spec"],
      "anti_keywords": ["bug", "error", "urgent"],
      "triggers_on": ["planning intent", "decomposition intent"]
    },
    "/impl": {
      "description": "Implement next task with TDD",
      "primary_keywords": ["implement", "build", "code", "write the", "create the", "add the", "develop"],
      "context_signals": ["plan exists", "task list ready", "next task"],
      "anti_keywords": ["spec", "plan", "design"],
      "triggers_on": ["implementation intent"]
    },
    "/antibug": {
      "description": "Deep root-cause debugging",
      "primary_keywords": ["bug", "error", "broken", "fails", "crash", "exception", "not working", "wrong output", "unexpected", "500", "null", "undefined", "traceback"],
      "context_signals": ["error message present", "stack trace present", "regression"],
      "anti_keywords": ["new feature", "build", "design"],
      "triggers_on": ["debugging intent", "error presence"]
    },
    "/security-auditor": {
      "description": "OWASP security vulnerability review",
      "primary_keywords": ["security", "vulnerability", "auth", "authentication", "injection", "xss", "csrf", "exposed", "breach", "hack", "token", "credential"],
      "context_signals": ["HAS_AUTH flag", "payment code", "user data handling", "500 on auth endpoint"],
      "anti_keywords": ["new feature", "performance", "ui"],
      "triggers_on": ["security concern", "auth issue"]
    },
    "/ship": {
      "description": "Parallel fan-out review before merge/deploy",
      "primary_keywords": ["ship", "deploy", "release", "merge", "pull request", "pr", "ready to", "done with", "finish", "complete"],
      "context_signals": ["feature complete", "tests passing", "ready for review"],
      "anti_keywords": ["bug", "error", "broken"],
      "triggers_on": ["release intent", "completion signal"]
    },
    "/web-aesthetics": {
      "description": "UI/UX audit and visual upgrade",
      "primary_keywords": ["ui", "design", "looks", "styling", "css", "visual", "layout", "color", "font", "responsive", "mobile", "ugly", "improve the design"],
      "context_signals": ["frontend project", "IS_FRONTEND_ONLY flag", "design feedback"],
      "anti_keywords": ["bug", "security", "database"],
      "triggers_on": ["design intent", "visual concern"]
    },
    "/quality-gate": {
      "description": "Pre-merge quality checklist: lint, types, tests, security",
      "primary_keywords": ["quality", "check", "lint", "type check", "coverage", "before merge", "code quality", "pre-commit", "clean up"],
      "context_signals": ["pre-merge", "CI failing", "code review requested"],
      "anti_keywords": ["new feature", "design"],
      "triggers_on": ["quality concern", "pre-merge intent"]
    },
    "/scanner": {
      "description": "Map the repository before starting work",
      "primary_keywords": ["scan", "analyze project", "what is this", "understand the code", "new project", "onboard", "explore"],
      "context_signals": ["first session", "new repository"],
      "anti_keywords": ["bug", "feature", "design"],
      "triggers_on": ["exploration intent", "first-time analysis"]
    },
    "/tdd-guide": {
      "description": "Strict Red-Green-Refactor test-driven development",
      "primary_keywords": ["test", "tdd", "test first", "write tests", "test driven", "red green", "unit test", "coverage"],
      "context_signals": ["no tests exist", "test coverage low"],
      "anti_keywords": ["bug", "deploy", "design"],
      "triggers_on": ["testing intent", "TDD workflow"]
    },
    "/auto-commit": {
      "description": "Semantic git commit from staged changes",
      "primary_keywords": ["commit", "save", "git", "check in", "push", "stage"],
      "context_signals": ["files modified", "git status has changes"],
      "anti_keywords": ["deploy", "review"],
      "triggers_on": ["commit intent"]
    },
    "/failure-memory": {
      "description": "Query past failure patterns",
      "primary_keywords": ["seen this before", "similar error", "past failures", "history", "remember", "last time"],
      "context_signals": ["recurring error", "second time debugging"],
      "triggers_on": ["memory query intent"]
    }
  }
}
```

---

## Phase 2 — Build the Intent Mapper

### Step 2.1 — Create .agent/scripts/intent_mapper.py

```python
#!/usr/bin/env python3
"""
Antigravity Agent OS — Semantic Intent Mapper
=============================================
Location: .agent/scripts/intent_mapper.py

Classifies natural language task descriptions into workflow candidates
with confidence scores. Replaces brittle keyword matching with probabilistic
routing that improves over time via failure memory integration.

Usage:
  python .agent/scripts/intent_mapper.py "I noticed the auth endpoint is returning 500 errors"
  python .agent/scripts/intent_mapper.py "build the login page" --top 3
  python .agent/scripts/intent_mapper.py "commit my changes" --threshold 0.3
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIGNATURES_PATH = os.path.join(BASE, ".agent", "data", "workflow_signatures.json")
FLAGS_PATH = os.path.join(BASE, ".agent", "data", "project_flags.json")
INTENT_LOG = os.path.join(BASE, ".agent", "data", "intent_log.jsonl")

# Scoring weights
WEIGHT_KEYWORD = 0.40
WEIGHT_CONTEXT = 0.40
WEIGHT_HISTORY = 0.20

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "will", "with", "that",
    "this", "for", "and", "or", "not", "but", "when", "then", "so", "i",
    "my", "me", "we", "our", "you", "your", "it", "its", "be", "been",
    "have", "has", "had", "do", "does", "did", "can", "could", "would",
    "should", "may", "might", "just", "also", "need", "want", "like"
}


def tokenize(text: str) -> list[str]:
    """Lowercase, remove punctuation, split into meaningful tokens."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) >= 3]


def keyword_score(user_tokens: list[str], signature: dict) -> float:
    """
    Score based on keyword overlap between user input and workflow signature.
    Primary keywords score higher than general presence.
    Anti-keywords reduce the score.
    """
    if not user_tokens:
        return 0.0

    user_set = set(user_tokens)
    user_text = " ".join(user_tokens)

    score = 0.0

    # Primary keyword matches (exact phrase or token match)
    primary_kw = signature.get("primary_keywords", [])
    primary_hits = 0
    for kw in primary_kw:
        kw_lower = kw.lower()
        if kw_lower in user_text:
            primary_hits += 1
        elif any(t in user_set for t in kw_lower.split()):
            primary_hits += 0.5

    if primary_kw:
        score = min(primary_hits / len(primary_kw), 1.0)

    # Anti-keyword penalty
    anti_kw = signature.get("anti_keywords", [])
    for kw in anti_kw:
        if kw.lower() in user_text:
            score *= 0.3  # Heavy penalty for anti-keywords

    return score


def context_score(signature: dict, flags: dict) -> float:
    """
    Score based on project context flags matching signature context signals.
    """
    context_signals = signature.get("context_signals", [])
    if not context_signals:
        return 0.5  # Neutral if no context signals defined

    flag_map = {
        "HAS_AUTH flag": flags.get("HAS_AUTH", False),
        "HAS_PAYMENTS flag": flags.get("HAS_PAYMENTS", False),
        "IS_FRONTEND_ONLY flag": flags.get("IS_FRONTEND_ONLY", False),
        "IS_SECURITY_SENSITIVE flag": flags.get("IS_SECURITY_SENSITIVE", False),
        "frontend project": flags.get("IS_FRONTEND_ONLY", False) or flags.get("IS_FULLSTACK", False),
        "payment code": flags.get("HAS_PAYMENTS", False),
        "user data handling": flags.get("HAS_AUTH", False) or flags.get("HAS_DB", False),
    }

    hits = 0
    for signal in context_signals:
        signal_lower = signal.lower()
        for flag_pattern, flag_val in flag_map.items():
            if flag_pattern in signal_lower and flag_val:
                hits += 1
                break

    return min(hits / len(context_signals), 1.0) if context_signals else 0.5


def history_score(workflow_name: str) -> float:
    """
    Score based on historical success rate from intent log.
    Higher score if this workflow was confirmed correct in past sessions.
    """
    if not os.path.exists(INTENT_LOG):
        return 0.5  # Neutral with no history

    total = 0
    correct = 0

    with open(INTENT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                if record.get("top_candidate") == workflow_name:
                    total += 1
                    if record.get("confirmed", False):
                        correct += 1
            except Exception:
                continue

    if total == 0:
        return 0.5

    # Weighted toward recent sessions: simple success rate
    return correct / total


def classify(user_input: str, project_flags: Optional[dict] = None,
             top_n: int = 3, threshold: float = 0.1) -> list[dict]:
    """
    Classify user input into workflow candidates with confidence scores.

    Returns list of {workflow, confidence, reasoning} sorted by confidence desc.
    """
    if not os.path.exists(SIGNATURES_PATH):
        return [{"workflow": "/antibug", "confidence": 0.5, "reasoning": "Default (no signatures file)"}]

    with open(SIGNATURES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    signatures = data.get("signatures", {})
    flags = project_flags or {}
    user_tokens = tokenize(user_input)

    candidates = []

    for workflow, sig in signatures.items():
        kw_s = keyword_score(user_tokens, sig)
        ctx_s = context_score(sig, flags)
        hist_s = history_score(workflow)

        combined = (
            kw_s * WEIGHT_KEYWORD +
            ctx_s * WEIGHT_CONTEXT +
            hist_s * WEIGHT_HISTORY
        )

        if combined >= threshold:
            # Build reasoning explanation
            reasoning_parts = []
            if kw_s > 0.3:
                reasoning_parts.append(f"keyword match ({kw_s:.0%})")
            if ctx_s > 0.6:
                reasoning_parts.append("project context matches")
            if hist_s > 0.6:
                reasoning_parts.append(f"historically successful ({hist_s:.0%})")

            candidates.append({
                "workflow": workflow,
                "confidence": round(combined, 3),
                "confidence_pct": f"{combined:.0%}",
                "reasoning": ", ".join(reasoning_parts) if reasoning_parts else "general match",
                "scores": {
                    "keyword": round(kw_s, 3),
                    "context": round(ctx_s, 3),
                    "history": round(hist_s, 3)
                }
            })

    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    return candidates[:top_n]


def load_flags() -> dict:
    if not os.path.exists(FLAGS_PATH):
        return {}
    with open(FLAGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flags", {})


def log_intent(user_input: str, candidates: list[dict], confirmed: bool = False,
               actual_workflow: Optional[str] = None):
    """Log intent classification for historical learning."""
    os.makedirs(os.path.dirname(INTENT_LOG), exist_ok=True)
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_preview": user_input[:80],
        "top_candidate": candidates[0]["workflow"] if candidates else None,
        "all_candidates": [c["workflow"] for c in candidates],
        "confirmed": confirmed,
        "actual_workflow": actual_workflow
    }
    with open(INTENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def format_output(user_input: str, candidates: list[dict]) -> str:
    """Format the classification output for display in the agent."""
    if not candidates:
        return "No matching workflow found. Try being more specific."

    top = candidates[0]
    lines = [
        f"Interpreting: \"{user_input[:60]}{'...' if len(user_input)>60 else ''}\"",
        "",
        f"  → {top['workflow']:25s} {top['confidence_pct']:5s}  [{top['reasoning']}]"
    ]

    for c in candidates[1:]:
        lines.append(f"    {c['workflow']:25s} {c['confidence_pct']:5s}  [{c['reasoning']}]")

    lines.extend([
        "",
        f"Proceeding with {top['workflow']}.",
        f"Say 'redirect to [command]' to choose a different workflow."
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Antigravity Intent Mapper")
    parser.add_argument("input", nargs="?", help="Natural language task description")
    parser.add_argument("--top", type=int, default=3, help="Number of candidates to return")
    parser.add_argument("--threshold", type=float, default=0.1, help="Minimum confidence score")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--log", action="store_true", help="Log this classification")
    args = parser.parse_args()

    if not args.input:
        # Interactive mode
        print("Antigravity Intent Mapper — Interactive Mode")
        print("Type your task description (or 'quit' to exit):")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in ("quit", "exit", "q"):
                    break
                if not user_input:
                    continue
                flags = load_flags()
                candidates = classify(user_input, flags, args.top, args.threshold)
                print(format_output(user_input, candidates))
                print()
            except KeyboardInterrupt:
                break
        return

    flags = load_flags()
    candidates = classify(args.input, flags, args.top, args.threshold)

    if args.json:
        print(json.dumps(candidates, indent=2))
    else:
        print(format_output(args.input, candidates))

    if args.log and candidates:
        log_intent(args.input, candidates)


if __name__ == "__main__":
    main()
```

---

## Phase 3 — Update CLAUDE.md Section 7

### Step 3.1 — Replace the static auto-detection table in CLAUDE.md

Replace Section 7 (Workflow Auto-Detection) with:

```markdown
## 7. Workflow Auto-Detection (Probabilistic)

Before starting any substantial task, run the intent mapper:
  python .agent/scripts/intent_mapper.py "[user's request]"

The mapper returns ranked workflow candidates with confidence scores:
  → /antibug        68%  [keyword match, context: error pattern]
  → /security-auditor 24%  [context: auth endpoint mentioned]
  → /quality-gate    8%  [general code quality implied]

Proceed with the top candidate. Report it to the user:
  "Interpreting as /antibug (68%). Say 'redirect to [command]' to change."

If top confidence < 25%: ask the user to clarify their intent.
If top confidence > 75%: proceed without asking.
If top confidence 25-75%: proceed but confirm: "Starting /antibug — correct?"

### Quick-Reference Auto-Triggers (for speed)
These still trigger without running the mapper:
  User says "commit" → /auto-commit
  User says "release" → /ship
  User says "scan this" → /scanner
  User uploads a file → read it, then run intent mapper on the content
```

---

## Phase 4 — Create the /intent Command

Create `.claude/commands/intent.md`:

```markdown
---
description: Classify natural language intent into workflow candidates with confidence scores
---

Analyze the intent behind a task description and suggest the best workflow.

Run:
  python .agent/scripts/intent_mapper.py "$ARGUMENTS" --top 3

Display results to user in this format:
  "Interpreting: '[input]'
   
   → /antibug           68%  [keyword match, error pattern]
   → /security-auditor  24%  [context: auth mentioned]
   → /quality-gate       8%  [general quality]

   Proceeding with /antibug. Say 'redirect to [workflow]' to change."

If user says "redirect to /[workflow]":
  Run the specified workflow instead.
  Log the correction: python .agent/scripts/intent_mapper.py --log "[original input]"
  This improves future accuracy.

If user says "interactive":
  python .agent/scripts/intent_mapper.py  (no arguments — enters interactive mode)
```

---

## Phase 5 — Feedback Loop for Improvement

### Step 5.1 — Create the correction capture

When a user redirects to a different workflow, log the correction to improve future scoring:

```python
# In intent_mapper.py, add to log_intent():
# When actual_workflow differs from top_candidate:
# This signals the classifier made a wrong prediction
# Historical weight will down-score the wrong prediction next time
```

Update `.claude/commands/intent.md` to log corrections:

```markdown
## Correction Logging
When user redirects to a different workflow, log the correction:
  python -c "
import sys; sys.path.insert(0, '.agent/scripts')
import intent_mapper
intent_mapper.log_intent(
  '$original_input',
  $candidates,
  confirmed=False,
  actual_workflow='/corrected-workflow'
)
"

This feeds back into the historical scoring to improve future accuracy.
```

---

## Verification

```bash
# 1. Test error debugging intent
python .agent/scripts/intent_mapper.py "the API is throwing 500 errors on login"
# Expected: /antibug top, /security-auditor second

# 2. Test feature creation intent
python .agent/scripts/intent_mapper.py "I want to build a user registration system"
# Expected: /spec top

# 3. Test commit intent (should be clear)
python .agent/scripts/intent_mapper.py "commit my changes to git"
# Expected: /auto-commit with high confidence

# 4. Test ambiguous intent (should show multiple candidates)
python .agent/scripts/intent_mapper.py "the login page needs work"
# Expected: /web-aesthetics, /antibug, /spec — all moderate confidence

# 5. Test JSON output
python .agent/scripts/intent_mapper.py "fix the payment bug" --json

# 6. Interactive mode
python .agent/scripts/intent_mapper.py
# Enter several queries interactively
```

---

## Expected Outputs

| File | Status |
|---|---|
| `.agent/data/workflow_signatures.json` | NEW |
| `.agent/scripts/intent_mapper.py` | NEW |
| `.agent/data/intent_log.jsonl` | NEW (gitignored) |
| `.claude/commands/intent.md` | NEW |
| `CLAUDE.md` | UPDATED (Section 7 — probabilistic auto-detection) |

---

## Learning Resources
- TF-IDF text scoring: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- Naive Bayes text classification: search "naive bayes text classification Python"
- rapidfuzz (fuzzy string matching): https://github.com/maxbachmann/RapidFuzz
- ReAct prompting paper: https://arxiv.org/abs/2210.03629
- sentence-transformers (upgrade path): https://sbert.net/

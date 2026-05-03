---
description: "Self-auditing step that runs after any workflow to verify each agent actually did its job — not just acknowledged it."
---

# Workflow: Cross-Agent Validator

**Objective**: Prevent shallow execution. After any multi-agent workflow completes, this validator audits whether each agent in the pipeline delivered real, substantive output — or just acknowledged the task and moved on.

## When to Run
- Automatically as the **final step** of every multi-agent workflow.
- Manually when you suspect an agent produced surface-level output.
- Before committing any generated artifact (plan, report, code, README) to the repository.

## Execution Sequence

### Step 1 — Pipeline Audit
For each agent that ran in the preceding workflow, check:
- **Did it produce a concrete artifact?** (A file created, a patch written, a plan documented — not just a conversational summary.)
- **Did it run the Research Loop?** (Was evidence cited, or did the agent go straight to output?)
- **Did it follow its SKILL.md rules?** (E.g., did `web-aesthetics` enforce font imports? Did `antibug` provide actual patches, not just descriptions?)

### Step 2 — Gap Detection
For each agent that skipped a required step, flag it:
```
VALIDATOR FLAG: [agent-name]
Expected: [what the SKILL.md requires]
Received: [what actually happened]
Action Required: [re-run agent / complete missing step manually]
```

### Step 3 — Artifact Verification
Confirm that all expected output files exist:
- `build-website` / `build-app` → source files exist, tests exist, `PROJECT_METADATA.md` version was bumped
- `fix-bugs` → patches were applied, version was bumped
- `multi-plan-synthesis` → `MASTER_PLAN.md` exists
- `release-project` → `LICENSE.md`, `README.md`, and `MARKET_EVALUATION.md` all exist
- `write-report` → final document exists with bibliography

### Step 4 — Final Health Score
Output a simple health score:
```
CROSS-AGENT VALIDATION REPORT
==============================
Workflow: [name]
Agents Audited: [N]
Agents Passed: [N]
Agents Flagged: [N]
Artifacts Verified: [list]
Missing Artifacts: [list or "None"]
Overall Health: [GREEN / YELLOW / RED]

GREEN  = All agents passed, all artifacts present.
YELLOW = Minor gaps, no critical failures. Recommend review.
RED    = Critical agent failure or missing core artifact. Do not proceed to commit.
```

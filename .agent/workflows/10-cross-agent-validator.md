---
title: "CROSS AGENT VALIDATOR"
description: "Workflow 10 - CROSS AGENT VALIDATOR"
order: 10
---

# Workflow: Cross-Agent Validator

**Objective**: Prevent shallow execution. After any multi-agent workflow completes, this validator audits whether each agent in the pipeline delivered real, substantive output â€” or just acknowledged the task and moved on.

## When to Run
- Automatically as the **final step** of every multi-agent workflow.
- Manually when you suspect an agent produced surface-level output.
- Before committing any generated artifact (plan, report, code, README) to the repository.

## Execution Sequence

### Step 1 â€” Pipeline Audit
For each agent that ran in the preceding workflow, check:
- **Did it produce a concrete artifact?** (A file created, a patch written, a plan documented â€” not just a conversational summary.)
- **Did it run the Research Loop?** (Was evidence cited, or did the agent go straight to output?)
- **Did it follow its SKILL.md rules?** (E.g., did `web-aesthetics` enforce font imports? Did `antibug` provide actual patches, not just descriptions?)
- **Did it exclude `.agent/` from all scans?** (Deep-scan and antibug must ONLY report on project code.)

### Step 2 â€” Gap Detection
For each agent that skipped a required step, flag it:
```
VALIDATOR FLAG: [agent-name]
Expected: [what the SKILL.md requires]
Received: [what actually happened]
Action Required: [re-run agent / complete missing step manually]
```

### Step 3 â€” Artifact Verification
Confirm that all expected output files exist at project root (not inside `.agent/`):
- `scanner` / `build-website` / `build-app` â†’ source files exist, tests exist, root `PROJECT_METADATA.md` version was bumped
- `fix-bugs` â†’ patches were applied, version was bumped in root `PROJECT_METADATA.md`
- `multi-plan-synthesis` â†’ `MASTER_PLAN.md` exists at project root
- `release-project` â†’ `LICENSE.md`, `README.md` exist at project root; `zip/` contains versioned archive
- `write-report` â†’ final document exists with bibliography

### Step 3.5 â€” Technical Verification (if applicable)
If the workflow produced code, run a structured verification:

```
VERIFICATION: [PASS/FAIL]

Build:    [OK/FAIL]        â€” Run the project's build command
Types:    [OK/X errors]    â€” Run type checker (tsc, mypy, etc.)
Lint:     [OK/X issues]    â€” Run linter (eslint, clippy, flake8)
Tests:    [X/Y passed]     â€” Run full test suite
Coverage: [XX%]            â€” Check coverage meets 80% threshold
Git:      [clean/dirty]    â€” Show uncommitted changes

Ready for commit: [YES/NO]
```

### Step 4 â€” Final Health Score
```
CROSS-AGENT VALIDATION REPORT
==============================
Workflow: [name]
Agents Audited: [N]
Agents Passed: [N]
Agents Flagged: [N]
.agent/ Exclusion Respected: [YES / NO â€” flag if any agent scanned .agent/]
Artifacts Verified: [list]
Missing Artifacts: [list or "None"]
Overall Health: [GREEN / YELLOW / RED]

GREEN  = All agents passed, all artifacts present, .agent/ correctly excluded.
YELLOW = Minor gaps, no critical failures. Recommend review.
RED    = Critical agent failure, missing core artifact, or .agent/ was scanned as project code.
```

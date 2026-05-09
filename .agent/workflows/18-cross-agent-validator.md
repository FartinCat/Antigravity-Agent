---
title: "CROSS AGENT VALIDATOR"
description: "Audit previous steps for hallucinations/errors."
order: 18
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

- **Did it exclude `.agent/` from all scans?** (Deep-scan and antibug must ONLY report on project code.)



### Step 2 — Gap Detection

For each agent that skipped a required step, flag it:

```

VALIDATOR FLAG: [agent-name]

Expected: [what the SKILL.md requires]

Received: [what actually happened]

Action Required: [re-run agent / complete missing step manually]

```



### Step 3 — Artifact Verification

Confirm that all expected output files exist in their designated locations (per Rule 20 — output routing):

- `scanner` / `build-website` / `build-app` → source files exist, tests exist, root `PROJECT_METADATA.md` version was bumped

- `fix-bugs` → patches were applied, version was bumped in root `PROJECT_METADATA.md`

- `multi-plan-synthesis` → `MASTER_PLAN.md` exists in `docs/master-plans/`

- `release-project` → `LICENSE.md`, `README.md` exist at project root; `zip/` contains versioned archive

- `write-report` → final document exists with bibliography



### Step 3.5 — Technical Verification (if applicable)

If the workflow produced code, run a structured verification:



```

VERIFICATION: [PASS/FAIL]



Build:    [OK/FAIL]        — Run the project's build command

Types:    [OK/X errors]    — Run type checker (tsc, mypy, etc.)

Lint:     [OK/X issues]    — Run linter (eslint, clippy, flake8)

Tests:    [X/Y passed]     — Run full test suite

Coverage: [XX%]            — Check coverage meets 80% threshold

Git:      [clean/dirty]    — Show uncommitted changes



Ready for commit: [YES/NO]

```



### Step 4 — Final Health Score

```

CROSS-AGENT VALIDATION REPORT

==============================

Workflow: [name]

Agents Audited: [N]

Agents Passed: [N]

Agents Flagged: [N]

.agent/ Exclusion Respected: [YES / NO — flag if any agent scanned .agent/]

Artifacts Verified: [list]

Missing Artifacts: [list or "None"]

Overall Health: [GREEN / YELLOW / RED]



GREEN  = All agents passed, all artifacts present, .agent/ correctly excluded.

YELLOW = Minor gaps, no critical failures. Recommend review.

RED    = Critical agent failure, missing core artifact, or .agent/ was scanned as project code.

```



**Note**: Perform registry drift check (`/sync-registry`) during artifact verification. If drift > 5 components, flag as YELLOW health.

### Step 5 — Autonomous Self-Diagnosis

These checks prevent the validator itself from becoming a source of drift.

#### 5a — Rule 20 Compliance Audit
Scan this workflow's own Step 3 artifact paths. If any step directs output to
"project root" for files that should go to `docs/` per Rule 20, flag as:
```
SELF-CHECK FAIL: Step 3 artifact path contradicts Rule 20 (output routing)
```

#### 5b — Version Consistency
Read `CLAUDE.md` version and compare to `PROJECT_METADATA.md`. If they differ:
```
SELF-CHECK FAIL: CLAUDE.md version drift detected — run /sync-registry
```

#### 5c — Hardcoded Version Detection
Scan all `.agent/workflows/*.md` files for literal version strings like `v3.0.0`,
`v4.0.0`, etc. that should be dynamically read from `PROJECT_METADATA.md`. Flag each:
```
HARDCODED VERSION: [workflow-file] references [version] — should use dynamic lookup
```

#### 5d — Numbering Collision Check
Run `python .agent/scripts/sync_registry.py` and check Step 2 output. If collisions
or gaps are reported, flag as YELLOW health.

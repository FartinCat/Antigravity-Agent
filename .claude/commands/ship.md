---
description: Run parallel fan-out to code-reviewer, security-auditor, and test-engineer, then synthesize a go/no-go decision
---

`/ship` is a fan-out orchestrator. Spawn three subagents **CONCURRENTLY**.

## PHASE A — Parallel Fan-Out (all three in one turn)

1. **code-reviewer**: Five-axis review (correctness, readability, architecture, security, performance)
2. **security-auditor**: OWASP Top 10, secrets handling, auth/authz, dependency CVEs
3. **test-engineer**: Coverage gaps for happy path, edge cases, error paths, concurrency

## PHASE B — Merge in Main Context

- Aggregate Critical/Important findings, resolve duplicates
- Promote Critical security findings to **launch blockers**
- Check accessibility (keyboard nav, contrast), infrastructure (env vars, migrations)

## PHASE C — Decision and Rollback Plan

Output: **"Ship Decision: GO | NO-GO"** with:
- Blockers (if any)
- Recommended fixes
- Rollback plan

**Rule:** If ANY persona returns a Critical finding → default **NO-GO** unless user accepts risk.

**Skip fan-out ONLY if:** ≤2 files changed AND diff <50 lines AND does NOT touch auth/payments/data/config.

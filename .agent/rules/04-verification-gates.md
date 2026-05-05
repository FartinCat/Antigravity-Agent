# Verification Gate System

Every action passes through a gate before the agent declares it complete. Gates are layered and cumulative — each level includes all previous levels.

## Verification Ladder

### Level 1: SYNTAX CHECK (Cost: <100ms)
Language-native parser or compiler in check mode.
Pass criterion: exit code 0.

### Level 2: STATIC ANALYSIS (Cost: <2s)
Linter / type checker (mypy, tsc --noEmit, cargo check, eslint, clippy).
Pass criterion: zero warnings at error level.

### Level 3: UNIT TEST PASS (Cost: <30s)
Run the subset of tests relevant to the changed file.
Pass criterion: all tests pass.

### Level 4: INTEGRATION TEST PASS (Cost: <5min)
Run integration tests if applicable.
Pass criterion: all integration tests pass.

### Level 5: BEHAVIORAL SPOT CHECK (LLM-assisted)
Sample 2-3 behaviors the change is supposed to enable.
Ask: "Given this implementation, will behavior X work? Explain in one sentence."
This is a sanity check, not a guarantee.

### Level 6: HUMAN SIGN-OFF (for high-risk changes)
Present the verification report to the human.
Block on human confirmation before committing.

## Confidence-Based Gate Selection

| Confidence Score | Required Gate Level |
|---|---|
| ≥ 85 | Level 1-3 (auto-accept) |
| 70-84 | Level 1-4 (flag for spot check) |
| 50-69 | Level 1-5 (hold for human review) |
| < 50 | Level 6 (decompose further or escalate) |

## Action-Specific Gates

| Action Type | Primary Gate |
|---|---|
| Write file | Syntax check (L1) |
| Build | Exit code + stderr (L2) |
| Test | All pass + no regressions (L3) |
| Deploy | Health endpoint check (L4) |
| Security-critical | Human sign-off (L6) |

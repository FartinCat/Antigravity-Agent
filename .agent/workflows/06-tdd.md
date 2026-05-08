---
title: "TDD"
description: "Workflow 6 - TDD"
order: 6
---

# Workflow: TDD Cycle

**Objective**: Ensure high code quality and functional correctness through disciplined test-driven development.

## Pre-Conditions
Before starting any TDD cycle, confirm:
- `/scanner` has been run and the project structure is understood.
- `MASTER_PLAN.md` or a planner roadmap exists â€” TDD without a plan produces test soup.
- The tech stack and test framework are confirmed (check `PROJECT_METADATA.md`).

## The TDD Cycle

```
RED â†’ GREEN â†’ REFACTOR â†’ REPEAT

RED:      Write a failing test
GREEN:    Write minimal code to pass
REFACTOR: Improve code, keep tests passing
REPEAT:   Next feature/scenario
```

## Execution Sequence

1. **Context Load**: Read `.agent/session-context.md` to understand what was last built and what comes next.
2. **Feature Selection**: Identify the single smallest unit of behavior from the current roadmap phase.
3. **Scaffold Interface**: Define types/interfaces first. The function signature exists but throws `Not Implemented`.
4. **RED**: Write a failing test using `/tdd-guide`. Name it: `test_[what]_[condition]_[expected]`.
   - Run the test and **verify it FAILS** for the right reason (not a syntax error).
5. **GREEN**: Write the minimal code to pass the test. No extras. Run the full suite â€” all tests must be green.
6. **REFACTOR**: Apply `06-refactor.md` principles. Run the full suite again after each change.
7. **Repeat**: Return to step 2 for the next unit.
8. **Coverage Check**: Verify coverage meets the thresholds below.
9. **Log**: When a feature is complete, append to `.agent/session-context.md`.

## Coverage Requirements

- **80% minimum** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

## Test Types to Include

**Unit Tests** (Function-level):
- Happy path scenarios
- Edge cases (empty, null, max values, boundary values)
- Error conditions

**Integration Tests** (Component-level):
- API endpoints
- Database operations
- External service calls

**E2E Tests** (Full stack):
- Critical user flows
- Multi-step processes

## Guardrails

**DO:**
- âœ… Write the test FIRST, before any implementation
- âœ… Run tests and verify they FAIL before implementing
- âœ… Write minimal code to make tests pass
- âœ… Refactor only after tests are green
- âœ… Aim for 80%+ coverage (100% for critical code)

**DON'T:**
- âŒ Write implementation before tests
- âŒ Skip running tests after each change
- âŒ Write too much code at once
- âŒ Ignore failing tests
- âŒ Test implementation details (test behavior)

## Tools Involved
- `/tdd-guide` agent (Red-Green-Refactor protocol)
- `06-refactor.md` foundational skill (Phase 3 cleanup rules)
- `/antibug` (post-feature regression check)

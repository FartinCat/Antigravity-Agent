---
description: "Step 5 — Write test-first code using the Red-Green-Refactor cycle."
order: 6
---

# Workflow: TDD Cycle

**Objective**: Ensure high code quality and functional correctness through disciplined test-driven development.

## Pre-Conditions
Before starting any TDD cycle, confirm:
- `/scanner` has been run and the project structure is understood.
- `MASTER_PLAN.md` or a planner roadmap exists — TDD without a plan produces test soup.
- The tech stack and test framework are confirmed (check `PROJECT_METADATA.md`).

## Steps

1. **Context Load**: Read `.agent/session-context.md` to understand what was last built and what comes next.
2. **Feature Selection**: Identify the single smallest unit of behavior from the current roadmap phase.
3. **Red**: Write a failing test for that unit using `/tdd-guide`. Name it: `test_[what]_[condition]_[expected]`.
4. **Green**: Write the minimal code to pass the test. No extras. Run the full suite — all tests must be green.
5. **Refactor**: Apply `04-refactor.md` principles. Run the full suite again after each change.
6. **Repeat**: Return to step 2 for the next unit.
7. **Log**: When a feature is complete, append to `.agent/session-context.md`.

## Tools Involved
- `/tdd-guide` agent (Red-Green-Refactor protocol)
- `04-refactor.md` foundational skill (Phase 3 cleanup rules)
- `/antibug` (post-feature regression check)

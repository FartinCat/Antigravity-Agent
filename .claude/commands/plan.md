---
description: Break work into small verifiable tasks with acceptance criteria and dependency ordering
---

Invoke the Antigravity planning-and-task-breakdown workflow.

**ENTER PLAN MODE — read only, no code changes.**

Process:
1. Read `SPEC.md` (or existing spec/requirements)
2. Map the dependency graph (what must be built before what)
3. Slice **VERTICALLY** — one complete path per task, not horizontal layers
4. Write each task with:
   - Description
   - Acceptance criteria (3 max)
   - Verification step
   - Files likely touched
   - Estimated scope: S (1-2 files) / M (3-5 files) / L (5+ files → break down further)
5. Add checkpoints between phases (build must pass, tests must pass)
6. Present plan for human review before any implementation begins

Task sizing rule: L = break it down further.

Save plan to `tasks/plan.md` and task list to `tasks/todo.md`.

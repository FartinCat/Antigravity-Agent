---
name: "source-command-impl"
description: "Implement the next task incrementally — build, test, verify, commit"
---

# source-command-impl

Use this skill when the user asks to run the migrated source command `impl`.

## Command Template

Invoke the Antigravity incremental-implementation + tdd-guide workflow.

Pick the **NEXT PENDING** task from `tasks/todo.md`.

For each task:
1. Read the task's acceptance criteria
2. Load relevant context (existing code, patterns, types) — **use scripts, not raw reads**
3. Write a **FAILING test** for the expected behavior (**RED**)
4. Implement **minimum code** to pass the test (**GREEN**)
5. Run full test suite to check for regressions
6. Run build to verify compilation
7. Commit with descriptive message (Conventional Commits format)
8. Mark task complete in `tasks/todo.md` and move to next

If any step fails: invoke `/antibug`.

**Rule:** Never implement without a test. Never skip the RED phase.

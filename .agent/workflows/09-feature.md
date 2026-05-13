# Workflow: Feature Development

**Objective**: Incrementally build a single feature from specification through implementation to verification. This is the inner loop of development — one feature at a time, fully tested before moving to the next.

## Trigger Conditions
- User has an approved plan with task items
- User says "build feature X" or "implement the next task"
- Invoked via `/feature-development`

## Execution Sequence

### Phase 1 — Feature Scoping (Pre-flight)
1. **Read Plan**: Load the current implementation plan or task list.
2. **Select Next Task**: Pick the highest-priority incomplete task.
3. **Acceptance Criteria**: Extract or define 3-5 measurable criteria for "done."
4. **Dependency Check**: Verify all prerequisites (files, APIs, packages) are available.
5. **Estimate Scope**: Flag if the task is > 200 lines of change — if so, decompose further.

**Gate**: Announce the selected task and acceptance criteria. Proceed only if scope is manageable.

### Phase 2 — Implementation
1. **Branch Context**: Note the current git state (branch, clean/dirty).
2. **Scaffold First**: Create file stubs, interfaces, or type definitions before writing logic.
3. **Incremental Build**: Write code in blocks of < 50 lines. After each block:
   - Run the relevant test suite or linter
   - Fix any errors before continuing
   - Do NOT accumulate untested code
4. **Follow Existing Patterns**: Match the codebase's existing style, naming conventions, and architecture.
5. **No Gold Plating**: Implement exactly what the acceptance criteria require — nothing more.

### Phase 3 — Verification
1. **Unit Tests**: Write or update tests covering the new feature. Minimum: 1 happy path, 1 edge case, 1 error case.
2. **Integration Check**: Verify the feature works with adjacent components.
3. **Regression Scan**: Run the full test suite to confirm nothing broke.
4. **Acceptance Criteria Review**: Check each criterion explicitly — mark PASS/FAIL.
5. **Code Quality**: Run linter, check for TODO/FIXME/HACK comments left behind.

**Gate**: All acceptance criteria must PASS. If any FAIL, return to Phase 2.

### Phase 4 — Commit & Update
1. **Stage Changes**: `git add` only files related to this feature.
2. **Conventional Commit**: Write a commit message following `12-commit-semantics.md`.
3. **Update Task List**: Mark the task as complete in the plan.
4. **Session Context**: Log the feature completion in **`AETHER.md` §18**.

## Failure Paths
- **Test Failures**: If tests fail after 3 fix attempts, escalate to `/antibug` for root-cause analysis.
- **Scope Creep**: If implementation reveals the task is larger than estimated, STOP, decompose it, and restart Phase 1 with sub-tasks.
- **Dependency Missing**: If a required API/package is unavailable, document the blocker and move to the next independent task.
- **Breaking Change**: If the feature breaks existing tests, assess whether the change is intentional (update tests) or a regression (revert and investigate).

## Rollback Protocol
If the feature is abandoned mid-implementation:
1. `git stash` or `git checkout -- .` to revert changes
2. Log the reason for abandonment in **`AETHER.md` §18**
3. Update the task list with a "BLOCKED" status and the reason

## Output Format
```
FEATURE COMPLETE: [feature name]
─────────────────────────────────
Acceptance Criteria:
  ✅ [criterion 1] — PASS
  ✅ [criterion 2] — PASS
  ✅ [criterion 3] — PASS
Tests: [X passed, Y failed, Z skipped]
Files Changed: [count]
Commit: [hash] — [message]
```

## Output Organization (Rule 20)
Feature reports are ephemeral — logged to **`AETHER.md` §18** only, not saved as standalone files.

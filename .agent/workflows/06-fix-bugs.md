---
description: "Step 6 — Find and patch all bugs: Scanner → Historical Analysis → Antibug → Patch → Test → Version → Validate."
order: 7
---

# Workflow: Fix Bugs

**Objective**: Automatically track down and resolve syntax errors, logic flaws, memory leaks, and historical regressions.

## Execution Sequence

1. **Context Read**: Read `.agent/session-context.md` for any notes from previous sessions about known issues.
2. **Scan**: Invoke `/scanner` to map the current project structure. The scanner EXCLUDES `.agent/` — the diagnostic focuses only on project code.
3. **Hunt**: Pass the scanner output to `/antibug`. The antibug agent MUST:
   - Execute Phase 0 (Historical Pattern Analysis from `dump/` — NOT from `.agent/`).
   - Run Phases 1–4 on project source files only.
   - Never flag `.agent/` files as bugs in the project.
4. **Patch**: Apply all CRITICAL and HIGH severity fixes. Apply MEDIUM fixes if time permits.
5. **Verify**: Run the full test suite via `/tdd-guide` to confirm no regressions were introduced.
6. **Version Bump**: Apply `semantic-versioning` — bump the Patch version in root `PROJECT_METADATA.md` (v0.1.X).
7. **Log**: Append a session entry to `.agent/session-context.md` detailing what was fixed.
8. **Validate**: Run `cross-agent-validator` to confirm patches are real and version was bumped.

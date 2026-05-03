---
description: "Orchestrates the bug hunting process: Deep Scan -> Historical Analysis -> Antibug -> Patch Bump -> Validation."
---

# Workflow: Fix Bugs

**Objective**: Automatically track down and resolve syntax errors, logic flaws, memory leaks, and historical regressions.

## Execution Sequence

1. **Context Read**: Check `.agent/session-context.md` for any notes from previous sessions about known issues.
2. **Scan**: Invoke `/deep-scan` to map the current repository structure and identify recently modified files.
3. **Hunt**: Pass the context to `/antibug`. The antibug agent MUST execute Phase 0 (Historical Pattern Analysis from `dump/`) before issuing any diagnosis.
4. **Patch**: Apply all CRITICAL and HIGH severity fixes. Apply MEDIUM fixes if time permits.
5. **Verify**: Run the full test suite via `/tdd-guide` to confirm no regressions were introduced.
6. **Version Bump**: Apply `semantic-versioning` — bump the Patch version (v0.1.X).
7. **Log**: Append a session entry to `.agent/session-context.md` detailing what was fixed.
8. **Validate**: Run `cross-agent-validator` to confirm patches are real and version was bumped.

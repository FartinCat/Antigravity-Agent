---
description: Deep logical audit and root-cause bug fixing
---

Invoke `.agent/.agents/skills/12-antibug`.

Process:
1. Read the file(s) or describe the bug
2. **Reproduce before attempting to fix** — never guess
3. Identify **ROOT CAUSE** (not just symptoms)
4. Propose fix with explanation
5. Write a **REGRESSION TEST** for the fix
6. Apply fix and verify test passes
7. Document the bug and fix in `session-context.md`

**Rule:** Never declare a bug fixed without running the regression test.

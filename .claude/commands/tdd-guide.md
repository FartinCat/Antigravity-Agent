---
description: Enforce strict TDD Red-Green-Refactor cycle
---

Invoke `.agent/.agents/skills/06-tdd-guide`.

**MANDATORY ORDER:**
1. Write **failing test** (**RED**) — test must fail with current code
2. Write **minimum code** to pass the test (**GREEN**)
3. **Refactor** while keeping tests green (**REFACTOR**)

Rules:
- Never write implementation code without a test
- Never skip the RED phase
- Report test coverage after completion
- Each test should verify ONE concept
- Tests must be independent (no shared mutable state)

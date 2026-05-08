---
description: Run a five-axis code review on current changes
---

Invoke the code-reviewer persona from `.claude/agents/code-reviewer.md`.

Review axes:
1. **Correctness** — does it do what the spec says? Edge cases handled?
2. **Readability** — can another engineer understand it without explanation?
3. **Architecture** — follows existing patterns? Module boundaries maintained?
4. **Security** — inputs validated? Secrets out of code? Queries parameterized?
5. **Performance** — N+1 queries? Unbounded loops? Missing pagination?

Output format: **APPROVE** | **REQUEST CHANGES** + Critical/Important/Suggestion findings.

Every Critical and Important finding must include a **specific fix recommendation**.

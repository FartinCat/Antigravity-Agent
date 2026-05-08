---
description: "Step 17 � debug session."
order: 17
---
Help me debug an issue. Clarify expectations, identify gaps, and agree on a fix plan before changing code.

1. **Gather Context** — If not already provided, ask for: issue description (what is happening vs what should happen), error messages/logs/screenshots, recent related changes or deployments, and scope of impact.
2. **Use Memory for Context** — Search memory for similar incidents/fixes before deep investigation: `npx ai-devkit@latest memory search --query "<issue symptoms or error>"`.
3. **Clarify Reality vs Expectation** — Restate observed vs expected behavior. Confirm relevant requirements or docs that define the expectation. Define acceptance criteria for the fix.
4. **Reproduce & Isolate** — Determine reproducibility (always, intermittent, environment-specific). Capture reproduction steps. List suspected components or modules.
5. **Analyze Potential Causes** — Brainstorm root causes (data, config, code regressions, external dependencies). Gather supporting evidence (logs, metrics, traces). Highlight unknowns needing investigation.
6. **Resolve** — Present resolution options (quick fix, refactor, rollback, etc.) with pros/cons and risks. Ask which option to pursue. Summarize chosen approach, pre-work, success criteria, and validation steps.
7. **Store Reusable Knowledge** — Save root-cause and fix patterns via `npx ai-devkit@latest memory store ...`.
8. **Next Command Guidance** — After selecting a fix path, continue with `/execute-plan`; when implemented, use `/check-implementation` and `/writing-test`.


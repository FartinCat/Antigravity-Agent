---
description: "Orchestrates the entire website building process: Scaffolding -> Planning -> Styling -> Testing -> Validation."
---

# Workflow: Build Website

**Objective**: Execute a flawless, end-to-end pipeline for generating a modern web application.

## Execution Sequence

1. **Scaffold**: Trigger `/scaffold-assets` to build the required directory taxonomy and initialize `PROJECT_METADATA.md`.
2. **Plan**: Invoke `/planner` to map out the required HTML/JS structure. Planner must complete the Research Loop before generating the roadmap.
3. **Style**: Invoke `/web-aesthetics` to ensure the UI is premium, uses modern typography, and avoids generic placeholders.
4. **Test-Drive**: Execute `/tdd-guide` to build all logic using the Red-Green-Refactor cycle. No production code without a passing test.
5. **Bug Check**: Run `/antibug` including Phase 0 historical pattern analysis before finalizing.
6. **Version Bump**: Apply `semantic-versioning` — bump the Minor version (v0.X.0).
7. **Validate**: Run `cross-agent-validator` to confirm all agents completed their full responsibilities.

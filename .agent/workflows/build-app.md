---
description: "Orchestrates the entire application building process: Scaffolding -> Planning -> Logic -> Testing -> Validation."
---

# Workflow: Build Application

**Objective**: Execute an end-to-end pipeline for generating a software application (Python, Rust, Java, etc).

## Execution Sequence

1. **Scaffold**: Trigger `/scaffold-assets` to build the required directory taxonomy and initialize `PROJECT_METADATA.md`.
2. **Plan**: Invoke `/planner` to map out the application architecture using `architectural-design.md` principles. Planner must complete the Research Loop before outputting the roadmap.
3. **Test-Drive**: Execute `/tdd-guide` to build all logic using strict Red-Green-Refactor. Every function must have a test before it is written.
4. **Bug Check**: Run `/antibug` including Phase 0 historical pattern analysis.
5. **Refactor**: Apply `refactor.md` principles to all generated code before committing.
6. **Version Bump**: Apply `semantic-versioning` — bump the Minor version (v0.X.0).
7. **Validate**: Run `cross-agent-validator` to confirm all agents completed their full responsibilities.

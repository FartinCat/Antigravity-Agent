---
title: "05B BUILD APP"
description: "Production-ready application build cycle."
order: 5
---

# Workflow: Build Application



**Objective**: Execute an end-to-end pipeline for generating a software application (Python, Rust, Java, etc).



## Execution Sequence



1. **Scaffold**: Trigger `/scaffold-assets` to build the required directory taxonomy and initialize `PROJECT_METADATA.md`.

2. **Plan**: Invoke `/planner` to map out the application architecture using `04-architectural-design.md` principles. Planner must complete the Research Loop before outputting the roadmap.

3. **Test-Drive**: Execute `/tdd-guide` to build all logic using strict Red-Green-Refactor. Every function must have a test before it is written.

4. **Bug Check**: Run `/antibug` including Phase 0 historical pattern analysis.

5. **Refactor**: Apply `06-refactor.md` principles to all generated code before committing.

6. **Version Bump**: Apply `semantic-versioning` — bump the Minor version in root `PROJECT_METADATA.md` (v0.X.0).

7. **Log**: Append a session entry to `.agent/session-context.md` with what was built and the new version.

8. **Validate**: Run `cross-agent-validator` to confirm all agents completed their full responsibilities.


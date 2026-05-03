---
description: "Orchestrates the entire website building process: Scaffolding -> Planning -> Styling -> Testing."
---

# Workflow: Build Website

**Objective**: Execute a flawless, end-to-end pipeline for generating a modern web application.

## Execution Sequence

1. **Scaffold**: Automatically trigger `/scaffold-assets` to build the required directory taxonomy.
2. **Plan**: Invoke the `planner` agent to map out the required HTML/JS structure.
3. **Style**: Invoke the `web-aesthetics` skill to ensure the UI is premium, uses modern typography, and avoids generic placeholders.
4. **Test**: Execute the `/tdd` workflow to build the logic cleanly.
5. **Version Bump**: Invoke `semantic-versioning` to bump the Minor version (v0.X.0).

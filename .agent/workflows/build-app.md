---
description: "Orchestrates the entire application building process: Scaffolding -> Planning -> Logic -> Testing."
---

# Workflow: Build Application

**Objective**: Execute an end-to-end pipeline for generating a software application (Python, Rust, Java, etc).

## Execution Sequence

1. **Scaffold**: Automatically trigger `/scaffold-assets` to build the required directory taxonomy.
2. **Plan**: Invoke the `planner` agent to map out the application architecture, keeping `architectural-design` principles in mind (separation of concerns, state management).
3. **Develop**: Execute the `/tdd` workflow to build the logic iteratively.
4. **Version Bump**: Invoke `semantic-versioning` to bump the Minor version (v0.X.0).

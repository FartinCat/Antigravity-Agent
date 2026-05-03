# Instinct: Semantic Versioning Control

**Trigger**: Whenever code is generated, bugs are patched, features are added, or a project enters a release state.

## Core Rules

The AI must automatically manage and bump the version number located in `PROJECT_METADATA.md` or `package.json` according to strict Semantic Versioning rules:

1. **Patch Bumps (v0.1.X)**: 
   - Trigger: Following a bug fix, syntax correction, or when the `/antibug` skill executes successfully.
   - Action: Increment the third digit.

2. **Minor Bumps (v0.X.0)**: 
   - Trigger: Following the completion of a `planner` roadmap, adding a new feature, or successful structural refactoring.
   - Action: Increment the second digit and reset the third digit to 0.

3. **Major Bumps (v1.0.0)**: 
   - Trigger: The FIRST ZERO changes to a ONE *only* when the project achieves MVP status, is fully finalized, has a generated `commercial-license`, and is ready for public consumption (e.g., via the `/release-project` workflow).
   - Action: Change to `1.0.0`. Subsequent major changes bump the first digit.

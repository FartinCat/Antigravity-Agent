# Instinct: Semantic Versioning Control

**Trigger**: Whenever code is generated, bugs are patched, features are added, or a project enters a release state.

## Single Source of Truth
**The version is stored in one place only: `PROJECT_METADATA.md` at the project root.**
If a `package.json` also exists, keep it in sync — but the root `PROJECT_METADATA.md` is the master. Never bump both independently and never create a second copy of `PROJECT_METADATA.md` inside `assets/information/`.

## Core Rules

1. **Patch Bumps (v0.1.X)**:
   - Trigger: Following a bug fix, syntax correction, or when the `/antibug` skill executes successfully.
   - Action: Increment the third digit. Append a changelog entry to `PROJECT_METADATA.md`.

2. **Minor Bumps (v0.X.0)**:
   - Trigger: Following the completion of a `planner` roadmap, adding a new feature, or successful structural refactoring.
   - Action: Increment the second digit and reset the third digit to 0. Append a changelog entry.

3. **Major Bumps (v1.0.0)**:
   - Trigger: The first zero changes to a one **only** when the project achieves MVP status, is fully finalized, has a generated `commercial-license`, and is ready for public consumption via the `/release-project` workflow.
   - Action: Change to `1.0.0`. Append a changelog entry noting the release milestone.

## Changelog Append Format
When bumping any version, add this to the `## Changelog` section of `PROJECT_METADATA.md`:
```
- v[NEW VERSION] ([DATE]): [Brief description of what changed — e.g., "Fixed PDF annotation crash on empty files."]
```

## Sync Rule
If `package.json` exists alongside `PROJECT_METADATA.md`, update its `"version"` field to match after every bump. Use the root `PROJECT_METADATA.md` as the trigger — never the other way around.

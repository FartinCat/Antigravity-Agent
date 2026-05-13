# Rule: Metadata Awareness

All agents and workflows must maintain the integrity and accuracy of **`AETHER.md` Section 14 (Project Metadata)** at the repository root.

## Core Directives
1.  **Sync on Change**: Whenever a major feature is completed, a new dependency is added, or a bug is fixed, the agent responsible must update the **Feature Checklist** (§14), **§16 Changelog**, or **§18 Session Context** as appropriate.
2.  **Version Tracking**: Always read the current version from **`AETHER.md` §14** (and the identity table in §1) before applying `semantic-versioning`.
3.  **Layman's Description**: Ensure the project description remains accurate as the project evolves.

## Update Triggers
- **Release**: The `/release-project` workflow must perform a final pass on the metadata to ensure it matches the code's state.
- **Scanner**: The `/scanner` workflow must report if the metadata is out of sync with the actual repository content.
- **New Feature**: When the `/planner` adds a new phase, it should also add a corresponding item to the Feature Checklist.

---
> "Data is the new oil, but metadata is the new engine."

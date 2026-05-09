---
title: "CONTINUOUS VERSIONING"
description: "Governance rule mandating a semantic version bump before every finalized commit sequence."
---

# Rule 22: Continuous Auto-Versioning

**Objective**: Ensure that the software version incrementally ticks forward naturally as work progresses, without relying on manual human intervention or waiting for a massive monolithic release cycle.

## The Versioning Mandate
If you (the Agent) have modified the codebase in a way that alters logic, adds features, or fixes bugs during the current session, you **MUST** ensure the version is bumped before finalizing the work via `/23-auto-commit`.

### Increment Rules (SemVer)
- **Patch (+0.0.1)**: Any update or changes to existing files or directories.
- **Minor (+0.1.0)**: Major architectural additions, like building a new subdirectory inside any folder or introducing a new agent/workflow.
- **Major (+1.0.0)**: If the whole directory or core operational logic is completely changed (e.g., v4 to v5).

### Execution Trigger
This rule is automatically enforced by the **`sync_registry.py`** engine during the `/23-sync-registry` workflow.
1. The script runs `git status` / `git diff`.
2. It evaluates the changes against the criteria above.
3. It autonomously bumps `PROJECT_METADATA.md` before syncing the rest of the documentation.

*Failure to increment the version when functional changes occur is a violation of the God Mode integrity mandate.*

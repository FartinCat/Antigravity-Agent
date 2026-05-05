# Instinct: Release Packaging

**Trigger**: Successful execution of a version bump in `PROJECT_METADATA.md` or completion of the `11-release-project` workflow.

## Objective
Ensure that a distributable ZIP archive of the core `.agent/` folder is always synchronized with the current system state. This prevents users from accidentally deploying an outdated version of the brain.

## Core Rules

### Rule 1 — Automatic Synchronization
Whenever the system version is incremented:
1.  **Locate**: Target the `.agent/` directory.
2.  **Naming**: The output zip must be named `antigravity-agent-v[VERSION].zip` (e.g., `antigravity-agent-v3.0.0.zip`).
3.  **Destination**: Save the archive into the `zip/` directory at the project root.
4.  **Exclusions**: Ensure `.git`, `node_modules`, and any local-only temp files are EXCLUDED from the archive. Only the core `.agent/` infrastructure and necessary root documentation (`README.md`, `LICENSE.md`, `DEPLOY.md`) should be included if requested.

### Rule 2 — Atomic Updates
Do not delete the previous version's zip file immediately. Keep the last **three** major/minor versions in the `zip/` folder for rollback purposes.

### Rule 3 — Metadata Verification
Before packaging, the agent MUST verify that `antigravity-agent-install-state.json` has been updated to the same version number as `PROJECT_METADATA.md`.

## Execution Command (PowerShell)
```powershell
# Example command for v3.0.0
Compress-Archive -Path ".agent", "README.md", "LICENSE.md", "DEPLOY.md" -DestinationPath "zip/antigravity-agent-v3.0.0.zip" -Force
```

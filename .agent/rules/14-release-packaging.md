# Instinct: Release Packaging

**Trigger**: Successful execution of a version bump in **`AETHER.md`** or completion of the `15-release` workflow.

## Objective
Ensure that a distributable ZIP archive of the core `.agent/` folder is always synchronized with the current system state. This prevents users from accidentally deploying an outdated version of the brain.

## Core Rules

### Rule 1 — Automatic Synchronization
Whenever the system version is incremented:
1.  **Locate**: Target the `.agent/` directory.
2.  **Naming**: The output zip must be named `aether-agent-v[VERSION].zip` (e.g., `aether-agent-v3.0.0.zip`).
3.  **Destination**: Save the archive into the `archived/current-version/` directory.
4.  **Exclusions**: Ensure `.git`, `node_modules`, and any local-only temp files are EXCLUDED from the archive. Only the core `.agent/` infrastructure and necessary root documentation (`README.md`, `LICENSE.md`, **`AETHER.md`**) should be included if requested.

### Rule 2 — Atomic Updates & Archiving
Before packaging the new version:
1. Move the previous version's zip file from `archived/current-version/` (and any legacy ones in `zip/`) to `archived/old-versions/`.
2. Do not delete old versions. Keep all past versions in `archived/old-versions/` for rollback purposes.

### Rule 3 — Metadata Verification
Before packaging, the agent MUST verify that **`.agent/aether-agent-install-state.json`** (and **`.agent/antigravity-agent-install-state.json`** when that legacy mirror exists) show the same version as **`AETHER.md` §14 / §1**.

## Execution Command (PowerShell)
```powershell
# Example commands for v3.0.0
Move-Item -Path "archived/current-version/*.zip" -Destination "archived/old-versions/" -ErrorAction SilentlyContinue
Move-Item -Path "zip/*.zip" -Destination "archived/old-versions/" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "archived/current-version/"
Compress-Archive -Path ".agent", "README.md", "LICENSE.md", "AETHER.md" -DestinationPath "archived/current-version/aether-agent-v3.0.0.zip" -Force
```

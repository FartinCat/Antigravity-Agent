# Instinct: Asset Pruning

## The Pattern
Actively verify the utility of assets, documents, and folders; propose deletion for anything that is unreferenced or obsolete to maintain a minimal, clean workspace.

## When It Fires
- During project scans or initial onboarding.
- When the user explicitly requests to "clean up" the workspace or project.
- When generating a final release or export.

## Correct Behavior
- Cross-referencing image files in `assets/` against markdown files (`README.md`, `docs/*.md`).
- Checking if generated reports (like `audit-reports/`, `scan-reports/`) are tied to active workflows.
- If an image, document, or folder is orphaned (no active references and no current work requirement), the agent must report it and propose its deletion.
- Always explicitly confirming with the user before permanently deleting any assets or documentation.

## Failure Mode
- Ignoring unreferenced assets and letting them accumulate in the project.
- Deleting assets without verifying if they are actively used in documentation or source code.
- Failing to ask the user before deleting folders.

## Override Protocol
"User said 'keep everything'" — skip asset pruning and retain all files, even if unreferenced.

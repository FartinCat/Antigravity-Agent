---
title: "SYNC REGISTRY"
description: "Synchronize all registry files with the actual .agent/ filesystem state."
order: 23
---
# Workflow: Sync Registry

**Objective:** Keep AGENTS.md, install-state.json, and CLAUDE.md perfectly
synchronized with the actual .agent/ filesystem.

## Trigger Conditions
- Automatically as LAST STEP of any workflow that creates new .agent/ files
- Manually via /sync-registry
- Automatically when scanner detects drift
- Automatically before /release-project packaging step

## Execution Sequence

### Step 1 — Drift Detection (script-based)
Run script comparing filesystem vs install-state.json:
Output: [component]: [disk count] actual / [registry count] registered -> [IN SYNC / DRIFT]
Print full drift report before any changes.

### Step 1.5 — Version & Changelog Verification
Read `PROJECT_METADATA.md` to extract the latest `**Version**` and the newest `## Changelog` entry.
Compare with `install-state.json` and `.agent/session-context.md`.
Flag drift if versions do not match.

### Step 2 — AGENTS.md Regeneration (only if drift detected)
For each drifted component:
1. Read actual files in the directory
2. Extract name and description from each file's first 3 lines
3. Regenerate the affected AGENTS.md section
4. Preserve all other sections — surgical update only
5. Update version number at top to match PROJECT_METADATA.md

### Step 3 — install-state.json Update
Update drifted lists with actual filenames.
Update component_counts with accurate numbers.
Update the `version` field to match PROJECT_METADATA.md.
Append the latest changelog string to the `changelog` dictionary.
Update last_updated timestamp.

### Step 4 — CLAUDE.md Command Registry Sync (only if commands or personas changed)
Read all command files, extract description from YAML frontmatter.
Regenerate Section 4 (Slash Command Registry) of CLAUDE.md.
Preserve all other sections.

### Step 5 — Verification
Re-run drift detection script.
Expected: ALL components show IN SYNC.
If any still show drift: repeat Steps 2-4.

### Step 6 — Sync Report
Output:
"REGISTRY SYNC COMPLETE — [date]
Components synced: [list]
AGENTS.md: UPDATED / UNCHANGED
install-state.json: UPDATED / UNCHANGED
CLAUDE.md: UPDATED / UNCHANGED
Drift resolved: [N] components"

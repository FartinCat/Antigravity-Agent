---
title: "SYNC REGISTRY"
description: "Synchronize all registry files with the actual .agent/ filesystem state."
order: 23
---
# Workflow: Sync Registry

**Objective:** Keep AGENTS.md, install-state.json, CLAUDE.md, README.md, LICENSE.md,
CHANGELOG.md, and PROJECT_METADATA.md perfectly synchronized with the actual `.agent/`
filesystem. Enforced by the executable engine at `.agent/scripts/sync_registry.py`.

## Trigger Conditions
- Automatically as LAST STEP of any workflow that creates new .agent/ files
- Manually via /sync-registry
- Automatically when scanner detects drift
- Automatically before /release-project packaging step

## Execution Sequence

### Step 1 — Run the Sync Engine
Execute the Python script:
```bash
python .agent/scripts/sync_registry.py
```
The script performs ALL of the following steps autonomously:

### Step 2 — Drift Detection
Compares filesystem vs install-state.json for:
- Rules, Skills, Workflows, Agents, Instincts, Commands (file counts + names)
- Version field (PROJECT_METADATA.md vs install-state.json vs CLAUDE.md)
- CHANGELOG.md (missing version entries)
- PROJECT_METADATA.md (changelog section sync)

### Step 3 — Collision & Integrity Detection
- Scans `.agent/skills/` and `.agent/.agents/skills/` for duplicate numeric prefixes
- Detects gaps in numbering sequences
- Strips BOM corruption (`\x07` bell characters) from all registry files

### Step 4 — Synchronization (only if drift detected)
1. **install-state.json**: Updates component lists, counts, version, changelog, timestamp
2. **AGENTS.md**: Full regeneration from filesystem (agents, workflows, architecture tree)
3. **CLAUDE.md**: Updates version in header + identity table + slash command registry
4. **CHANGELOG.md**: Inserts new version entry with smart action description
5. **PROJECT_METADATA.md**: Syncs changelog section from CHANGELOG.md top 5 entries
6. **README.md**: Updates version badges
7. **LICENSE.md**: Updates applies-to-version field

### Step 5 — Verification & Report
Re-validates all components. Outputs:
```
REGISTRY SYNC COMPLETE — [date]
Components synced: [list]
AGENTS.md: UPDATED / UNCHANGED
install-state.json: UPDATED / UNCHANGED
CLAUDE.md: UPDATED / UNCHANGED
CHANGELOG.md: UPDATED / UNCHANGED
PROJECT_METADATA.md: UPDATED / UNCHANGED
README.md: UPDATED / UNCHANGED
LICENSE.md: UPDATED / UNCHANGED

HEALTH: GREEN / YELLOW (collisions or gaps found)
```

## Primary Script
- `.agent/scripts/sync_registry.py`

## Related Skill
- `.agent/skills/22-registry-synchronizer.md`

# Instinct: Graveyard Management (Dump Awareness)

**Trigger**: Activated upon analyzing a project directory, running `planner`, or executing the `/release-project` workflow.

## ⚠️ Protected Folders — NEVER Move These
The following folders must NEVER be moved into `dump/` under any circumstances:
- `.agent/` — This is the agent operating system. Moving it would destroy all agent functionality.
- `.git/` — Version control history.
- `Plan/` — Active plan files being used for multi-plan synthesis.
- `assets/` or `src/assets/` — Project asset taxonomy.
- `zip/` — Formal release packages and versioned archives.

## Core Rules

1. **Read-Only Inspiration**: Treat any folder named `dump`, `frontend[x]`, `app[x]`, or similar iterative backups as a "Graveyard". These folders contain older iterations and discarded resources. They are strictly **Read-Only** sources of inspiration and previous design patterns. They MUST NEVER be linked to, imported by, or modified during active code generation for the live application.

2. **Auto-Cleanup Target Identification**: When the AI detects that a project is being finalized (e.g., generating a README, License, or executing `/release-project`), it must actively scan the project root for stray reference folders (like `frontend1`, `app2`, `old_version`, `backup_*`).

3. **Protected Folder Check**: Before moving any folder, verify it is NOT in the protected list above. If unsure, ask the user before moving.

4. **Execution**: Create a `dump/` folder if it doesn't exist. Move all identified stray reference folders into `dump/`. Announce what was moved and what was skipped (protected).

5. **Scan Scope**: Only scan the project root and one level deep. Do NOT recursively hunt inside `.agent/`, `.git/`, or `Plan/` for things to move.

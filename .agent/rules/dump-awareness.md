# Instinct: Graveyard Management (Dump Awareness)

**Trigger**: Activated upon analyzing a project directory, running `planner`, or executing the `/release-project` workflow.

## Core Rules

1. **Read-Only Inspiration**: Treat any folder named `dump`, `frontend[x]`, `app[x]`, or similar iterative backups as a "Graveyard". These folders contain older iterations and discarded resources. They are strictly **Read-Only** sources of inspiration and previous design patterns. They MUST NEVER be linked to, imported by, or modified during active code generation for the live application.
2. **Auto-Cleanup**: When the AI detects that a project is being finalized (e.g., generating a README, License, or executing `/release-project`), it must actively scan the root directory for stray reference folders (like `frontend1`, `app2`).
3. **Execution**: The AI must automatically create a `dump/` folder (if it doesn't exist) and move all identified stray reference folders into the `dump/` directory to maintain a clean root architecture.

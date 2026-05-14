---
name: "source-command-sync-registry"
description: "Synchronize install-state.json and AETHER.md §13 with actual .agent/ filesystem state"
---

# source-command-sync-registry

Use this skill when the user asks to run the migrated source command `sync-registry`.

## Command Template

Run workflow `16-sync-registry.md` (or execute `python .agent/scripts/sync_registry.py`).
Detect drift between `.agent/` filesystem and registry documents.
Updates **`AETHER.md`** (§13 registry, §16 changelog, §18 session as needed), `install-state.json`, and downstream `README.md` / `LICENSE.md` when drift is detected.
Always run after adding new skills, workflows, rules, agents, or commands.

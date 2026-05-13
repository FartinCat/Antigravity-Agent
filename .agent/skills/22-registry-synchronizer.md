# Skill: Registry Synchronizer

## Purpose
Maintain perfect synchronization between the live `.agent/` filesystem and the
registry documents that describe it. This skill is backed by an **executable Python
engine** at `.agent/scripts/sync_registry.py`.

## The Executable Engine
The script at `.agent/scripts/sync_registry.py` is the **enforcement mechanism**.
It is NOT advisory documentation — it physically reads the filesystem, compares it
to `install-state.json`, and rewrites registry outputs to match reality.

Run it with:
```bash
python .agent/scripts/sync_registry.py
python .agent/scripts/sync_registry.py --no-bump
python .agent/scripts/sync_registry.py --no-bump --regen-section13   # rebuild §13 from disk only
```

## Capabilities

### A. Drift Detection
Counts actual files in each `.agent/` directory and compares them against
`install-state.json` component lists. Reports IN SYNC or DRIFT DETECTED per
component type, with specific files that are new or missing.

### B. Collision Detection
Scans `.agent/skills/` and `.agent/.agents/skills/` for duplicate numeric prefixes
(e.g., two files starting with `22-`). Also detects gaps in the numbering sequence.
Reports CLEAN or lists each collision/gap.

### C. BOM / Encoding Sanitization
After every sync, scans written files for `\x07` bell characters (remnants of
BOM encoding bugs) and strips them. Prevents corruption from propagating through
the registry chain (`install-state.json` → **`AETHER.md`**).

### D. `AETHER.md` Version & Structure Sync
Keeps **`AETHER.md`** internally consistent: title line (`# Aether Agent vX.Y.Z`),
identity table version, and **§14 Project Metadata** `**Version**:` field.

### E. Semantic Versioning
Auto-bumps patch or minor version based on `git status --porcelain` footprint:
- **Minor bump**: New files added to `.agent/rules/`, `.agent/skills/`, `.agent/workflows/`,
  `.agent/.agents/skills/`, or `.claude/commands/`
- **Patch bump**: Any other significant file changes
- **No bump**: Only registry files (`AETHER.md`, `README.md`, `LICENSE.md`, `CLAUDE.md` stub, `.agent/aether-agent-install-state.json`) changed

Registry files are explicitly excluded from triggering bumps to prevent infinite loops.

### F. Smart Changelog / Session Text
Uses **`AETHER.md` §18 Session Context** for the latest action description when available; otherwise builds a short summary from changed paths (via `git status` classification).

### G. Cross-file Propagation
Ripples the current version to:
- **`AETHER.md` §13** — full agents + workflows registry regenerated from disk
- **`AETHER.md` §16 / §18** — changelog + session entries when the engine reconciles a version
- **`README.md`** — version badges
- **`LICENSE.md`** — applies-to-version field
- **`.agent/aether-agent-install-state.json`** — version + component lists + counts (and **`.agent/antigravity-agent-install-state.json`** mirror when written)

## The Linked-File Map

```
TRIGGER                              -> AFFECTED REGISTRIES
New file in .agent/rules/            -> AETHER.md §13, .agent/aether-agent-install-state.json
New file in .agent/skills/           -> AETHER.md §13, .agent/aether-agent-install-state.json
New file in .agent/workflows/        -> AETHER.md §13, .agent/aether-agent-install-state.json
New dir in .agent/.agents/skills/    -> AETHER.md §13, .agent/aether-agent-install-state.json
New file in .agent/instincts/        -> AETHER.md §13, .agent/aether-agent-install-state.json
New file in .claude/commands/        -> AETHER.md §13, .agent/aether-agent-install-state.json
Version bump (non-registry diff)      -> AETHER.md §1/§14, .agent/aether-agent-install-state.json (+ legacy mirror), README.md, LICENSE.md
```

## Quality Gate
Before declaring sync complete:
- Component counts in **`.agent/aether-agent-install-state.json`** match actual filesystem
- **`AETHER.md` §13** lists all actual agent personas and workflows
- No numbering collisions or gaps in skills/agents
- No BOM corruption in `AETHER.md` or **`.agent/aether-agent-install-state.json`**
- **`AETHER.md` version fields** agree across §1 identity table and §14

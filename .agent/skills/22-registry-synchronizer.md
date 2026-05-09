# Skill: Registry Synchronizer

## Purpose
Maintain perfect synchronization between the live `.agent/` filesystem and the
registry documents that describe it. This skill is backed by an **executable Python
engine** at `.agent/scripts/sync_registry.py`.

## The Executable Engine
The script at `.agent/scripts/sync_registry.py` is the **enforcement mechanism**.
It is NOT advisory documentation — it physically reads the filesystem, compares it
to `install-state.json`, and rewrites every registry file to match reality.

Run it with:
```bash
python .agent/scripts/sync_registry.py
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
After every sync, scans all written files for `\x07` bell characters (remnants of
BOM encoding bugs) and strips them. Prevents corruption from propagating through
the registry chain (install-state.json → CHANGELOG.md → PROJECT_METADATA.md).

### D. CLAUDE.md Version Sync
Updates the `CLAUDE.md` header line (`# Antigravity Agent vX.Y.Z`) and the identity
table (`| **Version** | X.Y.Z |`) to match `PROJECT_METADATA.md`. This was the
single most visible drift issue in v4.0–v4.2.

### E. Semantic Versioning
Auto-bumps patch or minor version based on `git status --porcelain` footprint:
- **Minor bump**: New files added to `.agent/rules/`, `.agent/skills/`, `.agent/workflows/`,
  `.agent/.agents/skills/`, or `.claude/commands/`
- **Patch bump**: Any other significant file changes
- **No bump**: Only registry files (README, LICENSE, CHANGELOG, etc.) changed

Registry files are explicitly excluded from triggering bumps to prevent infinite loops.

### F. Smart Changelog Generation
Tries to read `.agent/session-context.md` for an action description. If none found,
constructs a fallback message from the modified file names (e.g., "Updated readme_architect.py
and 2 others") instead of the generic "Version bumped."

### G. Cross-file Propagation
Ripples the current version to all downstream files:
- `PROJECT_METADATA.md` — version field + changelog section
- `CHANGELOG.md` — new version entry
- `AGENTS.md` — full regeneration from filesystem
- `CLAUDE.md` — header + identity table + slash command registry
- `README.md` — version badges
- `LICENSE.md` — applies-to-version field
- `install-state.json` — version + component lists + counts

## The Linked-File Map

```
TRIGGER                              -> AFFECTED REGISTRIES
New file in .agent/rules/            -> AGENTS.md, install-state.json
New file in .agent/skills/           -> AGENTS.md, install-state.json
New file in .agent/workflows/        -> AGENTS.md, install-state.json
New dir in .agent/.agents/skills/    -> AGENTS.md, install-state.json
New file in .agent/instincts/        -> AGENTS.md, install-state.json
New file in .claude/commands/        -> AGENTS.md, CLAUDE.md
Version bump in PROJECT_METADATA.md  -> install-state.json, CLAUDE.md, README.md, LICENSE.md
```

## Quality Gate
Before declaring sync complete:
- Component counts in install-state.json match actual filesystem
- AGENTS.md sections list all actual files
- No file exists in `.agent/` undocumented in AGENTS.md
- No file listed in AGENTS.md that does not exist in `.agent/`
- No numbering collisions or gaps in skills/agents
- No BOM corruption in any registry file
- CLAUDE.md version matches PROJECT_METADATA.md version

# Foundational skills (`.agent/skills/`)

These files are **Aether Agent** “recipe book” skills: loaded by boot order and workflows inside this OS. They are **not** the same thing as [Cursor Agent Skills](https://cursor.com) (separate feature).

## Cursor Agent Skills: what controls list order?

Cursor discovers Agent Skills from:

- **User scope:** `%USERPROFILE%\.cursor\skills\<name>\SKILL.md` (Windows) / `~/.cursor/skills/`
- **Project scope:** `.cursor/skills/<name>/SKILL.md` under the workspace

The product UI does **not** expose a user-defined sort order for the skill picker. In practice, skills are shown in a **stable lexicographic order** (by skill folder name / path), not in the order you typed names in chat.

**Practical fix:** prefix each skill directory with a sort key, e.g. `01-babysit`, `02-canvas`, … — the same pattern already used here (`01-research-loop.md`, …).

**Built-in skills** under Cursor-managed paths (for example `skills-cursor`) are reserved for the product; use `~/.cursor/skills/` or project `.cursor/skills/` for your own.

## This folder (`.agent/skills/`)

Numeric prefixes define load order for **Aether** workflows and `sync_registry.py` collision checks. To change how often an agent *should* load a skill, edit **`AETHER.md`** boot sequence (Section 2) — renaming files here only affects ordering when rules/workflows sort by filename.

This `README.md` is excluded from `sync_registry.py` / `aether-agent-install-state.json` so it never appears as an extra numbered “skill” in the install manifest. See **`AETHER.md`** §12 for the Cursor vs Aether distinction.

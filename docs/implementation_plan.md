# Unified Agent Architecture Plan

**Status (2026-05-13):** Executed in-repo — consolidated state lives in root **`AETHER.md`**; optional **`CLAUDE.md`** stub for IDE auto-load; registry sync targets **`AETHER.md`** via `.agent/scripts/sync_registry.py`.

---

You have raised a very valid point. Maintaining version numbers and state changes across 6 different markdown files (`CHANGELOG.md`, `DEPLOY.md`, `CLAUDE.md`, `AGENTS.md`, `PROJECT_METADATA.md`, `session-context.md`) creates unnecessary friction, merge conflicts, and clutter in the root directory. 

This implementation plan proposes consolidating all these files into a single, unified state file at the root of the project.

## User Review Required

> [!WARNING]  
> Unifying `CLAUDE.md` into a custom file means some AI IDEs (like Cursor or Windsurf) that specifically look for the name `CLAUDE.md` to load custom instructions might not pick it up automatically anymore. We can either:
> 1. Keep a minimal `CLAUDE.md` that just says "Read `AETHER_OS.md` for instructions".
> 2. Name the unified file `CLAUDE.md` (so the IDE picks it up), but structure it to hold *everything* (Changelog, Metadata, etc.).
> 3. Name it `AETHER_OS.md` (or similar) and ignore IDE auto-loading.

## Open Questions

> [!IMPORTANT]  
> 1. **File Naming:** What should we name the new unified file? I propose `AETHER_OS.md` or `AGENT_STATE.md`. Alternatively, we could keep the name `CLAUDE.md` so IDEs pick up the instructions natively. Which do you prefer?
> 2. **Script Updates:** Do you want me to update the `16-sync-registry.md` and `17-auto-commit.md` workflows and their associated python scripts so they only target this single unified file instead of the 6 separate files?

## Proposed Changes

### 1. Creation of Unified Context File
We will create a single markdown file at the root of the project. Its structure will be logically divided into sections replacing the old files:

```markdown
# Aether Agent OS

## 1. System Prompt & Rules (Formerly CLAUDE.md)
[Agent identities, global instructions, formatting rules]

## 2. Project Metadata (Formerly PROJECT_METADATA.md)
[Version, Author, Tech Stack, Feature Checklist]

## 3. Agents Registry (Formerly AGENTS.md)
[List of active agents and their capabilities]

## 4. Deployment Protocol (Formerly DEPLOY.md)
[Instructions on how to deploy or package the project]

## 5. Changelog & Session Context (Formerly CHANGELOG.md & session-context.md)
[Combined sequential history of all actions, versions, and updates]
```

### 2. File Deletion
Once the data is successfully migrated, the following files will be **permanently deleted**:
- `CLAUDE.md` (Depending on your answer to Question 1)
- `docs/CHANGELOG.md`
- `docs/DEPLOY.md`
- `.agent/AGENTS.md`
- `.agent/PROJECT_METADATA.md`
- `.agent/session-context.md`

### 3. Workflow Modifications
- Update `01-scan.md` to look for the single unified file instead of `PROJECT_METADATA.md` and `session-context.md`.
- Update the sync and commit workflows so they bump the version in exactly **one** place.

## Verification Plan

### Automated Tests
- Run `/01-scan` to ensure the agent correctly reads the new unified file and doesn't crash looking for the old ones.

### Manual Verification
- Review the unified file to ensure all historical data, agent registries, and system instructions transferred perfectly.
- Ensure the root directory and `.agent/` directories are significantly cleaner.

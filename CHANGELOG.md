# Antigravity Agent Changelog

## [4.8.0] - 2026-05-11
- Updates and improvements.

## [4.8.1] - 2026-05-11
- Modified 2 other

## [4.7.0] - 2026-05-09
### Quality Hardening Release
- **Sync Engine**: Upgraded changelog generation with deduplication, category-based descriptions, and --no-bump flag
- **CLAUDE.md**: Auto-updated Section 12 (Project Structure) with actual component counts (23 rules, 22 skills, 24 workflows, 23 agents)
- **Boot Sequence**: Converted skill loading from bulk (97KB) to on-demand with 8 core skills always loaded
- **Workflows**: Expanded 6 thin workflows (06, 10, 11, 12, 19, 20) to 4-5KB each with failure paths and output formats
- **Archive Rule**: Updated 09-archive-management.md content to match renamed terminology
- **Instincts**: Fixed count from 6 to 5 (excluded README.md from component list)
- **Commands**: Added 4 missing workflow commands to CLAUDE.md registry table

## [4.2.4] - 2026-05-09
- Generated knowledge-antigravity-capabilities.md documenting core AOS features.

## [4.1.1] - 2026-05-09
- Executed /21-release-project God Mode pipeline. Migrated all previous zip files to archived/old-versions/. Packaged core system to archived/current-version/antigravity-agent-v4.1.1.zip. Generated strict commercial license and market evaluation.

## [4.1.0] - 2026-05-09
### Added
- **Self-Maintenance Framework**: Introduced `23-sync-registry.md` workflow and `/sync-registry` command to automatically synchronize the `.agent/` filesystem state with `install-state.json`, `AGENTS.md`, and `CLAUDE.md`.
- **Output Organization (Rule 20)**: Implemented strict output routing. All agent-generated output (plans, reports, evaluations) is now routed to `docs/` subdirectories to prevent root folder pollution.
- **Destructive Operation Safety (Rule 21)**: Added a mandatory authorization gate and Move-First Protocol. Files are now moved to `archived/` instead of being permanently deleted, with all actions logged in `DELETION_REGISTRY.md`.
- **Registry Drift & Root Pollution Scanner**: Upgraded `/scanner` to detect drift between the filesystem and registry files, and to flag stray output files in the root directory.

### Changed
- **Workflow Renumbering**: Renumbered all 22 workflows strictly from 01 to 22 according to the 5-phase software lifecycle.
- **Specialist Personas**: Rewrote `code-reviewer`, `security-auditor`, and `test-engineer` with comprehensive 80+ line frameworks including severity models and composition rules.
- **File Encodings**: Stripped BOM markers and fixed corrupted UTF-8 em-dashes across all `.agent/workflows/*.md` files.

## [4.0.0] - 2026-05-08
### Added
- **MCP Integration Pipeline**: Integrated 21st-dev-magic, StitchMCP, figma-remote, mongodb, playwright, and supabase into the ecosystem.
- **Probabilistic Instincts**: Implemented 5 passive instinct modules to govern behavior without explicit prompting.
- **Specialist Personas Base**: Stubs for Code Reviewer, Security Auditor, and Test Engineer introduced.

### Changed
- Converted all legacy workflows to strictly follow the 5-phase framework.
- Upgraded repository documentation to premium God-Mode state.

## [3.0.0] - 2026-05-05
- Stabilized automated project lifecycle and fixed workflow visibility.
- God Mode pipeline established.

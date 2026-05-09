# Antigravity Agent Changelog

## [4.2.0] - 2026-05-09
- Version bumped.

## [4.1.1] - 2026-05-09
- Executed /21-release-project God Mode pipeline. Migrated all previous zip files to rchived/old-versions/. Packaged core system to rchived/current-version/antigravity-agent-v4.1.1.zip. Generated strict commercial license and market evaluation.

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

### Fixed
- Fixed numbering violation for `mcp-auditor` (changed from Agent 21 to Agent 20 to comply with Rule 00).
- Cleaned up extraneous Advanced Operations Matrix data from `13-knowledge-capture.md`.

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

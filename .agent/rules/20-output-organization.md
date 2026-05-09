---
rule: 20-output-organization
priority: HIGH
---
# Rule 20: Output Organization — No Root Pollution

## The Law
All agent-generated output documents go into typed subdirectories under docs/,
never the project root.

## Why This Exists
After 10 sessions the project root becomes a junk drawer of MARKET_EVALUATION.md,
SCAN_REPORT.md, MASTER_PLAN.md, and WEEKLY_REVIEW files. The root is for entry
points only: README.md, CLAUDE.md, package.json, LICENSE.md, CHANGELOG.md.

## The docs/ Structure
docs/
├── market-evaluations/   -> MARKET_EVALUATION_{NN}.md
├── master-plans/         -> MASTER_PLAN_{NN}.md
├── scan-reports/         -> SCAN_REPORT_{NN}.md
├── specs/                -> SPEC_{feature-name}_{NN}.md
├── research/             -> RESEARCH_{topic}_{NN}.md
├── audit-reports/        -> AUDIT_REPORT_{NN}.md
├── release-notes/        -> RELEASE_NOTES_v{version}.md
├── weekly-reviews/       -> WEEKLY_REVIEW_{YYYY-MM-DD}.md
└── ai/
    ├── requirements/
    ├── design/
    ├── planning/
    └── implementation/

## Numbering Protocol
Before writing any output file:
1. Check if subdirectory exists. Create it if not.
2. Count existing files matching the pattern.
3. Use next number zero-padded to 2 digits: 00, 01, 02...
4. Never overwrite existing output — always increment.

## Root File Exceptions (ONLY these belong at root)
README.md, CLAUDE.md, DEPLOY.md, LICENSE.md, CHANGELOG.md,
PROJECT_METADATA.md, .mcp.json, all dotfiles,
source entry points: package.json, pyproject.toml, Cargo.toml, go.mod

## Migration of Existing Root Files
When /scanner or /onboard detects root-level output files:
1. Flag as Root Pollution anomaly
2. Offer to move them to docs/ subdirectories
3. Rename with sequence numbers during move

## Enforcement
- /scanner flags root output files as anomaly
- /cross-agent-validator checks workflow outputs landed in docs/

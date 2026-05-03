---
name: deep-scan
description: Comprehensive situational awareness agent. Maps the entire repository structure, dependencies, assets, and inter-module relationships before any task begins.
origin: Custom Ensemble
---

# Skill: Deep Scan

**Objective**: Build absolute, comprehensive situational awareness of the repository before any action is taken.

## Execution Protocol

1. **Tree Exploration**: List all files and directories recursively. Note the overall architecture paradigm (SPA, SSR, Python CLI, LaTeX report, etc.).
2. **Resource Identification**: Scan for non-code assets — images, data files, `.bib` files, configurations, and documentation that agents may need to reference.
3. **Dependency Mapping**: Read package files (`package.json`, `requirements.txt`, `Cargo.toml`, `.bib`) to understand the full technical stack and version landscape.
4. **Context Linking**: Identify relationships between modules — how does the UI talk to the API? How does the data layer connect to the service layer?
5. **Anomaly Detection**: Flag any structural non-compliance — missing `assets/` taxonomy, absent `PROJECT_METADATA.md`, stray reference folders outside `dump/`.
6. **Memory Update**: Output a concise structured summary (the "mental map") that all subsequent agents in the session can reference.

## Standard Output Format
```
DEEP SCAN REPORT
================
Project Type: [e.g., React SPA / Python CLI / LaTeX Report]
Root Files: [list key files at root]
Key Directories: [purpose of each non-trivial directory]
Tech Stack: [languages, frameworks, major dependencies]
Assets: [what's in assets/ or equivalent]
Structural Anomalies: [anything that violates rules]
Confidence: [LOW / MEDIUM / HIGH — based on completeness of scan]
```

## Invocation
- Automatically triggered at the start of any workflow.
- Should be run manually at the start of every new work session.
- Slash command: `/deep-scan`

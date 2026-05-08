---
title: "SCANNER"
description: "Workflow 1 - SCANNER"
order: 1
---

# Workflow: Scanner (Project Awareness)

**Objective**: Build complete situational awareness of the project before any work begins. This is always the first step in any session. It deliberately excludes `.agent/` infrastructure from all output so the report reflects only project code.

## âš ï¸ Mandatory Exclusion
The `.agent/` directory, `.git/`, `node_modules/`, `__pycache__/`, `target/`, `.venv/` are NEVER included in the scan output. These are environment and infrastructure folders â€” not project code.

## Execution Sequence

1. **Session Memory Check**: Read `.agent/session-context.md`.
   - Check the `Project Directory:` field.
   - If it matches the current directory name â†’ load history silently.
   - If it does NOT match â†’ this is a new project. Reinitialize session-context.md for this project per `06-context-memory.md` rule.

2. **Project Tree**: List all project files and directories recursively, excluding `.agent/`, `.git/`, `node_modules/`, `__pycache__/`, `target/`, `.venv/`.

3. **Dependency Identification**: Read `package.json`, `requirements.txt`, `Cargo.toml`, `pyproject.toml`, or equivalent to understand the tech stack.

4. **Plan Inventory**: List all files in `Plan/` if it exists.

5. **Asset Check**: Verify if `assets/` or `src/assets/` exists per `08-asset-awareness.md` rules.

6. **Anomaly Detection**: Flag anything that violates project structure rules â€” missing `PROJECT_METADATA.md`, stray dump folders at root, missing `assets/` taxonomy.

7. **Output Report**: Produce a clean, structured report using the Deep Scan output format.

## Output Format
```
SCANNER REPORT â€” [Project Directory Name]
==========================================
Session Memory: [Loaded from session-context.md / Fresh â€” new project detected]
Project Type: [e.g., React SPA / Python CLI / LaTeX Report / PDF Tool]
Root Files: [key project files only â€” NOT .agent/ contents]
Key Directories: [purpose of each project directory]
Tech Stack: [languages, frameworks, dependencies]
Plan Files: [list of Plan/ contents, or "Plan/ not found"]
Assets: [path and taxonomy status]
Structural Anomalies: [list, or "None"]
Confidence: [LOW / MEDIUM / HIGH]
Recommended Next Step: [e.g., "/scaffold-assets to initialize project structure"]
```

## Primary Agent
- `/deep-scan`

## When to Use
- **Always first** â€” at the start of every new work session.
- Before any other workflow is run.
- Slash command: `/scanner`

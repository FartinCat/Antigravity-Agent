---
name: deep-scan
description: Comprehensive situational awareness agent. Maps the project repository structure, dependencies, assets, and inter-module relationships. Never scans .agent/ infrastructure folders.
origin: Custom Ensemble
---

# Skill: Deep Scan

**Objective**: Build absolute, comprehensive situational awareness of the **project** before any action is taken.

## ⚠️ Critical Exclusion Rule — READ FIRST
**NEVER scan, list, report, include, or reference the `.agent/` directory or any of its sub-folders or files in any output.**
The `.agent/` folder contains agent infrastructure — rules, skills, workflows, and context memory. It is NOT part of the project being developed. Including it in scan output is noise that confuses planning, creates false structural anomalies, and pollutes reports.

**Excluded at all times (treat as invisible):**
- `.agent/` and everything inside it
- `.git/` and everything inside it
- `node_modules/` and `__pycache__/` (build artifacts)
- `target/` (Rust build output)
- `.venv/`, `.vscode/`, `.idea/` (environment folders)

**Only report on project files** — source code, configuration files, assets, plans, documentation, tests, and dependency manifests.

---

## Execution Protocol

1. **Tree Exploration**: List all files and directories recursively, **excluding the folders listed above**. Note the overall architecture paradigm (SPA, SSR, Python CLI, LaTeX report, etc.).
2. **Resource Identification**: Scan for non-code assets — images, data files, `.bib` files, configurations, and documentation that agents may need to reference.
3. **Dependency Mapping**: Read package files (`package.json`, `requirements.txt`, `Cargo.toml`, `.bib`) to understand the full technical stack and version landscape.
4. **Context Linking**: Identify relationships between modules — how does the UI talk to the API? How does the data layer connect to the service layer?
5. **Anomaly Detection**: Flag any structural non-compliance — missing `assets/` taxonomy, absent `PROJECT_METADATA.md`, stray reference folders outside `dump/`. **Do NOT flag the `.agent/` folder as an anomaly — it is expected and correct.**
6. **Memory Update**: Output a concise structured summary (the "mental map") that all subsequent agents in the session can reference.

## Standard Output Format
```
DEEP SCAN REPORT
================
Project Directory: [name of the current project folder]
Project Type: [e.g., React SPA / Python CLI / LaTeX Report]
Root Files: [list key project files at root — NOT .agent/ contents]
Key Directories: [purpose of each non-trivial project directory]
Tech Stack: [languages, frameworks, major dependencies]
Assets: [what's in assets/ or equivalent]
Plan Files Found: [list files in Plan/ if present]
Structural Anomalies: [anything that violates rules — .agent/ is NOT an anomaly]
Confidence: [LOW / MEDIUM / HIGH — based on completeness of scan]
```

## Invocation
- Automatically triggered at the start of any workflow.
- Should be run manually at the start of every new work session.
- Slash command: `/deep-scan`
\n## Advanced Operations Matrix\n\n- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.\n- **Simulation & Modeling**: For scientific simulations, employ 
umpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.\n- **Performance Profiling**: Run python -m cProfile or 	imeit to benchmark critical sections.\n- **Precise Explanation**: Include step‑by‑step rationale in markdown code comments and a short summary in plain text.\n- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re‑raise if unrecoverable.\n

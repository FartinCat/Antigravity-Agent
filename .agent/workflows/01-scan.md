---

title: "SCANNER"

description: "Build situational awareness and map directories."

order: 1

---



# Workflow: Scanner (Project Awareness)







**Objective**: Build complete situational awareness of the project before any work begins. This is always the first step in any session. It deliberately excludes `.agent/` infrastructure from all output so the report reflects only project code.







## Mandatory Exclusion



The `.agent/` directory, `.git/`, `node_modules/`, `__pycache__/`, `target/`, `.venv/` are NEVER included in the scan output. These are environment and infrastructure folders — not project code.







## Execution Sequence







1. **Session Memory Check**: Read **`AETHER.md` Section 18 (Session Context)**.



   - Check the `Project Directory:` field.



   - If it matches the current directory name → load history silently.



   - If it does NOT match → this is a new project. Reinitialize **§18 Session Context** for this project per `06-context-memory.md` rule.







2. **Project Tree**: List all project files and directories recursively, excluding `.agent/`, `.git/`, `node_modules/`, `__pycache__/`, `target/`, `.venv/`.







3. **Dependency Identification**: Read `package.json`, `requirements.txt`, `Cargo.toml`, `pyproject.toml`, or equivalent to understand the tech stack.







4. **Plan Inventory**: List all files in `Plan/` if it exists.







5. **Asset Check**: Verify if `assets/` or `src/assets/` exists per `08-asset-awareness.md` rules.







6. **Anomaly Detection**: Flag anything that violates project structure rules — missing root **`AETHER.md`**, stray archived folders at root, missing `assets/` taxonomy.

### Step 6a — Workflow Sequence Verification
Run a check of the `.agent/workflows/` directory to ensure workflows are sequentially numbered (e.g., `01`, `02`, ... `N`).
Report:
  WORKFLOW SEQUENCE: NOMINAL / ANOMALY DETECTED
  If anomaly: "Gaps or misordering detected in workflows. Suggest renaming files to restore sequential order."

### Step 6b — Registry Drift Detection
Run a script (not raw file reads) that checks:
- Count .agent/rules/*.md vs install-state.json installed_rules count
- Count .agent/skills/*.md vs installed_foundational_skills count
- Count .agent/workflows/*.md vs installed_workflows count
- Count .agent/.agents/skills/ directories vs installed_skills count
- Compare install-state.json version with **`AETHER.md` title** (`# Aether Agent vX.Y.Z`) and identity table version

Report:
  REGISTRY STATUS: IN SYNC / DRIFT DETECTED
  If drift: "[component]: [N] on disk, [M] in registry — run /sync-registry"
  If version mismatch: "VERSION MISMATCH — run /sync-registry"

### Step 6c — Root Pollution Detection
Check project root for output files that belong in docs/:
Patterns to flag: *EVALUATION*.md, *MASTER_PLAN*.md, *SCAN_REPORT*.md,
*RESEARCH_*.md, *AUDIT_REPORT*.md, WEEKLY_REVIEW_*.md
Exclude: README.md, CLAUDE.md, AETHER.md, LICENSE.md

Report:
  ROOT POLLUTION: CLEAN / [N] files found
  If found: list them and ask "Run /migrate-docs to move to docs/?"

### Step 6d — Numbering Collision Detection
Scan `.agent/skills/` and `.agent/.agents/skills/` for duplicate numeric prefixes.
For each directory, extract the leading number from each file/folder name and check for duplicates.
Also check for gaps in the numbering sequence.
Report:
  NUMBERING: CLEAN / COLLISION DETECTED
  If collision: "[directory]: prefix [NN] shared by [file1], [file2]"
  If gap: "[directory]: position [NN] is missing"

### Step 6e — Encoding Integrity Check
Scan all `.md` files in the project root and `.agent/` for bell characters (`\x07`) — remnants of BOM encoding bugs.
Also scan `.agent/aether-agent-install-state.json` string values.
Report:
  ENCODING: CLEAN / [N] files contain BOM corruption
  If found: "Run `python .agent/scripts/sync_registry.py` to auto-sanitize"

### Step 6f — AETHER.md Version Consistency
Read **`AETHER.md`**: title line (`# Aether Agent vX.Y.Z`), identity table `| **Version** | … |`, and **§14 Project Metadata** `**Version**:` line. All three MUST match.
Report:
  AETHER.md VERSION: IN SYNC / DRIFT DETECTED
  If drift: "Version fields disagree inside AETHER.md — edit manually or run /sync-registry"

### Step 6g — Cross-Reference Validation
Scan all workflow files for hardcoded version numbers (e.g., `v3.0.0`, `v4.0.0`).
Flag any workflow that references a specific version number instead of reading from **`AETHER.md` §14 / §1**.
Also check that Rule 20 (output routing) is not contradicted by any workflow step that says "at project root".
Report:
  CROSS-REFERENCES: CLEAN / [N] issues found
  If found: list each file and the hardcoded reference
### Step 6h — Asset Utility Verification
Scan `assets/` for any images or files, and cross-reference them against `.md` files in the repository. Also evaluate `docs/` and `archived/` subdirectories for active use.
Report:
  ORPHANED ASSETS: CLEAN / DETECTED
  If detected: list the orphaned files/folders and suggest "Orphaned assets detected. Propose deletion per 06-asset-pruning instinct."

7. **Output Report**: Produce a clean, structured report using the Deep Scan output format.









## Output Organization (Rule 20)
1. Check if `docs/scan-reports` exists, create if not.
2. Count existing files.
3. Output report to `docs/scan-reports/SCAN_REPORT_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.

## Output Format



```



SCANNER REPORT — [Project Directory Name]



==========================================



Session Memory: [Loaded from AETHER.md §18 / Fresh — new project detected]



Project Type: [e.g., React SPA / Python CLI / LaTeX Report / PDF Tool]



Root Files: [key project files only — NOT .agent/ contents]



Key Directories: [purpose of each project directory]



Tech Stack: [languages, frameworks, dependencies]



Plan Files: [list of Plan/ contents, or "Plan/ not found"]



Assets: [path and taxonomy status]



Structural Anomalies: [list, or "None"]

Registry Status: [IN SYNC / DRIFT DETECTED — details]

Root Pollution: [CLEAN / N output files at root]
Orphaned Assets: [CLEAN / DETECTED — details]



Confidence: [LOW / MEDIUM / HIGH]



Recommended Next Step: [e.g., "/scaffold-assets to initialize project structure"]

*(Logic: If registry drift AND root pollution -> "Run /sync-registry then move files to docs/". If only registry drift -> "Run /sync-registry". If only root pollution -> "Move files to docs/ or run /migrate-docs".)*



```







## Primary Agent



- `/deep-scan`







## When to Use



- **Always first** — at the start of every new work session.



- Before any other workflow is run.



- Slash command: `/scanner`




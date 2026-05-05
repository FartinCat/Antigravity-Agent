# Instinct: Workflow Orchestration

**Trigger**: Creation, modification, or presentation of system workflows in the `.agent/workflows/` directory.

## Core Rules

### Rule 1 — Filename Prefixing
To ensure that the slash-command UI and file explorers display workflows in their correct execution order, all workflows must use a two-digit numeric prefix followed by a hyphen.
- Format: `XX-name.md` (e.g., `01-scanner.md`, `02-scaffold-assets.md`).
- Sub-steps within the same phase should use letters (e.g., `04a-build-website.md`, `04b-build-app.md`).

### Rule 2 — Metadata Alignment
The internal metadata in the YAML frontmatter must exactly match the filename prefix.
- `order: X`: Must match the numeric prefix.
- `description: "Step X — ..."`: The description must explicitly state the step number as the first part of the string.

### Rule 3 — Logical Sequence
The following sequence is the official Antigravity execution pipeline:
1. **Awareness** (`01-scanner`)
2. **Initialization** (`02-scaffold-assets`)
3. **Planning** (`03-multi-plan-synthesis`)
4. **Implementation** (`04a/b-build-*`)
5. **Testing** (`05-tdd`)
6. **Debugging** (`06-fix-bugs`)
7. **Documentation** (`07-write-report`)
8. **Audit** (`08-cross-agent-validator`)
9. **Finalization** (`09-release-project`)

### Rule 4 — Enforcement
When generating a new workflow, always check the existing directory to find the next available step number. Do not skip numbers unless reserved for future expansions.

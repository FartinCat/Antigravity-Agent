# Instinct: System-Wide Orchestration

**Trigger**: Creation, modification, or presentation of ANY system component in the `.agent/` directory.

## Core Rules

### Rule 1 — Lifecycle Prefixing
To ensure logical execution flow and UI clarity, all components must follow the 5-phase lifecycle numbering system.

| Phase | Range | Purpose |
| :--- | :--- | :--- |
| **P0: Governance** | 00 | Orchestration and system rules. |
| **P1: Awareness** | 01–05 | Discovery, intelligence, and context. |
| **P2: Strategy** | 06–10 | Planning, strategy, and design. |
| **P3: Execution** | 11–20 | Implementation, language specialists, and work. |
| **P4: Quality** | 21–30 | Bug hunting, verification, and audit. |
| **P5: Finalization** | 31–40 | Release, licensing, and semantic git commits. |

### Rule 2 — Component-Specific Numbering
- **Workflows**: Must be numbered 01–99 sequentially.
- **Rules**: Must be numbered 00–99 sequentially.
- **Skills**: Must be numbered 01–99 sequentially.
- **Agents**: Must be numbered 01–99 sequentially.

### Rule 3 — Golden Path Enforcement
When suggesting actions, the agent must favor components in their logical order:
1.  **Scanner** (`01`) → **Onboarding** (`02`)
2.  **Planner** (`04`) → **Synthesis** (`05`)
3.  **Specialist Agents** (`07–11`)
4.  **Antibug** (`12`) → **Validator** (`10`)
5.  **Release** (`11`) → **Commit** (`12`)

### Rule 4 — Mandatory YAML Frontmatter (Visibility Gate)
**ALL workflow files** in `.agent/workflows/` MUST begin with a YAML frontmatter block. Without this block, the workflow will be **invisible** in the IDE `+` menu and unusable.

**Required format** (first lines of every workflow file):
```yaml
---
description: "Step XX — [concise description of what the workflow does]."
order: XX
---
```

- `description`: Must start with `"Step XX —"` where XX matches the numeric file prefix.
- `order`: Must be an integer matching the numeric file prefix.
- **Violation**: If a workflow file is created without this frontmatter, it MUST be flagged immediately and corrected before any other work proceeds.

### Rule 5 — Pre-Commit Frontmatter Audit
Before running `/12-auto-commit`, the agent MUST verify that ALL workflow files contain valid frontmatter. Run this check:
```
For each .md in .agent/workflows/: first line must be "---"
```
If any file fails this check, halt and fix before generating commits.

---
> "Order is the first law of heaven."

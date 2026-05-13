---
title: "README ARCHITECT"
description: "Dynamically updates the README.md to accurately reflect all active agents, workflows, and skills."
order: 22
---

# Workflow: README Architect

**Objective**: Ensure the main `README.md` file is an accurate, perfectly synced reflection of the `.agent/` architecture. 

## Execution Sequence

**This workflow is fully autonomous.** The agent must simply execute the python engine:

1. **Run Engine**: Execute `python .agent/scripts/readme_architect.py`
2. **Verification**: Run `git diff README.md` to verify the tables and flowchart updated successfully.

The Python engine handles:
- **Architecture Scan**: Parses `.agent/` and `.claude/` directories to identify all active rules, skills, workflows, and commands.
- **Deep Extraction**: Extracts actual YAML `description` and `trigger` attributes from `SKILL.md` and frontmatter.
- **Flowchart Generation**: Rebuilds the Mermaid flowchart dynamically based on workflow numbers.
- **README Injection**: Injects updated tables and graphs into `README.md`.

## Execution Trigger
- Triggered automatically during `/20-release-project` OR manually via `/22-readme-architect`.
- **Must execute BEFORE** `/23-sync-registry` so that the updated README correctly receives the finalized version badge during the sync.

## Primary Agent
- `16-readme-architect`

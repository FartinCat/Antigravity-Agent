---
title: "README ARCHITECT"
description: "Dynamically updates the README.md to accurately reflect all active agents, workflows, and skills."
order: 22
---

# Workflow: README Architect

**Objective**: Ensure the main `README.md` file is an accurate, perfectly synced reflection of the `.agent/` architecture. 

## Execution Sequence

1. **Architecture Scan**: Parse the `.agent/` and `.claude/` directories to identify all active rules, skills, workflows, and commands.
2. **Table Generation**: Generate updated Markdown tables for:
   - Specialist Agents & Commands
   - Workflows & Slash Commands
   - Foundational Skills
3. **Trigger Synchronization**: Ensure the "Trigger Phrase" or "Slash Command" for each entity is explicitly listed in the tables.
4. **README Injection**: Inject these updated tables into `README.md`, completely replacing the old tables, while preserving the preamble, branding, and core manifesto.

## Execution Trigger
- Triggered automatically during `/20-release-project` OR manually via `/22-readme-architect`.
- **Must execute BEFORE** `/23-sync-registry` so that the updated README correctly receives the finalized version badge during the sync.

## Primary Agent
- `16-readme-architect`

---
description: Read the /Plan folder, compare multiple AI plans, and generate a master implementation strategy.
---

# Workflow: Multi-Plan Synthesis

**Objective**: Convert multiple external AI perspectives into a single, optimized, conflict-free implementation file.

## Steps

1. **Detection**: Check for the existence of a `Plan/` folder in the root directory. If it does not exist, halt and instruct the user to create it and populate it with plan files (e.g., `planbychatgpt.txt`, `planbyclaude.txt`, `planbygrok.txt`).
2. **Deep Scan**: Invoke `/deep-scan` to capture the current true state of the repository before comparing plans.
3. **Ingestion**: Read all files inside `Plan/`. Log how many files were found and their names.
4. **Synthesis (Synthesizer Agent)**:
   - Compare strategies from each file.
   - Resolve contradictions by checking actual project resources from the `deep-scan` output.
   - Select the most robust, performance-oriented, and bug-free approach for each component.
   - Log every conflict found and the resolution ruling.
5. **Output**: Create `MASTER_PLAN.md` at the project root with the full structured plan, conflict log, and phase breakdown.
6. **Validation**: Run a final check to ensure the plan covers all user requirements and adheres to `core.md` instincts.

## Primary Agent
- `.agent/.agents/skills/synthesizer`

## Dependent Skills
- `.agent/.agents/skills/deep-scan` (must run before synthesis)
- `.agent/skills/code-synthesis.md` (conflict resolution logic)

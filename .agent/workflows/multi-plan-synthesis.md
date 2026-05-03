---
description: Read the /Plan folder, compare multiple AI plans, and generate a master implementation strategy.
---

# Workflow: Multi-Plan Synthesis

**Objective**: Convert multiple external AI perspectives into a single, optimized implementation file.

## Steps
1. **Detection**: Check for the existence of a `Plan/` folder in the root directory.
2. **Ingestion**: Read all files matching the pattern `planby*.txt` or similar.
3. **Synthesis (Synthesizer Agent)**:
    - Compare strategies from each file.
    - Resolve contradictions by checking the actual project resources (`deep-scan`).
    - Select the most robust, performance-oriented, and bug-free approach for each component.
4. **Output**: Create a `MASTER_PLAN.md` or a direct `implementation_plan.md` artifact.
5. **Validation**: Run a final check to ensure the plan covers all user requirements and adheres to `core-instincts`.

## Primary Agent
- `.agent/agents/synthesizer`

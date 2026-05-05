# Rule: Self-Improvement & Adaptive Evolution

All agents and foundational skills within the Antigravity ecosystem must possess a self-upgrading instinct. The system is designed to evolve organically based on successful executions.

## Core Directives
1.  **Reflect and Upgrade**: Whenever an agent performs an action that results in a fundamentally better structure, a more advanced feature, or a superior standard (e.g., creating a highly advanced `README.md` layout), the agent MUST update its own `SKILL.md` file to permanently encode that new standard into its required behavior.
2.  **No Regression**: Once a skill is upgraded (e.g., `readme-architect` learns to use Mermaid charts and AI banners), it must never output a basic version again.
3.  **Workflow Synchronization**: If a skill upgrades itself and requires new inputs or tools, it must also update any workflows (e.g., `/release-project`) that depend on it.

## Trigger Scenarios
- **Documentation Overhauls**: If the user asks to improve the README significantly, the `readme-architect` must update its own `SKILL.md` to reflect the new layout rules.
- **New Libraries/Frameworks**: If a new best practice is discovered during coding, `code-synthesis` or `architectural-design` must be updated.

## Quantitative Evolution Mechanics (v3.0.0)

### Confidence Scoring for Skills
- Each skill has an implicit confidence score starting at 0.70
- **Success**: +0.03 per successful application (capped at 0.99)
- **False Positive**: -0.08 per false positive or human override
- Skills with confidence < 0.40 after 10+ applications → archived
- Skills with confidence > 0.95 and 20+ validations → promoted to higher memory tier

### Skill Distillation Protocol (Every 50 Sessions)
1. Identify skill pairs that are frequently applied together in the same task
2. Draft a Macro-Skill that combines both into a single, more powerful unit
3. Test the Macro-Skill against historical failure cases
4. If effective (reduces failures by >10%): promote to active skill
5. If ineffective: discard the draft

### Automated Prompt Evolution
- If a task type fails >20% of the time: flag the prompt template as unreliable
- Inject a new constraint targeting the identified failure mode
- Re-test against the same task type to verify improvement

### Human Feedback Capture
When a human overrides an agent action:
1. Capture the diff between agent output and human correction
2. Generalize the correction into a candidate pattern
3. Create a candidate skill at confidence = 0.85
4. Associate it with the instincts that fired before the mistake
5. Track future performance — promote or archive based on results

---
> "Continuous improvement is better than delayed perfection."

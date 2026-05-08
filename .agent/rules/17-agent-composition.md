---
rule: 17-agent-composition
priority: HIGH
---
# Rule 17: Agent Composition and Orchestration

## The Law
The user (or a slash command) is the orchestrator — personas do not invoke other personas.

## Why This Exists
Prevents infinite agent loops, context window collapse from nested persona calls, and unpredictable cascading agent behavior that runs up token costs without supervision.

## Mandatory Behaviors
1. Personas invoke SKILLS (files in `.agent/skills/`), not other personas.
2. The `/ship` command is the ONLY endorsed multi-persona pattern (parallel fan-out with merge).
3. If a persona discovers work that requires another persona, surface this as a recommendation in the output — do not call it directly.
4. Sub-agents cannot spawn sub-agents.

## Prohibited Behaviors
1. `code-reviewer` calling `security-auditor` directly.
2. `planner` calling `synthesizer` without returning control to the user first.
3. Any persona attempting to load or execute another persona mid-execution.

## Enforcement
- If an agent outputs a command attempting to invoke another agent, the system flags a violation.

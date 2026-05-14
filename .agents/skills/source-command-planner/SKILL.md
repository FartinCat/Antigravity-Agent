---
name: "source-command-planner"
description: "Create a strategic implementation plan — single-agent version of /plan"
---

# source-command-planner

Use this skill when the user asks to run the migrated source command `planner`.

## Command Template

Invoke `.agent/.agents/skills/04-planner`.

1. Read **`AETHER.md` §18 Session Context** — understand the goal fully before planning
2. Break the goal into atomic, testable tasks
3. Assign complexity: **simple** / **medium** / **complex**
4. Identify dependencies between tasks
5. Output `TASK_PLAN.md`
6. Get user confirmation before execution begins

**Rule:** Never start implementation without user approval of the plan.

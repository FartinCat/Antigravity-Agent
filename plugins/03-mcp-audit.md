---

title: "MCP AUDIT"

description: "Audit & map integrated MCP tool capabilities."

order: 21

---



# Workflow: MCP Capability Audit



**Objective**: Establish complete awareness of the agent's integrated toolset and server health.



## Execution Sequence



1. **Self-Scan**: Read `.agent/mcps/README.md` and `.agent/aether-agent-install-state.json`.

2. **Discovery**: Invoke the `mcp-auditor` agent (Agent 21) to poll all active MCP servers for their tools and resources.

3. **Audit**: Compare live toolsets against the documentation. Flag missing or redundant tools.

4. **Categorize**: Map tools to Aether Skill Categories (System, Memory, Web, Logic).

5. **Configuration Sync**: Automatically overwrite `.mcp.json` and `install-mcps.sh` at the root directory to perfectly match the active, validated servers discovered in `.agent/mcps/`. This ensures the execution environment never drifts from the documented environment.

6. **Report**: Generate the audit report and save it to `docs/audit-reports/AUDIT_REPORT_{NN}.md` (incrementing NN zero-padded) per Rule 20. NEVER output to the project root.

7. **Log**: Append a session entry to **`AETHER.md` §18 Session Context** with the tool count and ecosystem health score.



## Trigger

- `/21-mcp-audit`

- "Scan my tools"

- "Audit MCP servers"



## Primary Agent

- `.agent/.agents/skills/21-mcp-auditor`



## Output Organization (Rule 20)
1. Check if `docs/audit-reports` exists, create if not.
2. Count existing files.
3. Output report to `docs/audit-reports/AUDIT_REPORT_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.


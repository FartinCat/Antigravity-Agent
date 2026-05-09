# MCP Capability Audit Protocol

This protocol defines the technical procedure for auditing the Model Context Protocol (MCP) servers integrated into the Antigravity Agent. It is the only protocol authorized to bypass the `.agent/` exclusion rule for infrastructure discovery.

## Objective
To map, validate, and summarize the operational capabilities (tools, resources, and endpoints) available to the agent via MCP.

## Execution Sequence

### Step 1 — Configuration Ingestion
1. Read `.agent/mcps/README.md` to identify the documented servers.
2. Read `.agent/antigravity-agent-install-state.json` to verify installation timestamps and versions.
3. Locate and read the MCP configuration file (e.g., `mcp_config.json`) if present in the project root or `.agent/`.

### Step 2 — Live Discovery
For each identified server, the agent must:
1. **Identify Tools**: Call `list_tools` to see available functions.
2. **Identify Resources**: Call `list_resources` to see available data sources.
3. **Check Status**: Verify if the server responds. If a server is documented but not responding, flag it as **INACTIVE**.

### Step 3 — Capability Mapping
Categorize the discovered tools into functional buckets:
- **Storage/Memory**: Persistent data handling.
- **I/O & Networking**: Fetching, HTTP, or external API access.
- **System/OS**: Local file operations, shell access, or system info.
- **Logic/Reasoning**: Specialized thinking or processing tools.
- **Project Specific**: Tools custom-built for the current repository.

### Step 4 — Conflict & Redundancy Check
Identify if multiple MCP servers provide overlapping tools (e.g., two different `fetch` tools). Recommend a "Preferred Provider" to avoid agent confusion.

### Step 5 — Operational Intelligence Report
Generate a structured report (The MCP Audit) including:
- **Active Servers**: List of responding servers.
- **Inactive/Ghost Servers**: Documented but non-responsive.
- **Tool Inventory**: Categorized list of all available commands.
- **Resource Inventory**: Available data buckets.
- **Health Score**: Overall ecosystem readiness.

## Output Format
```markdown
# MCP AUDIT REPORT — [Date]

## Ecosystem Health: [GREEN / YELLOW / RED]

## Active Servers
- [Server Name] ([Version]): [Status Summary]

## Capability Map
- **[Category Name]**: [List of tools/resources]

## Infrastructure Anomalies
- [e.g., Ghost server detected: @server-name documented in README but not in config]
- [e.g., Port conflict detected for server-X]

## Operational Intelligence Summary
Total Tools: [N]
Total Resources: [N]
Confidence in Tools: [HIGH / MEDIUM / LOW]
```

## Guardrails
- **DO NOT** modify the MCP configuration files during the audit unless explicitly instructed.
- **DO NOT** share the content of private resources scanned during the audit; only report on the *availability* of the resource.
- **EXEMPTION**: This skill is authorized to read `.agent/mcps/` and `.agent/antigravity-agent-install-state.json`.

# Aether Agent — MCP Integrations

This directory documents the Model Context Protocol (MCP) servers integrated into the Aether ecosystem.

## Configured Servers (`.mcp.json`)

1. **Memory** (`@modelcontextprotocol/server-memory`): Cross-session persistent knowledge graph.
2. **Git** (`@modelcontextprotocol/server-git`): Read repositories, analyze diffs, and interact with the local git history.
3. **Fetch** (`mcp-server-fetch`): Read and process external web content.
4. **Bash/Sequential Thinking** (`@modelcontextprotocol/server-sequential-thinking`): Safe execution environment and chain-of-thought processing.
5. **Postgres** (`@modelcontextprotocol/server-postgres`): Database introspection and querying.

## Installation

Run `./install-mcps.sh` from the project root to install the necessary global packages.

## Usage in Workflows

Skills in `.agent/skills/` may explicitly require these MCPs to function (e.g., `18-memory-management.md` requires the `memory` MCP). If an MCP is unavailable, agents fall back gracefully (Rule 04).

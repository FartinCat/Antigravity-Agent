#!/bin/bash

echo "Installing MCP Servers..."
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-postgres
pip install mcp-server-fetch

echo "MCP Servers installed successfully."

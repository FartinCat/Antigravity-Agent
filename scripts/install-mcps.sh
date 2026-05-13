#!/bin/bash

echo "Installing MCP Servers..."
npm install -g @21st-dev/magic-mcp-server
npm install -g @stitch-ui/mcp-server
npm install -g @modelcontextprotocol/server-figma
npm install -g @modelcontextprotocol/server-mongodb
npm install -g @modelcontextprotocol/server-playwright
npm install -g @supabase/mcp-server

echo "MCP Servers installed successfully."

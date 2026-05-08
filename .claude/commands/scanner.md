---
description: Map the entire repository before any work begins — project-aware deep scan
---

Invoke `.agent/.agents/skills/01-deep-scan`.

Actions:
1. List all directories and files
2. Identify tech stack (languages, frameworks, tools)
3. Find entry points, config files, test directories
4. Detect anti-patterns: missing tests, no .gitignore, dump folders, hardcoded secrets
5. Read `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` (whichever exists)

**IMPORTANT:** The `.agent/` folder is **EXCLUDED** from all scans. It is the agent's OS, not project code.

Output: structured `SCAN_REPORT.md` + update `session-context.md`.

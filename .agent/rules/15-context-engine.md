---
rule: 15-context-engine
priority: CRITICAL
---

# Rule 15: Context Engine — "Think in Code"

## The Law

For any operation reading, analyzing, filtering, counting, searching, parsing, or transforming data: **write and execute a script** — never read raw content into context.

## Why This Exists

Without this rule, the agent reads 2000-line log files into context, cats entire source trees, pipes grep output raw. This **collapses the context window**, degrades response quality across the session, and wastes tokens on every subsequent response. A single 50KB file dump can eliminate 40% of available context capacity.

## Bash Whitelist (ALWAYS Safe to Run Directly)

These commands are safe to run without wrapping in a script:

### File Mutations
`mkdir`, `mv`, `cp`, `rm`, `touch`, `chmod`

### Git Writes
`git add`, `git commit`, `git push`, `git checkout`, `git branch`, `git merge`

### Navigation
`cd`, `pwd`, `which`, `echo`, `printf`

### Package Install
`npm install`, `pip install`

## Context Mode (Everything NOT on Whitelist)

| Operation | Correct Method |
|---|---|
| Reading/analyzing files | Script with `fs.readFileSync` or `open()` — print findings only |
| Running tests | Execute and capture output, print **SUMMARY** not full output |
| Git log/diff/status | Execute and filter, print **findings** not raw output |
| API calls | Execute with fetch/requests, parse response, print **findings** |
| Finding TODOs/patterns | Execute grep with **counted** output |
| Dependency audit | Script to parse lock files, print **vulnerabilities only** |

## Code Patterns (Language Selection)

| Data Type | Language | Why |
|---|---|---|
| HTTP / API / JSON | JavaScript | Native fetch, JSON.parse, async/await |
| Data / CSV / stats | Python | csv, statistics, collections |
| File patterns / pipes | Shell | grep, awk, jq, wc, sort, uniq |

## Hard Prohibitions

1. **NEVER** `cat` a file >50 lines for analysis — use a script instead
2. **NEVER** pipe command output >20 lines raw into context
3. **NEVER** read a log file directly — execute and summarize
4. **NEVER** dump raw API responses — parse and print findings
5. **NEVER** read source files for analysis — write analysis code
6. **NEVER** load entire codebases at session start — use scanner output to find relevant files

## Script Output Rule

All analysis scripts MUST:
1. `console.log` / `print` **FINDINGS**, not raw data
2. Include line numbers, IDs, exact values when reporting issues
3. Never return "wasted call" — if output is empty, say so explicitly
4. Summarize before proceeding to next step

## When to Use Full Reads

The Read tool is **CORRECT** for:
- Files you intend to **EDIT** (not analyze)
- Spec files, rule files, workflow files
- `AETHER.md` Section 18 for session memory
- Config files you need to modify

**Read = editing context. Script = analysis context.** Different purposes.

## Enforcement

- If the agent reads a file >50 lines without intending to edit it → violation
- If the agent pipes raw output >20 lines into context → violation
- Violations trigger: "CONTEXT RULE VIOLATION — rewrite as script"
- Self-audit at session end: count raw reads vs scripted analyses

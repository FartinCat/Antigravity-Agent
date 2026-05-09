# Skill: Registry Synchronizer

## Purpose
Maintain perfect synchronization between the live .agent/ filesystem and the
four registry documents that describe it.

## The Linked-File Map

TRIGGER                              -> AFFECTED REGISTRIES
New file in .agent/rules/            -> AGENTS.md rules section, install-state.json installed_rules
New file in .agent/skills/           -> AGENTS.md skills section, install-state.json installed_foundational_skills
New file in .agent/workflows/        -> AGENTS.md workflows section, install-state.json installed_workflows
New dir in .agent/.agents/skills/    -> AGENTS.md agents section, install-state.json installed_skills
New file in .agent/instincts/        -> AGENTS.md instincts section, install-state.json installed_instincts
New file in .claude/commands/        -> AGENTS.md commands section, CLAUDE.md command registry
New file in .claude/agents/          -> AGENTS.md personas section, /ship command description
Server added to .mcp.json            -> .agent/mcps/README.md, install-state.json mcp_servers
Version bump in PROJECT_METADATA.md  -> install-state.json version, CLAUDE.md identity block

## Drift Detection (script-based — never reads files raw)
Write a shell or Python script that:
1. Counts actual files in each .agent/ directory
2. Reads expected counts from install-state.json component_counts
3. Compares them
4. Outputs: DRIFT DETECTED or IN SYNC for each component type
5. If drift: lists the specific files that are new or missing

## Sync Protocol
When drift is detected:
1. AGENTS.md: regenerate affected sections from actual filesystem
2. install-state.json: update affected lists and component_counts, update last_updated
3. CLAUDE.md: update only if commands or personas changed
4. Never change version field during sync — version bumps are intentional

## Quality Gate
Before declaring sync complete:
- Component counts in install-state.json match actual filesystem
- AGENTS.md sections list all actual files
- No file exists in .agent/ undocumented in AGENTS.md
- No file listed in AGENTS.md that does not exist in .agent/

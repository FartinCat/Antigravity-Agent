---
description: "Step 12 — Analyze all uncommitted changes and generate atomic, Conventional Commit commands."
order: 12
---

# Workflow: Auto-Commit Pipeline

**Objective**: Produce a structured list of atomic `git add` + `git commit` commands presented in a single copyable bash block.

## Execution Sequence

1. **State Capture**: Run `git status` and `git diff --stat`.
2. **Artifact Check**: Identify and exclude build artifacts.
3. **Diff Analysis**: Analyze each modified file's intent.
4. **Semantic Grouping**: Apply `12-commit-semantics.md` for atomic chunking.
5. **Message Generation**: Agent `19-git-commit-author` drafts messages per `11-git-awareness.md`.
6. **Output**: **CRITICAL: Present ALL commands inside a single triple-backtick bash block.** This allows the user to copy the entire sequence with one click.

## Output Format
```bash
# ═══════════════════════════════════════════════════
# AUTO-COMMIT REPORT — [Project Name]
# Generated: [Date]
# ═══════════════════════════════════════════════════

# 1/N — [Category]
git add [files]
git commit -m "[prefix]: [message]"

# [Additional Commits...]

# N/N — Version bump (always last)
git add PROJECT_METADATA.md .agent/antigravity-agent-install-state.json
git commit -m "chore(version): bump to v[X.Y.Z]"
```

## Primary Agent
- `.agent/.agents/skills/19-git-commit-author`

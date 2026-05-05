---
description: "Step 10 — Analyze all uncommitted changes and generate atomic, Conventional Commit commands."
order: 11
---

# Workflow: Auto-Commit Pipeline

**Objective**: After any major or minor update session, automatically analyze the full set of uncommitted changes and produce a structured list of atomic `git add` + `git commit` commands for the user to review and execute.

## When to Use
- At the **end of any work session** where multiple files were changed.
- After any workflow completes (e.g., after `/build-app`, `/fix-bugs`, or `/release-project`).
- Manually via `/auto-commit`.

## Execution Sequence

1. **State Capture**: Run `git status` and `git diff --stat` to list all modified, untracked, staged, and deleted files.

2. **Artifact Check**: Identify build artifacts or temporary files that should NOT be committed (`.log`, `dist/`, `node_modules/`, `__pycache__/`). Warn the user if any are detected.

3. **Diff Analysis**: Run `git diff` on each modified file to understand the nature of the change (new feature, bug fix, documentation, refactor, etc.).

4. **Semantic Grouping**: Apply the `05-commit-semantics.md` foundational skill to split the changes into logical, atomic chunks grouped by domain boundary.

5. **Message Generation**: The `13-git-commit-author` agent drafts each commit message following the `10-git-awareness.md` Conventional Commits rule.

6. **Output**: Present ALL commit commands as a single, numbered, copyable code block. **Do NOT auto-execute.** The user will review and run them manually.

7. **Version Reminder**: If a version bump occurred during the session (check `PROJECT_METADATA.md` diff), ensure the version bump commit is the **last** commit in the sequence.

## Output Format
```bash
# ═══════════════════════════════════════════════════
# AUTO-COMMIT REPORT — [Project Name]
# Generated: [Date]
# Total Commits: [N]
# ═══════════════════════════════════════════════════

# 1/N — [Category]
git add [files]
git commit -m "[prefix]: [message]"

# 2/N — [Category]
git add [files]
git commit -m "[prefix]: [message]"

# ...

# N/N — Version bump (always last)
git add PROJECT_METADATA.md .agent/antigravity-agent-install-state.json
git commit -m "chore(version): bump to v[X.Y.Z]"
```

## Primary Agent
- `.agent/.agents/skills/13-git-commit-author`

## Dependent Skills
- `.agent/skills/05-commit-semantics.md` (diff chunking logic)
- `.agent/rules/10-git-awareness.md` (Conventional Commits enforcement)

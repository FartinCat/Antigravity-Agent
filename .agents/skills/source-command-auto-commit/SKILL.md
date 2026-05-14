---
name: "source-command-auto-commit"
description: "Analyze all staged changes and create atomic Conventional Commits"
---

# source-command-auto-commit

Use this skill when the user asks to run the migrated source command `auto-commit`.

## Command Template

Invoke `.agent/.agents/skills/19-git-commit-author` + workflow `12-auto-commit.md`.

1. Read `git diff --staged` (use script to summarize, not raw dump)
2. Group changes by type: `feat` / `fix` / `chore` / `docs` / `test` / `refactor`
3. Write commit messages with scope and body
4. Never combine unrelated changes in one commit

Format: `type(scope): description`

```
[optional body explaining WHY, not WHAT]
[optional footer: BREAKING CHANGE, Closes #issue]
```

**Pre-commit check:** Verify all workflow files have valid YAML frontmatter (Rule 00, Rule 5).

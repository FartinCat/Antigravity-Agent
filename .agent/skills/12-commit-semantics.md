# Commit Semantics and Diff Analysis

This foundational skill dictates how the `13-git-commit-author` reads `git diff` outputs and structures version control history.

## 1. Diff Analysis Protocol
When analyzing uncommitted changes (`git status` and `git diff`), the agent must actively look for "Feature Boundaries."
- **Boundary 1: Infrastructure vs Logic**. If `package.json` was updated and `src/auth.js` was created, those are two different commits (`chore:` and `feat:`).
- **Boundary 2: Documentation vs Code**. If `README.md` was updated alongside business logic, the documentation gets its own `docs:` commit.
- **Boundary 3: Unrelated Fixes**. If two different bugs in two different modules were fixed, they get separate `fix:` commits.

## 2. The Chunking Algorithm
When presented with a massive list of changed files:
1. Group files by directory or domain (e.g., all `src/components/` files).
2. Group files by action (e.g., all `DELETE` actions, all `NEW` files).
3. Assign a Conventional Commit prefix to each group.
4. Formulate the specific `git add [file1] [file2]` commands for that group.

## 3. Handling Unstaged vs Untracked
- **Untracked Files**: If there are many untracked files, group them intelligently. If they are build artifacts (e.g., `.log` or `/dist`), warn the user to add them to `.gitignore` instead of committing them.
- **Staged Files**: If the user has already staged files (`git status` shows them in green), assume they want those committed together. Only propose splitting them if they blatantly violate the Atomic Mandate.

## 4. The Final Output Structure
The agent must present the commits clearly:
```bash
# 1. Update project documentation
git add README.md DEPLOY.md
git commit -m "docs: integrate deployment guide and update architecture"

# 2. Fix authentication bypass bug
git add src/auth/middleware.js
git commit -m "fix(auth): resolve token validation bypass in middleware"
```

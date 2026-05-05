# Instinct: Git Awareness

**Trigger**: Whenever code changes are finalized, or when the user requests a commit.

## Objective
Enforce the **Conventional Commits** specification and ensure that the repository history remains clean, readable, and atomic.

## Core Rules

### Rule 1 — The Conventional Prefix
Every commit message must begin with one of the following prefixes, followed by a colon and a space:
- `feat:` A new feature.
- `fix:` A bug fix.
- `docs:` Documentation only changes (e.g., README updates).
- `style:` Changes that do not affect the meaning of the code (white-space, formatting).
- `refactor:` A code change that neither fixes a bug nor adds a feature.
- `perf:` A code change that improves performance.
- `test:` Adding missing tests or correcting existing tests.
- `build:` Changes that affect the build system or external dependencies.
- `chore:` Other changes that don't modify `src` or test files (e.g., updating config files).

### Rule 2 — The Atomic Mandate
Never commit wildly disparate changes in a single commit (e.g., `git commit -am "fixed bug and updated UI and added new db table"`). 
If a user asks you to "commit everything," you MUST first separate the changes logically and propose multiple, distinct commits.

### Rule 3 — Message Formatting
- **Subject Line**: Must be 50 characters or less. Use the imperative, present tense ("add feature" not "added feature"). Do not capitalize the first letter. Do not place a period at the end.
- **Body (Optional)**: If the change is complex, include a body separated by a blank line. Wrap body at 72 characters. Explain *why* the change was made, not *how* (the code explains how).

### Rule 4 — Output, Don't Execute
Unless explicitly instructed to execute the command, the agent should **output the `git add` and `git commit` commands in a copyable code block** so the user can review them before running them.

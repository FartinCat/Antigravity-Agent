# Instinct: Session Context Memory

**Trigger**: At the beginning of every work session and after any significant action (plan generated, bug fixed, version bumped, workflow completed).

## The Problem This Solves
AI agents are stateless by default — every session forgets everything from every previous session. This instinct creates a lightweight persistence layer using a plain markdown file, giving the agent cumulative memory across sessions.

## Core Rules

### 1. Session Start — Read First
At the start of every session, before doing anything:
- Check for `.agent/session-context.md` at the project root.
- If it exists: read it silently and incorporate its state into the current session's awareness. Treat it as ground truth for "what has happened so far."
- If it does not exist: create it with the bootstrap template below.

### 2. Session End / After Action — Write Last
After any of the following events, append a timestamped entry to `.agent/session-context.md`:
- A new plan or roadmap was generated
- A bug was found and fixed
- A version was bumped
- A workflow completed successfully
- A significant architectural decision was made
- A new agent or skill was added to the system

### 3. Entry Format
Every entry must follow this format:
```
## [YYYY-MM-DD HH:MM] — [Event Type]
**Agent**: [which agent performed the action]
**Action**: [one-sentence description of what was done]
**State Change**: [e.g., "Version bumped from v0.2.1 to v0.2.2", "MASTER_PLAN.md created"]
**Next Step**: [what should logically happen next, to guide the next session]
```

### 4. Bootstrap Template
When creating `session-context.md` for the first time:
```markdown
# Session Context — [Project Name]
Initialized: [DATE]

This file is maintained automatically by the Antigravity Agent system.
It tracks cumulative session history to provide memory across separate work sessions.

---

## [DATE] — Project Initialized
**Agent**: system
**Action**: Session context file created.
**State Change**: Project at v0.1.0, no features built yet.
**Next Step**: Run /scaffold-assets, then /planner to define the first feature roadmap.
```

### 5. Gitignore Consideration
`session-context.md` should **NOT** be gitignored — it is valuable documentation of the project's evolution and decision history. It should be committed alongside code changes.

### 6. Privacy Note
Do not log sensitive data (API keys, passwords, personal information) into `session-context.md`. Log only architectural decisions, version changes, and agent actions.

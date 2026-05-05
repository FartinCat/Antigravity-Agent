# Instinct: Session Context Memory

**Trigger**: At the beginning of every work session and after any significant action (plan generated, bug fixed, version bumped, workflow completed).

## The Problem This Solves
AI agents are stateless by default — every session forgets everything from every previous session. This instinct creates a lightweight persistence layer using a plain markdown file, giving the agent cumulative memory across sessions.

Additionally: when the `.agent/` folder is **copied to a new project directory**, the `session-context.md` from the previous project must NOT bleed into the new project. Each project directory gets its own independent session memory.

---

## Core Rules

### Rule 1 — Session Start: Detect Project Directory FIRST
At the very start of every session, before doing anything else:

**Step A — Detect current project directory.**
Read the name of the folder that directly contains the `.agent/` folder. This is the **Active Project Name**. For example:
- If `.agent/` is inside `PDF_annotator/`, the Active Project Name is `PDF_annotator`.
- If `.agent/` is inside `my-react-app/`, the Active Project Name is `my-react-app`.
- If `.agent/` is inside `Antigravity Agent/` (the source repo), the Active Project Name is `Antigravity Agent`.

**Step B — Check `.agent/session-context.md`.**
- If the file does **NOT** exist → Create it using the bootstrap template. Set `Project Directory:` to the Active Project Name detected in Step A.
- If the file **DOES** exist → Read the `Project Directory:` field from its header.
  - **If `Project Directory:` matches the Active Project Name** → Read the full history silently and incorporate it as session memory. ✅
  - **If `Project Directory:` does NOT match the Active Project Name** → This `.agent/` folder was copied from another project. **Archive the old context** by appending a notice, then **reinitialize the file** with a fresh bootstrap for the current project. Never lose old context — archive it below a separator line.

**Archive format when project mismatch is detected:**
```markdown
---
⚠️ ARCHIVED CONTEXT — Original Project: [old project name]
The .agent/ folder was migrated from [old name] to [new name].
Context below belonged to the original project and is kept for reference only.

[OLD CONTENT HERE]
---
# Session Context — [NEW Project Name]
Initialized: [DATE — NEW DATE]
Project Directory: [NEW project folder name]
...fresh bootstrap continues...
```

---

### Rule 2 — Session End / After Action — Write Last
After any of the following events, append a timestamped entry to `.agent/session-context.md`:
- A new plan or roadmap was generated
- A bug was found and fixed
- A version was bumped
- A workflow completed successfully
- A significant architectural decision was made
- A new agent or skill was added to the system

### Rule 3 — Entry Format
Every entry appended must follow this format:
```
## [YYYY-MM-DD HH:MM] — [Event Type]
**Agent**: [which agent performed the action]
**Action**: [one-sentence description of what was done]
**State Change**: [e.g., "Version bumped from v0.2.1 to v0.2.2", "MASTER_PLAN.md created"]
**Next Step**: [what should logically happen next, to guide the next session]
```

### Rule 4 — Bootstrap Template
When creating `session-context.md` for the first time in a new project:
```markdown
# Session Context — [DETECTED PROJECT DIRECTORY NAME]
Initialized: [DATE]
Project Directory: [DETECTED PROJECT DIRECTORY NAME]

This file is maintained automatically by the Antigravity Agent system.
It tracks cumulative session history for THIS project only.
Do not manually edit Project Directory: — it is used for migration detection.

---

## [DATE] — Project Initialized
**Agent**: system
**Action**: Session context file created for project "[DETECTED PROJECT DIRECTORY NAME]".
**State Change**: .agent/ system deployed. No project features built yet.
**Next Step**: Run /scaffold-assets to initialize the project structure, then /planner to define the first feature roadmap.
```

### Rule 5 — Commit Policy
`session-context.md` should **NOT** be gitignored — it is valuable documentation of the project's evolution and decision history. It should be committed alongside code changes.

### Rule 6 — Privacy
Do not log sensitive data (API keys, passwords, personal information). Log only architectural decisions, version changes, and agent actions.

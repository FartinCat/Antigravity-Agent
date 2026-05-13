# Instinct: Session Context Memory

**Trigger**: At the beginning of every work session and after any significant action (plan generated, bug fixed, version bumped, workflow completed).

## The problem this solves

Agents are stateless by default. This instinct defines **where** cumulative session memory lives and how to detect when the `.agent/` folder was copied into a **new** project directory so history does not bleed across projects.

---

## Canonical location (all IDEs)

**Primary:** Root **`AETHER.md` → Section 18 (Session Context)**.

- At session start: read §18, especially the `Project Directory:` line in the §18 header block.
- If `Project Directory:` matches the folder that **contains** `.agent/` → treat §18 body as trusted session memory.
- If it does **not** match → the `.agent/` tree was migrated. **Archive** the old §18 content below a clear separator, then **bootstrap** a fresh §18 header + first entry for the new project (same archive pattern as before, but the file target is always `AETHER.md`).

**Session end / milestones:** append timestamped entries to **`AETHER.md` §18** (same entry format as the historical `session-context.md` format below).

---

## Legacy: `.agent/session-context.md` (Antigravity / older tooling)

Some external scripts or IDEs may still **mention** `.agent/session-context.md`. For this repository:

- **Do not** maintain a second long-form log there if `AETHER.md` exists — it creates drift.
- If a tool **cannot** read the repo root, add a **tiny pointer stub** at `.agent/session-context.md` whose sole job is to tell the agent to open **`AETHER.md` Section 18** (optional; not required when the IDE reads the repo root).

---

## Entry format (append to `AETHER.md` §18)

```
### [YYYY-MM-DD HH:MM] — [Event type]
**Agent**: [which agent performed the action]
**Action**: [one-sentence description]
**State Change**: [e.g. version bump, file created]
**Next Step**: [what should happen next]
```

---

## Privacy & commits

Do not log secrets. Session history in **`AETHER.md` §18** is meant to be **committed** with the repo when it documents decisions and releases (same policy as before for session-context).

# DEPLOY.md — Deploying Antigravity Agent to a New Project

This guide solves the migration problem: copying only the `.agent/` system (not the whole Antigravity Agent repo) into another project directory, cleanly, without flooding it.

---

## What to Copy

You only ever need to copy the **`.agent/` folder** into your new project. Everything else in the Antigravity Agent repo (README.md, LICENSE.md, PROJECT_METADATA.md, HOW-TO-USE.md, dump/, Plan/) belongs to this source project and should NOT be copied to other projects.

```
Antigravity Agent/           ← Source repository (do not copy all of this)
├── .agent/                  ← ✅ Copy ONLY this folder
│   ├── rules/
│   ├── skills/
│   ├── workflows/
│   ├── .agents/
│   ├── AGENTS.md
│   ├── session-context.md
│   └── antigravity-agent-install-state.json
├── README.md                ← ❌ Do not copy (belongs to this repo)
├── LICENSE.md               ← ❌ Do not copy (belongs to this repo)
├── HOW-TO-USE.md            ← ❌ Do not copy (belongs to this repo)
└── PROJECT_METADATA.md      ← ❌ Do not copy (belongs to this repo)
```

---

## Method 1 — rsync (Recommended for Linux/WSL/macOS)

### The Correct Command
```bash
rsync -av --exclude='.git' \
  "/mnt/d/Git_Work/Antigravity Agent/.agent/" \
  "/mnt/d/Git_Work/Project/YOUR_PROJECT_NAME/.agent/"
```

**The trailing slash on the source path is intentional.** It means "copy the contents of `.agent/` into the destination `.agent/` folder" — not the folder itself.

### Why the Trailing Slash Matters
```bash
# ✅ CORRECT: Copies contents of .agent/ into destination .agent/
rsync -av "Antigravity Agent/.agent/" "my-project/.agent/"

# ❌ WRONG (no trailing slash on source): Creates "my-project/.agent/.agent/"
rsync -av "Antigravity Agent/.agent" "my-project/.agent/"

# ❌ WRONG (backslash): Causes terminal to hang waiting for more input on Linux/WSL
rsync -av "Antigravity Agent/.agent/" "my-project/.agent\"
```

### Full Example (WSL path style)
```bash
# Deploy to a project called PDF_annotator
rsync -av --exclude='.git' \
  "/mnt/d/Git_Work/Antigravity Agent/.agent/" \
  "/mnt/d/Git_Work/Project/PDF_annotator/.agent/"
```

---

## Method 2 — Windows Explorer / File Manager
1. Navigate to `D:\Git_Work\Antigravity Agent\`
2. Right-click the `.agent` folder → Copy
3. Navigate to `D:\Git_Work\Project\YOUR_PROJECT_NAME\`
4. Paste (Ctrl+V)

This copies the entire `.agent/` folder as a sub-directory. It is safe and produces the correct result.

---

## Method 3 — PowerShell (Windows, no WSL)
```powershell
# From PowerShell in any directory:
Copy-Item -Recurse -Force `
  "D:\Git_Work\Antigravity Agent\.agent" `
  "D:\Git_Work\Project\YOUR_PROJECT_NAME\.agent"
```

---

## After Copying — First Steps in the New Project

1. **Open your AI IDE** (Cursor, Windsurf, VS Code) or chat interface in the new project directory.
2. **Run `/scanner`** — this is always the first step. It will:
   - Detect that `session-context.md` has a different `Project Directory:` than the current folder.
   - Archive the old project's context below a separator.
   - Initialize a fresh `session-context.md` for your new project.
3. **Run `/scaffold-assets`** — creates `assets/` taxonomy and a fresh `PROJECT_METADATA.md` for the new project.
4. **Proceed with your workflow.**

---

## Troubleshooting

### "Terminal hangs after command"
You used a backslash `\` at the end of a path inside quotes. In Linux/WSL, `\"` is an escape sequence that tells the terminal the quote hasn't closed yet. Press `Ctrl+C` to cancel and rewrite the command using forward slashes `/`.

### "All agent files appeared in my project root"
You ran rsync with a trailing slash on the source but NO target `.agent/` sub-path. Example of the wrong command: `rsync -av "Antigravity Agent/.agent/" "my-project/"`. This dumps the contents directly into `my-project/`, not into `my-project/.agent/`. To fix: delete the files that were created at root, then re-run with `"my-project/.agent/"` as the destination.

### "I see a nested .agent/.agent/ folder"
You ran rsync WITHOUT a trailing slash on the source. Example: `rsync -av "Antigravity Agent/.agent" "my-project/.agent/"`. The source without trailing slash copies the folder itself, not just contents. To fix: move the nested folder contents up one level, or delete and re-run with the trailing slash.

### "session-context.md still shows old project name"
This is expected on the first run after migration. Run `/scanner` — the `context-memory.md` rule will detect the mismatch and reinitialize the context file automatically for the new project.

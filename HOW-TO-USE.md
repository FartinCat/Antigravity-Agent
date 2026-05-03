# How to Use the Antigravity Agent System

This guide explains exactly how to invoke every agent and workflow — whether you're in a smart AI IDE or a plain chat window like Claude.ai or ChatGPT.

---

## The Two Ways to Use This System

### Method A — AI IDE with Native Agent Support (Cursor, Windsurf, VS Code + Copilot Agent Mode)
These tools natively read the `.agent/` folder and register agents as clickable buttons.

**Using a slash command:**
1. Open the AI chat panel in your IDE.
2. Type the slash command (e.g., `/planner`) followed by your request.
3. The IDE reads the corresponding `SKILL.md` as the system prompt automatically.

**Using a workflow (+ button):**
1. Click the `+` button in the chat bar.
2. Select the workflow you want (e.g., `build-website`).
3. The IDE runs each step in sequence using the agents defined in the workflow file.

> **Tip**: If agents don't appear, check that your IDE supports `.agent/` folder discovery. Cursor and Windsurf do by default. For others, check their documentation for "custom agent" or "slash command" configuration.

---

### Method B — Plain Chat Interface (Claude.ai, ChatGPT, Gemini, etc.)
These tools don't read your local file system. You need to bring the agent to the conversation manually.

**To use a single agent manually:**
1. Open the agent's `SKILL.md` file (e.g., `.agent/.agents/skills/planner/SKILL.md`).
2. Copy its full contents.
3. Start a new chat conversation.
4. Paste the SKILL.md content as your **first message**, prefixed with:
   > "You are operating under the following rules for this conversation: [paste SKILL.md here]"
5. Then send your actual task as the next message.

**Quick Reference — what to paste for each agent:**

| What you want to do | File to copy and paste |
|---|---|
| Create a phased project plan | `.agent/.agents/skills/planner/SKILL.md` |
| Map your entire repo before starting | `.agent/.agents/skills/deep-scan/SKILL.md` |
| Find and fix bugs | `.agent/.agents/skills/antibug/SKILL.md` |
| Merge multiple AI plans into one | `.agent/.agents/skills/synthesizer/SKILL.md` |
| Build a polished web UI | `.agent/.agents/skills/web-aesthetics/SKILL.md` |
| Write an academic report / dissertation | `.agent/.agents/skills/scientific-writing/SKILL.md` |
| Fix LaTeX citations and bibliography | `.agent/.agents/skills/latex-bib-manager/SKILL.md` |
| Evaluate project market value | `.agent/.agents/skills/market-evaluator/SKILL.md` |
| Generate a commercial license | `.agent/.agents/skills/commercial-license/SKILL.md` |
| Build a great README | `.agent/.agents/skills/readme-architect/SKILL.md` |
| Enforce TDD on your code | `.agent/.agents/skills/tdd-guide/SKILL.md` |

**To use a workflow manually in chat:**
Workflows are multi-step sequences. Run them by working through each step in order, using the relevant agent for each step:
1. Open `.agent/workflows/[workflow-name].md`
2. Read the Execution Sequence.
3. For each step, paste the corresponding agent's SKILL.md and give it the task.
4. Carry the output of each step into the next conversation as context.

---

## Everyday Usage Examples

### "I want to start a new feature"
1. Paste `planner/SKILL.md` → ask: *"Create a phased plan for adding user authentication to my Python Flask app."*
2. Take the plan output → paste `tdd-guide/SKILL.md` → ask: *"Start the TDD cycle for Phase 1 of this plan: [paste plan]"*

### "Something is broken and I don't know why"
1. Paste `deep-scan/SKILL.md` → ask: *"Here is my project structure: [paste file tree]. Map it and identify anomalies."*
2. Take the scan output → paste `antibug/SKILL.md` → ask: *"Run a full diagnostic on this codebase context: [paste scan output + relevant code]"*

### "I have plans from ChatGPT and Claude and want the best of both"
1. Create a `Plan/` folder in your project root.
2. Save ChatGPT's plan as `Plan/planbychatgpt.txt`, Claude's as `Plan/planbyclaude.txt`.
3. Paste `synthesizer/SKILL.md` → paste both plan files → ask: *"Synthesize these into a MASTER_PLAN.md"*

### "I want to release my project"
Run the `release-project` workflow manually:
1. `market-evaluator/SKILL.md` → evaluate the codebase
2. `commercial-license/SKILL.md` → generate the license
3. `readme-architect/SKILL.md` → generate the README

---

## The Research Loop (What Makes Agents "Deep")
Every agent in this system is designed to run a **Research Loop** before answering. When you paste a SKILL.md, it will first scan available context, check for contradictions, identify gaps, and give you a confidence score — before diving into the actual output. Let it do this. Don't skip past it. The deeper the scan, the better the output.

---

## Session Context Memory
After each session, the system will update `.agent/session-context.md` with what happened. At the start of your next session, paste this file's contents into the chat alongside the SKILL.md so the agent has memory of previous work.

---

## Agent Quick-Reference Card

| Slash Command | Purpose | Brand Color |
|---|---|---|
| `/planner` | Strategic roadmaps | Purple `#8B5CF6` |
| `/deep-scan` | Repo mapping | Emerald `#10B981` |
| `/antibug` | Bug hunting + patches | Red `#EF4444` |
| `/synthesizer` | Multi-AI plan merging | — |
| `/web-aesthetics` | Premium UI enforcement | — |
| `/scientific-writing` | Academic tone | — |
| `/latex-bib-manager` | Citation management | — |
| `/market-evaluator` | Commercial valuation | — |
| `/commercial-license` | License generation | — |
| `/readme-architect` | Documentation builder | — |
| `/tdd-guide` | Test-driven development | Emerald `#10B981` |

---

> "Programs must be written for people to read, and only incidentally for machines to execute." — Harold Abelson

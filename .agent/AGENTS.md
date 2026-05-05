# Antigravity Agent — v2.2.0

A portable AI operating system. Copy the `.agent/` folder into any project directory and the entire skill + workflow ecosystem activates immediately.

---

## ⚠️ Critical Deployment Rules

1. **The `.agent/` folder is NOT project code.** It is agent infrastructure. All scans, diagnostics, and reports exclude it.
2. **Always run `/scanner` first** at the start of every session. It reads `session-context.md`, detects the project directory, and maps the project before any work begins.
3. **`session-context.md` is project-aware.** When you copy `.agent/` to a new project, the agent detects the directory mismatch and initializes fresh context for the new project automatically.

---

## 🚀 Deployment (Copying to a New Project)

Use `rsync` to copy the `.agent/` folder **contents** into your target project directory:

```bash
# Copy .agent/ contents into a new project (Linux/WSL)
rsync -av --exclude='.git' "/path/to/Antigravity Agent/.agent/" "/path/to/your-project/.agent/"
```

See `DEPLOY.md` at the root of this repository for the full migration guide and common pitfalls.

---

## 🔧 Slash Commands (Single Agents)

Type the command in the AI chat panel followed by your task description.

| # | Command | Agent | Purpose |
| :--- | :--- | :--- | :--- |
| **01** | **`/scanner`** | 01-deep-scan | Project-aware repo mapping. Excludes `.agent/`. Always run first. |
| **02** | **`/ask`** | 02-ask | Precision query agent for architectural and logic doubts. |
| **03** | **`/planner`** | 03-planner | Strategic breakdown and phased roadmap generation. |
| **04** | **`/synthesizer`** | 04-synthesizer | Merge multiple AI plans from `Plan/` into `MASTER_PLAN.md`. |
| **05** | **`/tdd-guide`** | 05-tdd-guide | Strict Red-Green-Refactor test-driven development. |
| **06** | **`/antibug`** | 06-antibug | Deep logic auditing, historical pattern analysis, exact patches. |
| **07** | **`/web-aesthetics`** | 07-web-aesthetics | Premium UI enforcement — fonts, colors, micro-animations. |
| **08** | **`/scientific-writing`** | 08-scientific-writing | Academic tone, LaTeX formatting, dissertation writing. |
| **09** | **`/latex-bib-manager`** | 09-latex-bib-manager | Citation sequencing, `.bib` cleanup, float anchoring. |
| **10** | **`/readme-architect`** | 10-readme-architect | Premium `README.md` generation. |
| **11** | **`/market-evaluator`** | 11-market-evaluator | Codebase market value assessment and pricing strategy. |
| **12** | **`/commercial-license`** | 12-commercial-license | Custom commercial license generation. |
| **13** | **`/commit-author`** | 13-git-commit-author | Analyze diffs and generate atomic Conventional Commit commands. |

---

## ⚡ Workflows (+ Button — In Sequence)

Use these from the `+` button in the chat bar. **Run in order** — each workflow builds on the previous one.

| # | Workflow | Purpose | Key Agents |
| :-- | :--- | :--- | :--- |
| **01** | `/scanner` | Map the project before anything else. Session memory check included. | `01-deep-scan` |
| **02** | `/scaffold-assets` | Initialize `assets/` taxonomy and `PROJECT_METADATA.md`. | — |
| **03** | `/multi-plan-synthesis` | Merge all plans in `Plan/` into `MASTER_PLAN.md`. | `04-synthesizer` → `01-deep-scan` |
| **04a** | `/build-website` | End-to-end web app pipeline. | `03-planner` → `07-web-aesthetics` → `05-tdd-guide` → `06-antibug` |
| **04b** | `/build-app` | End-to-end software app pipeline. | `03-planner` → `05-tdd-guide` → `06-antibug` → `04-refactor` |
| **05** | `/tdd` | Focused TDD cycle for a single feature. | `05-tdd-guide` → `04-refactor` → `06-antibug` |
| **06** | `/fix-bugs` | Full bug hunting and patching. | `01-scanner` → `06-antibug` → `05-tdd-guide` |
| **07** | `/write-report` | Academic or technical report pipeline. | `03-planner` → `08-scientific-writing` → `09-latex-bib-manager` |
| **08** | `/cross-agent-validator` | Self-audit: verify all agents did their job. | — |
| **09** | `/release-project` | Final release: cleanup → market eval → license → README. | `11-market-evaluator` → `12-commercial-license` → `10-readme-architect` |
| **10** | `/auto-commit` | Generate atomic git commit commands for all uncommitted changes. | `13-git-commit-author` |

---

## Architecture

```
.agent/
├── rules/              ← Always-active behavioral instincts (fire every session)
│   ├── 00-workflow-orchestration.md  Prefix-based UI ordering
│   ├── 01-context-memory.md          Project-directory-aware persistence
│   ├── 02-metadata-awareness.md      Root PROJECT_METADATA.md focus
│   ├── 03-asset-awareness.md         src/ vs root asset placement
│   ├── 04-dump-awareness.md          Graveyard management (.agent/ protected)
│   ├── 05-semantic-versioning.md     Single-source version bumping
│   ├── 06-silent-ingest.md           Bulk text absorption mode
│   ├── 07-core.md                    Execution logic & isolation
│   ├── 08-self-improvement.md        Upgrade instincts
│   └── 09-release-packaging.md       Automated ZIP generation
│   └── 10-git-awareness.md           Conventional Commits enforcement
├── skills/             ← Foundational (subconscious) logic — not in UI
│   ├── 01-research-loop.md           DeepDive evidence scan
│   ├── 02-architectural-design.md    Hexagonal architecture & SOLID
│   ├── 03-code-synthesis.md          Weighted consensus merging
│   ├── 04-refactor.md                Red-Green-Refactor Phase 3
│   └── 05-commit-semantics.md        Atomic diff chunking logic
├── .agents/skills/     ← UI Agent-Skills (slash commands + buttons)
│   ├── 01-deep-scan/
│   ├── 02-ask/
│   ├── 03-planner/
│   ├── 04-synthesizer/
│   ├── 05-tdd-guide/
│   ├── 06-antibug/
│   ├── 07-web-aesthetics/
│   ├── 08-scientific-writing/
│   ├── 09-latex-bib-manager/
│   ├── 10-readme-architect/
│   ├── 11-market-evaluator/
│   ├── 12-commercial-license/
│   └── 13-git-commit-author/
├── workflows/          ← Multi-agent pipelines (+ button, ordered 01–10)
│   ├── 01-scanner.md
│   ├── 02-scaffold-assets.md
│   ├── 03-multi-plan-synthesis.md
│   ├── 04a-build-website.md
│   ├── 04b-build-app.md
│   ├── 05-tdd.md
│   ├── 06-fix-bugs.md
│   ├── 07-write-report.md
│   ├── 08-cross-agent-validator.md
│   ├── 09-release-project.md
│   └── 10-auto-commit.md
├── AGENTS.md           ← This file
├── session-context.md  ← Project-specific memory
└── antigravity-agent-install-state.json
```

# Antigravity Agent Architecture

This repository provides specialized agents, modular skills, and UI-integrated workflows.

## 🚀 How to Use

### 1. Using a Single Agent (Slash Commands)
You can call any agent directly in the chat by typing its folder name with a forward slash.
Example: Type `/planner` and then describe your feature.

| Slash Command | Agent Persona | Purpose |
| :--- | :--- | :--- |
| **`/planner`** | Planner | Strategic breakdown & phased roadmap. |
| **`/synthesizer`**| Synthesizer | Merging multiple AI plans from `/Plan`. |
| **`/antibug`** | Antibug | Deep logic auditing & memory leak detection. |
| **`/commercial-license`**| License | Generating commercial/contributor licenses. |
| **`/market-evaluator`**| Evaluator | Assessing codebase market value & pricing. |
| **`/scientific-writing`**| Scientific | Academic tone & dissertation drafting. |
| **`/latex-bib-manager`**| Bib Manager | Citation sequencing and LaTeX float fixing. |
| **`/web-aesthetics`**| Style Master | Enforcing premium UI & modern aesthetics. |
| **`/readme-architect`**| Architect | Building engaging, layman-friendly READMEs. |

### 2. Using Multiple Agents (Workflows)
To use multiple agents in a coordinated sequence, use the **Workflows** available in the **plus icon (`+`)** on the chat bar. Workflows are the "glue" that allows agents to work together.

| Workflow | Integrated Agents Sequence |
| :--- | :--- |
| **`/build-website`**| `planner` → `web-aesthetics` → `tdd` → `versioning` |
| **`/build-app`** | `planner` → `tdd` → `versioning` |
| **`/write-report`** | `planner` → `scientific-writing` → `latex-bib-manager` |
| **`/fix-bugs`** | `deep-scan` → `antibug` → `versioning` |
| **`/release-project`**| `dump-cleanup` → `market-evaluator` → `commercial-license` → `readme-architect` |

---

## The Dual-Skill Architecture
- **Foundational Skills (`.agent/skills/`)**: Internal "subconscious" logic (not in UI).
- **Agent-Skills (`.agent/.agents/skills/`)**: UI Personas with custom slash commands.

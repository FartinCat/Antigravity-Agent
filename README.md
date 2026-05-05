<div align="center">

![Antigravity Agent Banner](assets/banner.png)

# 🌌 Antigravity Agent Ecosystem
**The Ultimate AI Orchestration Framework for Professional Developers**

[![Version](https://img.shields.io/badge/version-2.2.0-blueviolet?style=for-the-badge)](https://github.com/FartinCat/Antigravity-Agent)
[![Buy License](https://img.shields.io/badge/GET_LICENSE-Click_Here-gold?style=for-the-badge&logo=gumroad)](https://antigravity.lemonsqueezy.com/checkout/buy/35a2a620-3f40-4aea-9e0d-1d58819ae5f1)
[![Student Access](https://img.shields.io/badge/STUDENTS-Verify_&_Get_Free-blue?style=for-the-badge)](mailto:fartincat@proton.me)

---

> "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." — **Nikola Tesla**

</div>

### 💰 Commercial Licensing
Antigravity is a **premium, paid ecosystem**. The core "Brain" (the `.agent` folder) is not included in this public repository. To unlock the full agentic power of the 12 autonomous skills and 10 workflows, you must purchase a license.

**[Click here to purchase and download the Core (.agent folder)](https://antigravity.lemonsqueezy.com/checkout/buy/35a2a620-3f40-4aea-9e0d-1d58819ae5f1)**

---

## 🧠 Introduction & Architecture
Welcome! This repository doesn't just hold code; it holds **behaviors, rules, and AI personas**. Antigravity uses a **Dual-Skill Architecture**:
- **🍽️ The "Waiters" (Agents)**: UI-facing skills that interact with you directly (`.agent/.agents/skills/`).
- **📖 The "Recipe Book" (Foundational Rules)**: Hidden markdown files that dictate AI behavior in the background (`.agent/skills/` and `.agent/rules/`).

---

## 📥 Installation & Deployment Guide
You can seamlessly integrate the Antigravity Brain into **any** existing project directory on any OS. **You only ever need to copy the `.agent/` folder.** Everything else in this repository belongs to the source project and should NOT be copied.

### Step 1: Copying the Core (`.agent/`)

**Method 1: rsync (Recommended for Linux/WSL/macOS)**
```bash
# The trailing slash on the source path is intentional.
# It copies the contents of .agent/ into the destination .agent/ folder.
rsync -av --exclude='.git' \
  "/path/to/Antigravity Agent/.agent/" \
  "/path/to/YOUR_PROJECT_NAME/.agent/"
```

**Method 2: PowerShell (Windows)**
```powershell
Copy-Item -Recurse -Force `
  "D:\path\to\Antigravity Agent\.agent" `
  "D:\path\to\YOUR_PROJECT_NAME\.agent"
```

**Method 3: Windows Explorer / File Manager**
Copy the `.agent` folder from the Antigravity Agent repo and paste it into your target project directory.

### Step 2: Booting the AI (First Steps in the New Project)
1. **Open your AI IDE** (Cursor, Windsurf, VS Code) in the new project directory.
2. **Run `/scanner`** — this is always the first step. It will detect that the `session-context.md` project name has changed, archive the old project's context, and initialize a fresh memory for your new project.
3. **Run `/scaffold-assets`** — creates the `assets/` taxonomy and a fresh `PROJECT_METADATA.md` for the new project.
4. **Proceed with your workflow.**

### 🛑 Troubleshooting Migration
*   **"All agent files appeared in my project root"**: You ran rsync with a trailing slash on the source but NO target `.agent/` sub-path. Delete the dumped files and re-run with `"my-project/.agent/"` as the destination.
*   **"I see a nested .agent/.agent/ folder"**: You ran rsync WITHOUT a trailing slash on the source. Move the contents up one level.
*   **"Terminal hangs after command"**: You used a backslash `\` at the end of a path inside quotes. Use forward slashes `/`.
*   **"session-context.md still shows old project name"**: Run `/scanner`. The `01-context-memory` rule will fix it automatically.

---

## ⚙️ Execution Modes Explained
Not all components act the same way. You must understand the two execution modes:

1. **Explicit (Manual) Triggers**: These are Agents and Workflows. You must explicitly call them using a `/slash-command` (in AI IDEs) or by providing a **Copiable Sentence** (in plain chat) to wake them up.
2. **Automatic (Instincts)**: These are Rules and Foundational Skills. The AI applies these *passively in the background*. You do not need to call them; they are hardcoded into the AI's "subconscious."

---

## 🤖 The Arsenal: Agents (Explicit Triggers)
These are your active tools. To use them in a plain chat, copy their `SKILL.md` file and paste the **Trigger Sentence** below.

### 💬 Ask
*   **Purpose**: Precise doubt resolution.
*   **Slash Command**: `/ask [query]`
*   **Plain Chat Trigger**:
    ```text
    Acting as the Ask Agent, clarify this doubt: [query]
    ```

### 🔍 Deep Scan
*   **Purpose**: Maps repo architecture.
*   **Slash Command**: `/deep-scan`
*   **Plain Chat Trigger**:
    ```text
    Run a Deep Scan on this directory structure and summarize it.
    ```

### 🗺️ Planner
*   **Purpose**: Generates phased roadmaps.
*   **Slash Command**: `/planner`
*   **Plain Chat Trigger**:
    ```text
    Acting as the Planner, build a phased roadmap for [feature].
    ```

### 🐛 Antibug
*   **Purpose**: Hunts and patches code bugs.
*   **Slash Command**: `/antibug`
*   **Plain Chat Trigger**:
    ```text
    Acting as Antibug, diagnose this error log and fix it.
    ```

### 🧬 Synthesizer
*   **Purpose**: Merges multiple AI plans.
*   **Slash Command**: `/synthesizer`
*   **Plain Chat Trigger**:
    ```text
    Synthesize these attached plans into a single bugless master plan.
    ```

### ✨ Aesthetics
*   **Purpose**: Enforces premium UI design.
*   **Slash Command**: `/web-aesthetics`
*   **Plain Chat Trigger**:
    ```text
    Apply Web Aesthetics guidelines to redesign this interface.
    ```

### 🧪 TDD Guide
*   **Purpose**: Enforces Test-Driven Dev.
*   **Slash Command**: `/tdd-guide`
*   **Plain Chat Trigger**:
    ```text
    Use TDD Guide to write tests for [feature] before implementing logic.
    ```

### 🔬 Sci-Writing
*   **Purpose**: Academic tone formatting.
*   **Slash Command**: `/scientific-writing`
*   **Plain Chat Trigger**:
    ```text
    Format this text using the Scientific Writing skill.
    ```

### 📚 LaTeX Bib
*   **Purpose**: Citation management.
*   **Slash Command**: `/latex-bib-manager`
*   **Plain Chat Trigger**:
    ```text
    Run the LaTeX Bib Manager to fix my citation sequence.
    ```

### ⚖️ Evaluator
*   **Purpose**: Market value assessment.
*   **Slash Command**: `/market-evaluator`
*   **Plain Chat Trigger**:
    ```text
    Evaluate this codebase and suggest commercial pricing.
    ```

### 📜 License
*   **Purpose**: Generates custom terms.
*   **Slash Command**: `/commercial-license`
*   **Plain Chat Trigger**:
    ```text
    Acting as the Commercial License Agent, generate a custom LICENSE.md.
    ```

### 🏗️ Architect
*   **Purpose**: Builds premium READMEs.
*   **Slash Command**: `/readme-architect`
*   **Plain Chat Trigger**:
    ```text
    Acting as Readme Architect, generate a premium README.
    ```

### 📝 Commit Author
*   **Purpose**: Generates atomic git commits.
*   **Slash Command**: `/commit-author`
*   **Plain Chat Trigger**:
    ```text
    Acting as the Git Commit Author, analyze my changes and generate commit commands.
    ```

---

## 🧬 The Instincts: Rules & Foundations (Automatic)
These run silently in the background. **Do not trigger them manually.**

| # | Instinct | Type | Background Action |
| :--- | :--- | :--- | :--- |
| 00 | `workflow-orchestration` | Rule | Enforces numeric prefix ordering on all workflows, agents, and skills. |
| 01 | `context-memory` | Rule | Ensures the AI writes to `session-context.md` to maintain long-term memory. |
| 02 | `metadata-awareness` | Rule | Automatically updates `PROJECT_METADATA.md` when features or versions change. |
| 03 | `asset-awareness` | Rule | Detects `src/` vs root and places assets in the correct directory. |
| 04 | `dump-awareness` | Rule | Moves old reference folders into a read-only `dump/` directory. `.agent/` is protected. |
| 05 | `semantic-versioning`| Rule | Manages version bumps (vX.Y.Z) based on code impact. |
| 06 | `silent-ingest` | Rule | Suppresses unnecessary conversational chatter during data ingestion. |
| 07 | `core` | Rule | Master execution logic, `.agent/` isolation, and session memory. |
| 08 | `self-improvement` | Rule | Self-Upgrading: agents encode new standards permanently after producing advanced work. |
| 09 | `release-packaging` | Rule | Generates a distributable ZIP archive after every version bump. |
| 10 | `git-awareness` | Rule | Enforces Conventional Commits and the Atomic Commit mandate. |
| 01 | `research-loop` | Foundation | Forces agents to check for contradictions before outputting code. |
| 02 | `architectural-design`| Foundation | Enforces Hexagonal Architecture (Ports & Adapters) and SOLID principles. |
| 03 | `code-synthesis` | Foundation | Weighted Perspective Analysis for merging multi-AI plans. |
| 04 | `refactor` | Foundation | Cleans and optimizes code automatically during generation. |
| 05 | `commit-semantics` | Foundation | Diff chunking algorithm for splitting changes into atomic commits. |

---

## 🛤️ The Pipelines: Workflows Deconstructed
Workflows are multi-step recipes that combine specific Agents and Instincts for complex tasks. 

### 🔍 `scanner` (Repo Orientation)
*   **Best Used For**: Getting your bearings in a new or changed repository.
*   **Composition**: `/deep-scan` + `/ask` + `metadata-awareness` (Rule).

### 🏗️ `build-app` & `build-website` (Full Stack Generation)
*   **Best Used For**: Scaffolding and building an entire project from zero.
*   **Composition**: `/planner` + `/tdd-guide` + `/antibug` + `architectural-design` (Foundation).

### 🐛 `fix-bugs` (Deep Diagnostics)
*   **Best Used For**: Fixing critical, persistent application errors.
*   **Composition**: `/deep-scan` + `/antibug` + `research-loop` (Foundation).

### 🚀 `release-project` (The Finalizer)
*   **Best Used For**: Preparing a project for public launch and monetization.
*   **Composition**: `dump-awareness` (Rule) + `/market-evaluator` + `/commercial-license` + `/readme-architect` + `semantic-versioning` (Rule).

### ⚖️ `cross-agent-validator` (Pipeline Audit)
*   **Best Used For**: Auditing multi-agent workflows to ensure agents produced substantive artifacts instead of conversational hallucinations.
*   **Composition**: Systematic checks across generated artifacts.

### 🧠 `multi-plan-synthesis` (Strategy Merge)
*   **Best Used For**: Merging multiple external AI-generated plans (ChatGPT, Claude, etc.) into one master, conflict-free blueprint.
*   **Composition**: `/deep-scan` + `/synthesizer` + `code-synthesis` (Foundation).

### 📂 `scaffold-assets` (Structure Bootstrap)
*   **Best Used For**: Standardizing project taxonomy by creating a unified `assets/` directory and initializing project metadata.
*   **Composition**: `asset-awareness` (Rule) + structural generation.

### 🧪 `tdd` (Test-Driven Cycle)
*   **Best Used For**: Ensuring high code quality by strictly enforcing the Red-Green-Refactor testing cycle.
*   **Composition**: `/tdd-guide` + `refactor` (Foundation).

### 📝 `write-report` (Academic Drafting)
*   **Best Used For**: Generating high-quality, properly formatted academic or technical reports (like LaTeX dissertations).
*   **Composition**: `/planner` + `/scientific-writing` + `/latex-bib-manager`.

### 📝 `auto-commit` (Version Control Automation)
*   **Best Used For**: Generating clean, atomic git commit commands after any work session with multiple file changes.
*   **Composition**: `/commit-author` + `commit-semantics` (Foundation) + `git-awareness` (Rule).

---

## 💾 Mastering Session Memory
Because AI models forget things when you close a chat, you must maintain the "Session Context."

1. **To Save State**: At the end of your day, use this exact trigger sentence:
    ```text
    Update the session context with our progress.
    ```
   *(The `context-memory` instinct will write a summary to `.agent/session-context.md`).*

2. **To Load State**: At the start of a new day, open `.agent/session-context.md`, copy its contents, and paste it into the chat:
    ```text
    Here is the context from our last session: [paste content]. Let's continue.
    ```

---

<div align="center">
Developed by <b>FartinCat</b> | 2026 Antigravity Ecosystem
</div>


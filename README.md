<div align="center">

![Antigravity Agent Banner](assets/banner.png)

# 🌌 Antigravity Agent Ecosystem
**The Next-Gen Agentic Framework for Autonomous Coding**

[![Version](https://img.shields.io/badge/version-1.5.1-blueviolet?style=for-the-badge)](https://github.com/FartinCat/Antigravity-Agent)
[![Language](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Language](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![Language](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://www.oracle.com/java/)
[![License](https://img.shields.io/badge/License-Commercial-gold?style=for-the-badge)](LICENSE.md)

---

> "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." — **Nikola Tesla**

</div>

## 🧠 Introduction & Architecture
Welcome! This repository doesn't just hold code; it holds **behaviors, rules, and AI personas**. Antigravity uses a **Dual-Skill Architecture**:
- **🍽️ The "Waiters" (Agents)**: UI-facing skills that interact with you directly (`.agent/.agents/skills/`).
- **📖 The "Recipe Book" (Foundational Rules)**: Hidden markdown files that dictate AI behavior in the background (`.agent/skills/` and `.agent/rules/`).

---

## 📥 Installation & Deployment Guide
You can seamlessly integrate the Antigravity Brain into **any** existing project directory on any OS.

### Step 1: Download the Core
You need to copy the `.agent` folder into your target project. 

**For PowerShell / CMD (Windows):**
```powershell
# Clone the repository to a temporary location
git clone https://github.com/FartinCat/Antigravity-Agent.git temp_antigravity

# Copy the .agent folder into your project directory
Copy-Item -Path "temp_antigravity\.agent" -Destination ".\Your_Project_Directory\.agent" -Recurse

# Clean up
Remove-Item -Path temp_antigravity -Recurse -Force
```

**For Bash / Linux / Kali Linux:**
```bash
git clone https://github.com/FartinCat/Antigravity-Agent.git /tmp/antigravity
cp -r /tmp/antigravity/.agent ./Your_Project_Directory/
rm -rf /tmp/antigravity
```

### Step 2: Booting the AI
Open your project in an AI IDE (like Cursor or Windsurf) or use a plain chat interface (ChatGPT, Claude). The AI will immediately detect the `.agent` folder and adopt the Antigravity ecosystem.

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
    Generate a commercial license prohibiting free commercial use.
    ```

### 🏗️ Architect
*   **Purpose**: Builds premium READMEs.
*   **Slash Command**: `/readme-architect`
*   **Plain Chat Trigger**:
    ```text
    Acting as Readme Architect, generate a premium README.
    ```

---

## 🧬 The Instincts: Rules & Foundations (Automatic)
These run silently in the background. **Do not trigger them manually.**

| Instinct | Type | Background Action |
| :--- | :--- | :--- |
| `metadata-awareness` | Rule | Automatically updates `PROJECT_METADATA.md` when features or versions change. |
| `self-improvement` | Rule | **Self-Upgrading Instinct**: If an agent builds something advanced (like a premium README), it automatically updates its own `SKILL.md` to encode that standard permanently. |
| `dump-awareness` | Rule | Moves old, iterative reference folders into a read-only `dump/` directory to keep the root clean. |
| `context-memory` | Rule | Ensures the AI writes to `session-context.md` to maintain long-term memory. |
| `semantic-versioning`| Rule | Manages version bumps (v1.0.0) based on code impact. |
| `silent-ingest` | Rule | Suppresses unnecessary conversational chatter during data ingestion. |
| `architectural-design`| Foundation | Enforces modular, scalable code structure across all agents. |
| `research-loop` | Foundation | Forces agents to check for contradictions before outputting code. |
| `refactor` | Foundation | Cleans and optimizes code automatically during generation. |

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


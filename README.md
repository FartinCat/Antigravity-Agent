# The Antigravity Agent Developer Manual

Welcome! If you are reading this, you are looking at a highly customized "Brain" for an AI coding assistant. This repository doesn't just hold code; it holds **behaviors, rules, and AI personas**.

This manual is written so that absolutely anyone—whether you're a student, a junior developer, or an expert—can understand exactly how to use this system, and more importantly, **how to build your own agents from scratch**.

---

## 🧠 Part 1: How the Architecture Works (Explained Simply)

We took inspiration from enterprise-grade agent frameworks (like the `.agent-reference` folder) and adopted a **Dual-Skill Architecture**.

Imagine you are running a restaurant:
1. You have the **Waiters** who interact with the customers, wear a uniform, and take orders.
2. You have the **Kitchen Recipe Book** hidden in the back that tells the chefs exactly how to cook the food, but the customers never see it.

Our folders work the exact same way:

### The "Waiters" (UI-Facing Agent-Skills)
**Location:** `.agent/.agents/skills/`
These are the Agents that you interact with directly in your chat UI. 
- They have their own dedicated folder (e.g., `.agents/skills/planner/`).
- Inside their folder, they have a "Brain" (`SKILL.md`) that tells them what to do.
- They have a "Uniform" (`agents/openai.yaml`) that gives them a name, a brand color, and registers them so they show up as a clickable button in your chat interface.

### The "Recipe Book" (Foundational Skills)
**Location:** `.agent/skills/`
These are flat, simple markdown files (e.g., `architectural-design.md`). 
- They do **not** have a YAML configuration. 
- They do **not** show up in your chat UI.
- Instead, the "Waiters" (the active agents) read these files silently in the background to learn advanced rules before they write code for you.

---

## 🚀 Part 2: The Antigravity Workstyle (Your Future Workflow)

This system was built to support a very specific, high-efficiency development cycle. Here is how you will use this `.agent` folder for every future project:

### 1. Ingestion & Scan (Deep Awareness)
Every session starts with the AI scanning your entire directory. Using the **`deep-scan`** skill, the AI gains absolute context of your existing resources before suggesting a single line of code.

### 2. The Ensemble Strategy (Multi-AI Planning)
You don't rely on just one AI. You collect perspectives from ChatGPT, Claude, DeepSeek, and others, saving them in a `/Plan` folder.
- **Action**: Run **`/multi-plan-synthesis`** from the `+` button. 
- **Result**: The **`synthesizer`** agent compares all those perspectives, resolves contradictions, and creates one "bugless" master implementation roadmap.

### 3. Organized Reference (The Graveyard)
Iterative designs (like `frontend1`, `app2`) are kept for inspiration, not production. 
- **Rule**: The **`dump-awareness`** instinct ensures these folders stay read-only.
- **Action**: When you finish a phase, the system automatically moves stray reference folders into the **`dump/`** directory to keep your workspace clean.

### 4. Scientific Rigor & Aesthetic Excellence
- **Academic**: Use **`/scientific-writing`** and **`/latex-bib-manager`** for Physics dissertations to ensure objective tone and perfect citation sequencing.
- **Web/App**: The **`web-aesthetics`** skill ensures every UI uses modern typography and vibrant colors—never generic placeholders.

### 5. Monetization for Students (Funding Your Work)
As a student developer, your code has value.
- **Action**: Run **`/release-project`**. 
- **Result**: The AI scans your work with **`market-evaluator`**, generates a custom **`commercial-license`** (where companies pay, but contributors get in for free), and builds your ultimate **`readme-architect`** manual.

---

## 🛠️ Part 3: How to Build Your Own Agent From Scratch

Do you want to create a brand new UI Agent? Follow these exact steps:

1. **Create the Folder**:
   Go to `.agent/.agents/skills/` and create a new folder (e.g., `my-custom-agent`).

2. **Create the Brain (`SKILL.md`)**:
   Inside your new folder, create a file named `SKILL.md`. Use this format:
   ```markdown
   ---
   name: my-custom-agent
   description: Briefly explain what it does.
   origin: Custom
   ---
   # My Custom Agent
   Write your specific rules and behaviors here.
   ```

3. **Create the Uniform (`agents/openai.yaml`)**:
   Inside your agent's folder, create an `agents/` folder and an `openai.yaml` file:
   ```yaml
   interface:
     display_name: "My Awesome Agent"
     short_description: "What the button says"
     brand_color: "#FF0000"
     default_prompt: "Type the command here."
   policy:
     allow_implicit_invocation: true
   ```

4. **Register It**:
   Add your agent name to the list in `.agent/antigravity-agent-install-state.json`.

---

> "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." — **Nikola Tesla**

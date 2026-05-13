---
name: research-loop
description: Skill for research-loop
---

# Research Loop Protocol

This is the core investigative protocol used by all UI agents before generating any output. It produces the "DeepDive" effect — agents that investigate before they respond, not agents that guess immediately.

## The Mandate
**Evidence before output. Always.**
No agent may skip to a final answer, plan, fix, or document without first completing this loop. An agent that outputs without evidence is a liability, not an asset.

## ⚠️ Critical Exclusion Rule — READ FIRST
**When scanning for evidence, NEVER read, open, reference, or include content from the `.agent/` directory or any of its sub-folders.**
The `.agent/` folder is agent infrastructure. Reading it as "project evidence" is a fundamental category error — it would be like a doctor diagnosing a patient by reading the doctor's own medical textbooks instead of the patient's chart.

**The only project evidence sources are:**
- `Plan/` folder — external AI plans and prior decisions
- `archived/` folder — discarded previous iterations
- Root **`AETHER.md`** — **§14 Project Metadata** (version, checklist) and **§18 Session Context** (prior sessions). Treat as project memory, not `.agent/` infrastructure.
- `MASTER_PLAN.md` at root (if present)
- Actual project source files (`.py`, `.js`, `.ts`, `.html`, `.css`, `.tex`, `.rs`, etc.)
- Dependency files (`package.json`, `requirements.txt`, `Cargo.toml`, `.bib`)

**Do not read anything under `.agent/`** as project evidence (rules, skills, workflows, agents). Those are tooling — not the product under analysis.

---

## The 5-Step Research Loop

### Step 1 — Evidence Scan
Read every relevant **project** file that exists before forming any opinion:
- `Plan/` folder: What has been decided before? What AI perspectives already exist?
- `archived/` folder: What was tried and discarded? Why did previous iterations fail?
- Root **`AETHER.md` §14**: What version are we at? What features are complete vs pending?
- `MASTER_PLAN.md` (if it exists): Is there an active synthesis in progress?
- **`AETHER.md` §18**: What happened in previous sessions? (Read silently when relevant.)
- Any existing **project** source files relevant to the task at hand.
- **Do NOT scan `.agent/rules/`, `.agent/workflows/`, `.agent/.agents/`, or `.agent/skills/`** — these are agent tools, not project evidence.

### Step 2 — Contradiction Audit
Cross-reference what the plans say against what the files actually contain:
- Does the plan reference a file that doesn't exist?
- Does the plan assume a library that isn't in the dependency file?
- Does the current code contradict a decision recorded in `Plan/`?
- Log every contradiction found, even minor ones.

### Step 3 — Gap Analysis
Explicitly list what information is **missing** that would improve the output:
- Is the tech stack confirmed or assumed?
- Are there design decisions that haven't been made yet?
- Are there external dependencies (APIs, assets, secrets) not yet available?
Be honest about gaps. A plan that acknowledges gaps is more useful than one that silently papers over them.

### Step 4 — Confidence Score
Before generating any output, state one of:
- **HIGH**: All required context was found. No major contradictions. Output is well-grounded.
- **MEDIUM**: Most context found. Minor gaps or one unresolved contradiction. Proceeding with stated assumptions.
- **LOW**: Key information is missing. Significant assumptions required. Flag clearly and request user input before proceeding, or proceed with heavily caveated output.

### Step 5 — Proceed
Only after completing Steps 1–4 may the agent generate its primary output. The Research Loop summary (evidence found, contradictions, gaps, confidence score) must precede the main output in the response, formatted as a collapsible block or brief preamble.

## Research Loop Output Template
```
RESEARCH LOOP COMPLETE
======================
Project Directory: [current project folder name]
Evidence Scanned: [project files read — e.g., "Plan/planbyclaude.txt, archived/frontend1/index.html"]
.agent/ Contents: [EXCLUDED — agent infrastructure, not project evidence]
Contradictions Found: [N — list them, or "None"]
Gaps Identified: [list, or "None"]
Confidence: [HIGH / MEDIUM / LOW]
Assumptions Made: [list any, or "None"]
======================
[Agent's primary output begins here]
```

## Agents That Use This Protocol
All UI agents reference this file. It is especially critical for:
- `planner` — before generating any roadmap
- `synthesizer` — before merging any plans
- `antibug` — before issuing any diagnostic
- `market-evaluator` — before issuing any valuation
- `readme-architect` — before generating documentation

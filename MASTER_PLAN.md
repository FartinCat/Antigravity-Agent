# Master Implementation Plan — Antigravity Agent v3.0.0
Generated: 2026-05-05
Plans Synthesized: suggestionbyclaude.txt, suggestionbygemini.txt, suggestionbyperplexity.txt, suggestionbychatgpt.txt, suggestionbydeepseek.txt
Conflicts Resolved: 14

---

## Executive Summary

This plan upgrades the Antigravity Agent from v2.2.0 → v3.0.0 by implementing the **highest-impact, consensus-driven** improvements from 5 independent AI strategy documents. The upgrade focuses on three pillars:

1. **Cognitive Architecture Upgrade** — New rules, skills, and an instincts layer
2. **Language-Specific Agent Modules** — Deep expertise per language
3. **Self-Evolution & Low-Tier LLM Compensation** — Memory tiers and confidence scoring

> **Design Constraint**: All new files integrate into the existing `.agent/` folder structure. No breaking changes to the existing 13 agents, 11 rules, 5 skills, or 10 workflows. All additions are additive.

---

## Phase 1: Foundational Upgrades (Rules + Skills)

### Step 1.1: New Universal Rules

Add 4 new rules to `.agent/rules/`:

| File | ID | Purpose | Source Consensus |
|---|---|---|---|
| `11-integrity.md` | R1 | Hard-stop rules: never edit build artifacts, never commit secrets, never skip verification, never assume state, never fix symptoms | Claude 5/5, all agree |
| `12-instincts.md` | INSTINCT | Probabilistic warnings: missing inverse operations, deep nesting, large functions, resource leaks, hardcoded config | Claude 5/5, DeepSeek, ChatGPT |
| `13-verification-gates.md` | VERIFY | Every action has a verification gate (syntax→static→unit→integration→behavioral) | Claude 4/5, Perplexity |
| `14-context-integrity.md` | R4 | No stale file summaries after writes, no reuse of call graphs after edits, skill version checking | Perplexity unique, strong |

### Step 1.2: New Foundational Skills

Add 4 new skills to `.agent/skills/`:

| File | Purpose | Source |
|---|---|---|
| `06-task-decomposition.md` | Rules for breaking tasks to ≤1 file, ≤1 function, ≤1 concept per LLM call | Claude, DeepSeek, ChatGPT all agree |
| `07-confidence-scoring.md` | Formula: base 70, modifiers for complexity/security/async/LOC | Claude, DeepSeek |
| `08-memory-evolution.md` | Session→Project→Global memory promotion protocol with confidence decay | Claude, Perplexity |
| `09-language-routing.md` | Detect language from extensions/shebangs/build files, route to correct agent | Claude, Gemini, Perplexity |

### Step 1.3: New Agent — Failure Prediction

Add agent `14-failure-predictor/` to `.agent/.agents/skills/`:

| Trigger | Purpose |
|---|---|
| Before any code execution | Predicts likely bugs, rule violations, fragile areas based on memory + instincts |

Risk: LOW
Dependencies: None

---

## Phase 2: Language-Specific Agent Modules

### Step 2.1: Python Language Agent

New agent `15-python-agent/` with SKILL.md encoding:
- **Rules**: PY-R001 through PY-R008 (type hints, no mutable defaults, explicit exceptions, context managers, no star imports, async boundaries, frozen dataclasses)
- **Instincts**: PY-INSTINCT-001 through PY-INSTINCT-007 (shared mutable state, generator exhaustion, pandas chained indexing, asyncio blocking, pickle security, dict key mutation, subprocess injection)
- **Workflow insert**: mypy → flake8/ruff → bandit → pytest → circular import check

### Step 2.2: Rust Language Agent

New agent `16-rust-agent/`:
- **Rules**: RS-R001 through RS-R008 (unsafe proof, no unwrap, lifetimes before clones, error hierarchy, Send/Sync docs, pinned futures, no await in sync mutex)
- **Instincts**: RS-INSTINCT-001 through RS-INSTINCT-006 (lock poisoning, iterator collect, Arc/Mutex smell, lifetime missing, memory layout, RefCell borrow panic)
- **Ownership Preflight Protocol**: For every function, decide own/borrow/mut-borrow before writing

### Step 2.3: JavaScript/TypeScript Language Agent

New agent `17-jsts-agent/`:
- **Rules**: JSTS-R001 through JSTS-R007 (strict mode, floating promises, ESM/CJS consistency, env split, dep audit, no default exports, Promise.allSettled)
- **Instincts**: JSTS-INSTINCT-001 through JSTS-INSTINCT-006 (async forEach, closure in loop, prototype pollution, React stale closure, V8 deoptimization)

### Step 2.4: C Language Agent

New agent `18-c-agent/`:
- **Rules**: C-R001 through C-R008 (all warnings as errors, malloc/free pairing, return value checked, buffer bounds, signed/unsigned, bounded string functions, strict aliasing, struct zeroing)
- **Instincts**: C-INSTINCT-001 through C-INSTINCT-006 (use-after-free, off-by-one, format string, struct padding, signal handler, macro side effects)

### Step 2.5: Go Language Agent

New agent `19-go-agent/`:
- **Rules**: GO-R001 through GO-R006 (errors handled, goroutine lifecycle, context first param, interfaces at use site, error wrapping, no global HTTP client)
- **Instincts**: GO-INSTINCT-001 through GO-INSTINCT-005 (loop variable capture)

Risk: LOW — All agents are additive SKILL.md files
Dependencies: Phase 1 (language routing skill)

---

## Phase 3: Micro-Inspector Swarm

### Step 3.1: Side-Effect Tracker

New skill `10-side-effect-tracker.md`:
- Detects global state mutation inside pure-named functions (get_, is_, calc_, format_)
- Source: Gemini (unique contribution, high value)

### Step 3.2: State Machine Inspector

New skill `11-state-machine-inspector.md`:
- Detects classes with multiple boolean flags that should be a unified enum
- Source: Gemini, Claude

### Step 3.3: Cognitive Load Inspector

New skill `12-cognitive-load-inspector.md`:
- Measures nesting depth + variable mutation in loops + declaration-usage distance
- Blocks functions with Cognitive Complexity > 15
- Source: Gemini, DeepSeek

Risk: LOW
Dependencies: None

---

## Phase 4: Advanced Workflows

### Step 4.1: Onboard-Analyze-Stabilize Workflow

New workflow `11-onboard-project.md`:
- First contact with any new repository
- Detect languages → infer project type → map architecture → run all inspectors read-only → write project memory
- Source: Perplexity, Claude (Appendix B)

### Step 4.2: Performance Optimization Workflow

New workflow `12-performance.md`:
- Measure → Algorithmic replacement → Mechanical sympathy → Verify >15% improvement or discard
- Source: Gemini

Risk: LOW
Dependencies: Phase 2 (language agents for mechanical sympathy)

---

## Phase 5: Self-Evolution Engine

### Step 5.1: Skill Distillation Protocol

Upgrade `08-self-improvement.md` to include:
- Every 50 sessions: identify skill pairs frequently applied together → draft Macro-Skill
- Skill decay: unused 30+ sessions → watch list
- Confidence scoring: +0.03 per success, -0.08 per false positive
- Source: Gemini, DeepSeek, Perplexity all converge

### Step 5.2: Automated Prompt Evolution

Add to `06-task-decomposition.md`:
- If a task type fails >20%: flag the prompt template, inject new constraint
- Source: Gemini

### Step 5.3: Human Feedback Loop

Add to `08-memory-evolution.md`:
- When human overrides agent action: capture diff, generalize pattern, create candidate skill at confidence 0.85
- Source: DeepSeek

Risk: MEDIUM (requires careful confidence calibration)
Dependencies: Phase 1 (confidence scoring)

---

## Conflict Log

| # | Conflict | Plan A | Plan B | Resolution |
|---|---|---|---|---|
| 1 | AST-based context vs full-file reading | Gemini (AST only) | Claude (full file + summary) | **Claude wins**: AST engines require tree-sitter integration not available in pure markdown agents. Use summary caching instead. |
| 2 | Agent tier count | Perplexity (5 tiers) | Claude (4 levels) | **Claude wins**: 4 levels matches existing architecture. Perplexity's Tier 4 (Repair) absorbed into existing `06-antibug`. |
| 3 | Skill store file format | Claude (YAML schemas) | Current system (Markdown) | **Current system wins**: Markdown is the native format. YAML skill schemas are aspirational for v4.0. |
| 4 | Number of language agents | Claude (9 languages) | DeepSeek (8 languages) | **Consensus**: Start with 5 (Python, Rust, JS/TS, C, Go). Add C++, C#, R, Java/Kotlin in v3.1. |
| 5 | Memory engine implementation | Claude (separate files per tier) | Current (single session-context.md) | **Hybrid**: Keep session-context.md for session tier. Add project_memory/ folder for project tier. Global memory deferred to v3.1. |
| 6 | Inter-agent communication protocol | Claude (JSON messages) | Current (workflow chaining) | **Current wins**: JSON message protocol requires runtime not available in markdown agents. Workflow chaining is sufficient. |
| 7 | Micro-inspector output format | DeepSeek (JSON dashboard) | Claude (JSON reports) | **Consensus**: Both agree on JSON. Implement as structured markdown with JSON code blocks for now. |
| 8 | Rollout timeline | DeepSeek (12 weeks) | Claude (20 weeks) | **Pragmatic**: Implement Phase 1-3 immediately. Phase 4-5 in follow-up sessions. |
| 9 | Cognitive Load Index | DeepSeek (RU 1-4) | ChatGPT (Task Atomization) | **Merge**: Both describe the same concept. Use DeepSeek's RU scale inside ChatGPT's atomization engine. |
| 10 | Self-play verification | DeepSeek (Devil's Advocate) | Claude (self-adversarial pass) | **Identical concept**: Implement as "adversarial verification" skill. |
| 11 | Macro-skills | Gemini (Synthesis Protocol) | Perplexity (Skill Distillation) | **Identical concept**: Implement as "skill distillation" in evolution rules. |
| 12 | Perception layer | ChatGPT (new meta-layer) | Claude (Context Load phase) | **Claude wins**: Already exists as Phase 1 of Feature Implementation workflow. Rename to "Perception Phase" for clarity. |
| 13 | Strategy selection | ChatGPT (5 strategy types) | Claude (workflow selection) | **Claude wins**: Existing workflow engine already selects strategy. ChatGPT's types map to existing workflows. |
| 14 | Reflection layer | ChatGPT (post-execution) | Claude (Memory Update phase) | **Identical**: Already exists as Phase 6 in Claude's workflows. No new component needed. |

---

## Verification Plan

### Automated Tests
- After each phase: verify all existing agents still function by running `/scanner` and `/cross-agent-validator`
- Verify new files are syntactically valid markdown with correct frontmatter

### Manual Verification
- Run `/scanner` after all changes to confirm no structural anomalies
- Bump version to v3.0.0 in PROJECT_METADATA.md and session-context.md
- Generate auto-commit with `/auto-commit`

---

## Version Impact
- **Before**: v2.2.0 — 13 agents, 11 rules, 5 skills, 10 workflows
- **After**: v3.0.0 — 19 agents, 15 rules, 12 skills, 12 workflows

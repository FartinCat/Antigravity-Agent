# Antigravity Agent — v4.0.0 Master Implementation Plan
**Author:** Deep analysis of 15 reference repositories  
**Current State:** v2.2.0 (install-state) / v3.0.0 (AGENTS.md)  
**Target:** v4.0.0 — A production-grade Agentic OS  
**Execution Mode:** Paste each Phase Prompt into Claude Code / Cursor / Antigravity, in strict order.

---

## What Was Found Across All 15 Reference Repos

| Repo | Key Contribution |
|---|---|
| `agent-skills-addyosmani` | **The gold standard.** SKILL.md format, 3 specialist personas, `/ship` parallel fan-out, Intent→Skill mapping, skill anatomy, SDD lifecycle |
| `cc-sdd` | **Kiro-style 3-phase approval.** Spec→Requirements→Design→Tasks→Impl. Steering files. Spec-per-feature. `kiro-review`, `kiro-debug`, `kiro-verify-completion` subagent skills |
| `context-mode` | **"Think in Code" mandate.** `ctx_execute`, `ctx_execute_file`, `ctx_batch_execute`. Bash whitelist. Context window preservation as a first-class concern |
| `antigravity-workspace-template` | **Knowledge Engine.** `/ag-refresh` + `/ag-ask` CLI commands. Local RAG for the repo. "Explicit is better than implicit" AGENTS.md philosophy |
| `peon-ping` | **Audio notification MCP.** `peon-mcp.js` — `play_sound` tool, catalog resource, CESP event system. Windows/WSL2/Linux/macOS support |
| `ai-devkit` | **Memory + Lifecycle.** `memory search/store/update` CLI, `capture-knowledge`, `execute-plan`, `new-requirement`, `debug` workflows. `docs/ai/` knowledge hierarchy |
| `antigravity-awesome-skills` | **Massive catalog.** 1000+ skills across all domains. Key extracts: `agent-orchestration`, `multi-agent-patterns`, `context-management`, `spec-to-code-compliance`, `tdd-workflow`, `antigravity-workflows` |
| `agent-skills-techleads` | **Enterprise skill taxonomy.** Organized by: architecture, cloud, creation, decision-making, design, development, monitoring, performance, quality, security, tooling |
| `cc-skills-golang` | **41 Go deep-dives.** concurrency, error-handling, testing, observability, design-patterns, security, naming, project-layout — complete language mastery |
| `stitch-skills` | **Premium UI skills.** `stitch-design`, `stitch-loop`, `design-md`, `react-components`, `shadcn-ui`, `taste-design` — visual quality-first approach |
| `autogen` | **Multi-agent orchestration patterns.** GroupChat, nested chats, function calling between agents |
| `langgraph` | **Stateful agent workflows.** Graph-based state machines, checkpoint persistence, subgraph patterns |
| `system-prompts-and-models` | **Commercial AI instinct patterns.** Cursor/Devin/Copilot behavioral patterns — minimal footprint, verification-before-confidence |
| `awesome-ai-apps` | **Application patterns.** Real-world agentic app architectures |
| `cc-sdd` (`.kiro/specs/`) | **Real spec examples.** 4 complete specs: RAG backend, photo albums, research agent — ground truth for spec format |

---

## Gap Analysis: v3.0.0 → v4.0.0

| Component | v3.0.0 | Gap | v4.0.0 Target |
|---|---|---|---|
| Entry point | ❌ No CLAUDE.md | Critical | ✅ CLAUDE.md master bootstrap |
| Slash commands | ❌ No .claude/commands/ | Critical | ✅ 20+ real slash commands |
| Spec lifecycle | ❌ No SDD pipeline | Critical | ✅ /spec → /plan → /impl → /ship |
| Specialist personas | ❌ Agents described, not real | Critical | ✅ 3 production personas |
| /ship fan-out | ❌ Missing | High | ✅ Parallel code+security+test review |
| Context management | ❌ No "Think in Code" rule | High | ✅ context-mode integration |
| Instincts layer | ❌ Embedded in rules | High | ✅ .agent/instincts/ directory |
| Knowledge engine | ❌ None | High | ✅ /ag-refresh + /ag-ask |
| MCP config | ❌ None | High | ✅ .mcp.json + 6 servers |
| Audio notifications | ❌ None | Medium | ✅ peon-ping MCP |
| Memory CLI | ❌ None | Medium | ✅ ai-devkit memory integration |
| Go skill depth | Basic agent | Medium | ✅ 10 extracted Go patterns |
| UI/Design skills | Basic | Medium | ✅ stitch-design integration |
| Rules | 15 files | Low | ✅ 5 new rules (15–19) |
| Skills | 12 files | Low | ✅ 7 new skills (13–19) |
| Workflows | 12 files | Low | ✅ 8 new workflows (13–20) |

---

## The 12-Phase Execution Plan

---

### PHASE 1 — CLAUDE.md: The Master Bootstrap

**What:** Create the `CLAUDE.md` file at the repo root. This is what Claude Code reads automatically on every session start. It is the single most important file — everything else is useless without it.

**Sources:** `agent-skills-addyosmani/CLAUDE.md`, `cc-sdd/CLAUDE.md`, `context-mode/CLAUDE.md`, `antigravity-workspace-template/CLAUDE.md`

**Key patterns to steal:**
- `agent-skills-addyosmani`: Project structure block, conventions block, "never add vague advice" boundary
- `cc-sdd`: Steering vs Specification separation concept, minimal workflow display  
- `context-mode`: **"Think in Code — MANDATORY"** block (this is the single most valuable import)
- `antigravity-workspace-template`: "Before acting: 1. Read AGENTS.md. 2. For spec work, follow openspec/AGENTS.md."

**Deliverables:** `CLAUDE.md` (~200 lines)

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create CLAUDE.md at the repo root of the Antigravity Agent project.
This is the master bootstrap file Claude Code reads automatically on every session start.

READ FIRST (mandatory before writing):
- .agent/AGENTS.md (current agent registry)
- .agent/rules/01-core.md (core directives)
- .agent/rules/00-workflow-orchestration.md (numbering system)
- .agent/session-context.md (current project state)

CLAUDE.md must contain these sections IN THIS ORDER:

## 1. IDENTITY BLOCK
- "Antigravity Agent v4.0.0 — Portable AI Operating System"
- Core personality: deterministic, zero-trust, quality-obsessed
- One sentence: what this repo is and what the agent's job is

## 2. BOOT SEQUENCE (ordered, mandatory, runs every session)
The agent MUST read files in this exact order:
a) .agent/rules/01-core.md
b) .agent/rules/03-instincts.md  
c) .agent/rules/00-workflow-orchestration.md
d) .agent/session-context.md
e) All remaining .agent/rules/ files
f) All .agent/skills/ files
g) .agent/AGENTS.md
Rule: Agent Infrastructure Isolation — .agent/ is NEVER treated as project source code.

## 3. THINK IN CODE — MANDATORY (import verbatim from context-mode concept)
For any operation that reads, analyzes, filters, counts, searches, parses, or transforms data:
WRITE A SCRIPT instead of reading raw content into context.
Bash whitelist (safe to run directly): mkdir, mv, cp, rm, touch, chmod, git add/commit/push/checkout/branch, cd, pwd, echo, npm install
Everything else: use a script/code block. One script replaces ten tool calls.
Rule: DO NOT cat large files. DO NOT read log files raw. DO NOT grep output >20 lines into context.

## 4. SLASH COMMAND REGISTRY
Two-column table: command name + one-line description for ALL commands:
Single agents (from AGENTS.md): /scanner /failure-predictor /ask /planner /synthesizer /tdd-guide /python /rust /jsts /c-lang /go /antibug /web-aesthetics /readme-architect /market-evaluator /commit-author
Workflows (+ button): /scanner /onboard-project /scaffold-assets /multi-plan-synthesis /build-website /build-app /tdd /fix-bugs /performance /write-report /cross-agent-validator /release-project /auto-commit
NEW lifecycle commands (Phase 3): /spec /plan /impl /review /ship

## 5. MEMORY PROTOCOL
- Always read session-context.md at session start
- Always write a summary to session-context.md at session end  
- The Project Directory field MUST match current project before trusting stored history
- Cross-session notes stored via memory MCP (if available) or personal-notes.md

## 6. ZERO-TRUST MANDATE (from rule 01-core.md)
- Never mark DONE without proof (test output, build success, or user walkthrough)
- Never hallucinate file paths or API calls — verify existence before writing the call
- Never delete files without explicit user confirmation
- Never advance to implementation without a validated plan

## 7. WORKFLOW AUTO-DETECTION
- User says "new feature" or "build X" → run /spec first
- User says "fix this bug" → run /antibug
- User says "commit" → run /auto-commit
- User says "release" → run /release-project
- User says "review my code" or "ship this" → run /ship (parallel fan-out)
- User says "research X" → use fetch MCP + synthesize

## 8. AGENT COMPOSITION RULES (from addyosmani AGENTS.md)
- Skills (.agent/skills/) = HOW. Mandatory workflows when intent matches.
- Personas (.agent/.agents/skills/) = WHO. Roles with output format.
- Commands (.claude/commands/) = WHEN. Orchestration layer.
- The user (or a slash command) is the orchestrator. Personas do not invoke other personas.
- One endorsed multi-persona pattern: parallel fan-out with merge (used by /ship).

## 9. QUALITY GATES (non-negotiable)
- Code must have tests before marking done
- UI must meet accessibility standards (WCAG AA)
- Commits must follow Conventional Commits spec
- Releases must have CHANGELOG entries
- Any function >60 lines must be justified

## 10. SELF-IMPROVEMENT LOOP
At session end, evaluate and write to session-context.md:
- What worked well → reinforce
- What failed → log as lesson
- New patterns discovered → propose addition to .agent/skills/

OUTPUT: CLAUDE.md in repo root. Minimum 200 lines. This is the most important file.
```

**Verification:**
```bash
wc -l CLAUDE.md                    # must be 200+
grep "Think in Code" CLAUDE.md     # must exist
grep "Boot Sequence" CLAUDE.md     # must exist  
grep "Zero-Trust" CLAUDE.md        # must exist
grep "Fan-Out" CLAUDE.md           # must exist (Phase 8)
```

---

### PHASE 2 — Context Engine: "Think in Code" Rule

**What:** Add a new rule file `.agent/rules/15-context-engine.md` that encodes the context-mode philosophy as a hard governance rule. Also update `session-context.md` to log context health.

**Source:** `context-mode/CLAUDE.md`, `context-mode/skills/context-mode/SKILL.md`

**Why this is critical:** Without this rule, the agent will blindly `cat` large files, dump grep output, and read logs raw — all of which collapse the context window on large projects, degrade response quality, and waste tokens.

**Deliverables:** `.agent/rules/15-context-engine.md`, amended `.agent/session-context.md`

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create .agent/rules/15-context-engine.md — the "Think in Code" governance rule.

This rule encodes context window management as a hard governance constraint.

The file must cover:

## The Law (one sentence)
"For any operation reading, analyzing, filtering, counting, searching, parsing, or transforming data: write and execute a script — never read raw content into context."

## Why This Exists
Without this rule: the agent reads 2000-line log files into context, cats entire source trees, pipes grep output raw. This collapses the context window, degrades response quality across the session, and wastes tokens on every subsequent response.

## Bash Whitelist (ALWAYS safe to run directly)
File mutations: mkdir, mv, cp, rm, touch, chmod
Git writes: git add, git commit, git push, git checkout, git branch, git merge
Navigation: cd, pwd, which, echo, printf
Package install: npm install, pip install

## Context Mode (everything not on whitelist)
Reading/analyzing files → use script with fs.readFileSync or open()
Running tests → execute and capture output, print SUMMARY not full output
Git log/diff/status → execute and filter, print findings not raw output
API calls → execute with fetch/requests, parse response, print findings
Finding TODOs/patterns → execute grep with counted output

## Code Patterns (language selection)
- HTTP/API/JSON: JavaScript (native fetch, JSON.parse, async/await)
- Data/CSV/stats: Python (csv, statistics, collections)
- File patterns/pipes: Shell (grep, awk, jq, wc, sort, uniq)

## Hard Prohibitions
- NEVER cat a file >50 lines for analysis (use script instead)
- NEVER pipe command output >20 lines raw into context
- NEVER read a log file directly — execute and summarize
- NEVER dump raw API responses — parse and print findings
- NEVER read source files for analysis — write analysis code

## Script Output Rule
All analysis scripts must:
1. console.log/print FINDINGS, not raw data
2. Include line numbers, IDs, exact values when reporting bugs
3. Never return "wasted call" — if output is empty, say so explicitly

## When to Use Full Reads
The Read tool is CORRECT for: files you intend to EDIT (not analyze), spec files, rule files, workflow files, session-context.md.
Read = editing context. Script = analysis context. Different purposes.

FORMAT: Use the standard rule frontmatter:
---
rule: 15-context-engine
priority: CRITICAL
---

Write the complete file now.
```

---

### PHASE 3 — The SDD Lifecycle: /spec /plan /impl /ship Commands

**What:** Create `.claude/commands/` directory with the core Spec-Driven Development slash commands. This is the "lifecycle" layer — the missing orchestration layer that makes the agent behave like a product team, not a code monkey.

**Sources:** `agent-skills-addyosmani/.claude/commands/` (spec.md, plan.md, build.md, ship.md), `cc-sdd/CLAUDE.md` (kiro workflow), `cc-sdd/.agents/skills/cc-sdd-new-agent/SKILL.md`

**Key patterns:**
- `spec.md` (addyosmani): 6-area spec document (Objective, Commands, Structure, Code Style, Testing, Boundaries), surfaces assumptions BEFORE writing any code
- `plan.md` (addyosmani): read-only plan mode, vertical slicing, acceptance criteria per task, checkpoints
- `build.md` (addyosmani): RED→GREEN→REFACTOR cycle, pick next task from plan
- `ship.md` (addyosmani): **the parallel fan-out pattern** — 3 subagents concurrently, then merge

**Deliverables:** `.claude/commands/` with 12 command files + README.md

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create the .claude/commands/ directory with all slash command files.
Claude Code reads .claude/commands/*.md files and makes them available as /command-name slash commands.

STEP 1: Create directory
mkdir -p .claude/commands/

STEP 2: Create these files. Each file must have YAML frontmatter with `description` field.

FILE: .claude/commands/spec.md
---
description: Start spec-driven development — write a structured specification before writing any code
---
Content: Invoke the Antigravity spec-driven-development workflow.
Surface assumptions IMMEDIATELY before writing spec content:
"ASSUMPTIONS I'M MAKING: [list] → Correct me now or I'll proceed with these."
Then write a spec document covering six core areas:
1. Objective — what, why, who, success criteria
2. Commands — full executable commands with flags (build, test, lint, dev)
3. Project Structure — directory layout with descriptions
4. Code Style — one real code snippet showing style beats paragraphs describing it
5. Testing Strategy — framework, test locations, coverage expectations
6. Boundaries — Always do / Ask first / Never do
Save as SPEC.md in project root. Confirm with user before proceeding to /plan.

FILE: .claude/commands/plan.md
---
description: Break work into small verifiable tasks with acceptance criteria and dependency ordering
---
Content: Invoke the Antigravity planning-and-task-breakdown workflow.
ENTER PLAN MODE — read only, no code changes.
Process:
1. Read SPEC.md (or existing spec/requirements)
2. Map the dependency graph (what must be built before what)
3. Slice VERTICALLY — one complete path per task, not horizontal layers
4. Write each task with: description, acceptance criteria (3 max), verification step, files likely touched, estimated scope (S/M/L)
5. Add checkpoints between phases (build must pass, tests must pass)
6. Present plan for human review before any implementation begins
Task sizing: S=1-2 files, M=3-5 files, L=5+ files (L = break it down further)
Save plan to tasks/plan.md and task list to tasks/todo.md.

FILE: .claude/commands/impl.md
---
description: Implement the next task incrementally — build, test, verify, commit
---
Content: Invoke the Antigravity incremental-implementation + tdd-guide workflow.
Pick the NEXT PENDING task from tasks/todo.md.
For each task:
1. Read the task's acceptance criteria
2. Load relevant context (existing code, patterns, types) — use scripts, not raw reads
3. Write a FAILING test for the expected behavior (RED)
4. Implement minimum code to pass the test (GREEN)
5. Run full test suite to check for regressions
6. Run build to verify compilation
7. Commit with descriptive message (Conventional Commits format)
8. Mark task complete in tasks/todo.md and move to next
If any step fails: invoke /antibug.

FILE: .claude/commands/review.md
---
description: Run a five-axis code review on current changes
---
Content: Invoke the code-reviewer persona from .agent/.agents/skills/12-antibug/.
Review axes:
1. Correctness — does it do what the spec says? edge cases handled?
2. Readability — can another engineer understand it without explanation?
3. Architecture — follows existing patterns? module boundaries maintained?
4. Security — inputs validated? secrets out of code? queries parameterized?
5. Performance — N+1 queries? unbounded loops? missing pagination?
Output format: APPROVE | REQUEST CHANGES + Critical/Important/Suggestion findings.
Every Critical and Important finding must include a specific fix recommendation.

FILE: .claude/commands/ship.md
---
description: Run parallel fan-out to code-reviewer, security-auditor, and test-engineer, then synthesize a go/no-go decision
---
Content: /ship is a fan-out orchestrator. Spawn three subagents CONCURRENTLY.
PHASE A — Parallel fan-out (all three in one turn):
1. code-reviewer: five-axis review (correctness, readability, architecture, security, performance)
2. security-auditor: OWASP Top 10, secrets handling, auth/authz, dependency CVEs
3. test-engineer: coverage gaps for happy path, edge cases, error paths, concurrency
PHASE B — Merge in main context:
- Aggregate Critical/Important findings, resolve duplicates
- Promote Critical security findings to launch blockers
- Check accessibility (keyboard nav, contrast), infrastructure (env vars, migrations)
PHASE C — Decision and rollback plan:
Output: "Ship Decision: GO | NO-GO" with Blockers, Recommended fixes, Rollback plan.
Rule: If ANY persona returns Critical finding → default NO-GO unless user accepts risk.
Skip fan-out ONLY if: ≤2 files changed AND diff <50 lines AND does NOT touch auth/payments/data/config.

FILE: .claude/commands/scanner.md
---
description: Map the entire repository before any work begins — project-aware deep scan
---
Content: Invoke .agent/.agents/skills/01-deep-scan.
Actions: List all directories and files. Identify tech stack (languages, frameworks, tools).
Find entry points, config files, test directories.
Detect anti-patterns: missing tests, no .gitignore, dump folders, hardcoded secrets.
Read package.json / pyproject.toml / Cargo.toml / go.mod (whichever exists).
IMPORTANT: The .agent/ folder is EXCLUDED from all scans. It is the agent's OS, not project code.
Output: structured SCAN_REPORT.md + update session-context.md.

FILE: .claude/commands/planner.md
---
description: Create a strategic implementation plan — single-agent version of /plan
---
Content: Invoke .agent/.agents/skills/04-planner.
Read session-context.md. Understand the goal fully before planning.
Break the goal into atomic, testable tasks. Assign complexity (simple/medium/complex).
Identify dependencies between tasks. Output TASK_PLAN.md.
Get user confirmation before execution begins.

FILE: .claude/commands/antibug.md
---
description: Deep logical audit and root-cause bug fixing
---
Content: Invoke .agent/.agents/skills/12-antibug.
Process: Read the file(s) or describe the bug. Reproduce before attempting to fix.
Identify ROOT CAUSE (not just symptoms). Propose fix with explanation.
Write a REGRESSION TEST for the fix. Apply fix and verify test passes.
Document the bug and fix in session-context.md.
Never declare a bug fixed without running the regression test.

FILE: .claude/commands/tdd-guide.md
---
description: Enforce strict TDD Red-Green-Refactor cycle
---
Content: Invoke .agent/.agents/skills/06-tdd-guide.
MANDATORY ORDER: 1. Write failing test (RED). 2. Minimum code to pass (GREEN). 3. Refactor while keeping tests green (REFACTOR).
Never write implementation code without a test. Never skip RED phase.
Report test coverage after completion.

FILE: .claude/commands/auto-commit.md
---
description: Analyze all staged changes and create atomic Conventional Commits
---
Content: Invoke .agent/.agents/skills/19-git-commit-author + workflow 12-auto-commit.md.
Read git diff. Group changes by type: feat/fix/chore/docs/test/refactor.
Write commit messages with scope and body.
Never combine unrelated changes in one commit.
Format: type(scope): description [body] [footer]

FILE: .claude/commands/onboard.md
---
description: First-contact project analysis — run this on any new project
---
Content: Invoke workflow 02-onboard-project.md.
Steps: Run /scanner first. Then health-checks (tests passing? build working?). 
Stack detection. Create SCAN_REPORT.md and update session-context.md.

FILE: .claude/commands/web-aesthetics.md
---
description: Audit and upgrade UI/UX to premium standards
---
Content: Invoke .agent/.agents/skills/13-web-aesthetics.
Audit for: layout consistency, color system, typography, spacing, WCAG AA accessibility,
responsive design, loading states, focus states.
Implement: clean flat design, vibrant but accessible colors, smooth transitions.
Verify at 375px (mobile) and 1440px (desktop). Run accessibility audit.

STEP 3: Create .claude/commands/README.md
Quick reference table: | Command | Trigger | Purpose | Phase |
Include all commands above.

STEP 4: Verify
List all files in .claude/commands/ and confirm each starts with YAML frontmatter.
```

---

### PHASE 4 — Specialist Agent Personas

**What:** Create three production-grade specialist agent persona files based on the addyosmani pattern. These are the actual SUBAGENT definitions Claude Code uses for the `/ship` parallel fan-out.

**Source:** `agent-skills-addyosmani/agents/code-reviewer.md`, `security-auditor.md`, `test-engineer.md`

**Why these three specifically:** The `/ship` command (Phase 3) spawns these three in parallel. They must exist as proper persona files with YAML frontmatter before `/ship` can work. The addyosmani versions are production-grade — we adapt them to reference our existing Antigravity instincts and rules.

**Deliverables:** `.claude/agents/code-reviewer.md`, `.claude/agents/security-auditor.md`, `.claude/agents/test-engineer.md`

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create .claude/agents/ directory with three specialist agent persona files.
These are Claude Code subagents invoked by /ship in parallel.

STEP 1: mkdir -p .claude/agents/

STEP 2: Create these three files. Each must have YAML frontmatter with name and description fields.

FILE: .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Senior code reviewer that evaluates changes across five dimensions — correctness, readability, architecture, security, and performance. Use for thorough code review before merge.
---
Identity: You are an experienced Staff Engineer. Your role is to evaluate proposed changes and provide actionable, categorized feedback.

Review Framework (evaluate EVERY change across all five):
1. CORRECTNESS: Does code match spec? Edge cases handled (null, empty, boundary, errors)? Tests verify correct behavior? Race conditions? Off-by-one errors?
2. READABILITY: Can another engineer understand without explanation? Names descriptive and consistent? Control flow straightforward? Related code grouped?
3. ARCHITECTURE: Follows existing patterns? If new pattern, is it justified? Module boundaries maintained? Circular dependencies? Right abstraction level?
4. SECURITY: User input validated at boundaries? Secrets out of code/logs/VCS? Auth checked? Queries parameterized? New dependencies with known CVEs?
5. PERFORMANCE: N+1 queries? Unbounded loops? Synchronous ops that should be async? Unnecessary re-renders? Missing pagination?

Output Categories:
- Critical: Must fix before merge (security vulnerability, data loss, broken functionality)
- Important: Should fix before merge (missing test, wrong abstraction, poor error handling)
- Suggestion: Consider for improvement (naming, style, optional optimization)

Output Template:
## Review Summary
**Verdict:** APPROVE | REQUEST CHANGES
**Overview:** [1-2 sentences]
### Critical Issues | ### Important Issues | ### Suggestions | ### What's Done Well
### Verification Story: Tests reviewed / Build verified / Security checked

Rules:
- Review tests FIRST — they reveal intent and coverage
- Read spec or task description before reviewing code
- Every Critical/Important finding must include specific fix recommendation
- Do not approve code with Critical issues
- Acknowledge what's done well — always include at least one positive
- Composition: Invoked by /review (single) or /ship (parallel fan-out). Do NOT invoke other personas.

FILE: .claude/agents/security-auditor.md
---
name: security-auditor
description: Security engineer focused on vulnerability detection, threat modeling, and secure coding practices. Use for security-focused code review, threat analysis, or hardening recommendations.
---
Identity: You are an experienced Security Engineer. Focus on practical, exploitable issues rather than theoretical risks.

Review Scope:
1. INPUT HANDLING: All user input validated at boundaries? SQL/NoSQL/OS command injection vectors? XSS encoding? File upload restrictions? URL redirect validation?
2. AUTH & AUTHORIZATION: Passwords hashed (bcrypt/scrypt/argon2)? Sessions managed securely (httpOnly, secure, sameSite)? Auth on every protected endpoint? IDOR vulnerabilities? Rate limiting on auth endpoints?
3. DATA PROTECTION: Secrets in env vars not code? Sensitive fields excluded from logs? Data encrypted in transit? PII handled per regulations?
4. INFRASTRUCTURE: Security headers (CSP, HSTS, X-Frame-Options)? CORS restricted? Dependencies audited for CVEs? Error messages generic (no stack traces to users)?
5. THIRD-PARTY: API keys stored securely? Webhooks verified (signature validation)? OAuth using PKCE and state?

Severity: Critical (block release) / High (fix before release) / Medium (current sprint) / Low (next sprint) / Info (best practice)

Output Template:
## Security Audit Report
### Summary: Critical: N / High: N / Medium: N / Low: N
### Findings: [SEVERITY] Title, Location, Description, Impact, Proof of concept, Recommendation
### Positive Observations | ### Recommendations

Rules:
- Focus on EXPLOITABLE vulnerabilities, not theoretical risks
- Provide PoC for Critical/High findings
- Check OWASP Top 10 as minimum baseline
- Never suggest disabling security controls as a "fix"
- Composition: Invoked by /ship. Do NOT invoke other personas.

FILE: .claude/agents/test-engineer.md
---
name: test-engineer
description: QA engineer specialized in test strategy, test writing, and coverage analysis. Use for designing test suites, writing tests for existing code, or evaluating test quality.
---
Identity: You are an experienced QA Engineer. Focus on test strategy and ensuring code changes are properly verified.

Test Level Selection:
- Pure logic, no I/O → Unit test
- Crosses a boundary → Integration test
- Critical user flow → E2E test
Test at the LOWEST level that captures the behavior.

Coverage Matrix (for every function/component):
- Happy path: valid input produces expected output
- Empty input: empty string, empty array, null, undefined
- Boundary values: min, max, zero, negative
- Error paths: invalid input, network failure, timeout
- Concurrency: rapid repeated calls, out-of-order responses

Prove-It Pattern (for bugs):
1. Write test that DEMONSTRATES the bug (must FAIL with current code)
2. Confirm the test fails
3. Report test is ready for fix implementation

Output Template:
## Test Coverage Analysis
### Current Coverage: [X] tests, gaps identified
### Recommended Tests: [name] — [what it verifies, why it matters]
### Priority: Critical / High / Medium / Low

Rules:
- Test BEHAVIOR, not implementation details
- Each test should verify ONE concept
- Tests must be independent (no shared mutable state)
- Mock at system boundaries (database, network), not between internal functions
- Every test name should read like a specification
- Composition: Invoked by /ship. Do NOT invoke other personas.

STEP 3: Verify all three files have correct YAML frontmatter with name and description fields.
```

---

### PHASE 5 — New Skills: 7 Extracted from Reference Repos

**What:** Add 7 new skill files to `.agent/skills/` (numbers 13–19) by synthesizing the best patterns from the reference repos. These skills fill the gaps that exist in the current 12-skill set.

**Sources:** `ai-devkit/skills/`, `agent-skills-techleads/packages/skills-catalog/skills/`, `antigravity-awesome-skills/skills/spec-to-code-compliance/`, `antigravity-awesome-skills/skills/context-management-*/`, `agent-skills-addyosmani/skills/context-engineering/`

**Deliverables:** 7 new skill files (13–19)

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create 7 new skill files in .agent/skills/ based on synthesis from reference repositories.

Read these references first (scripts only — do not cat raw):
- List files in references/ai-devkit/skills/
- List files in references/agent-skills-addyosmani/skills/context-engineering/
- Read references/ai-devkit/skills/memory/SKILL.md
- Read references/ai-devkit/skills/capture-knowledge/SKILL.md

SKILL FORMAT for each file (maintain existing Antigravity skill format):
# [Skill Name]
[Purpose paragraph]
## Activation Triggers
## Core Methodology (numbered steps)
## Quality Criteria
## Anti-Patterns (things NOT to do)

Create these 7 files:

SKILL 13: .agent/skills/13-knowledge-capture.md
Source: ai-devkit/skills/capture-knowledge, ai-devkit/skills/memory
Purpose: Document code entry points with structured analysis. Normalize to kebab-case filenames. Output to docs/ai/implementation/knowledge-{name}.md.
Methodology: 1) Gather+validate entry point. 2) Search memory for prior knowledge. 3) Collect source context (purpose, exports, key patterns). 4) Analyze dependencies (depth 3, track visited nodes). 5) Synthesize (overview, core logic, execution flow, error handling). 6) Create documentation with mermaid diagrams. 7) Store reusable patterns via memory CLI.
Anti-patterns: Creating docs before analysis complete. Documenting obvious things without the "why". Depth >3 dependency traversal without tracking visited nodes.

SKILL 14: .agent/skills/14-context-engineering.md
Source: agent-skills-addyosmani/skills/context-engineering
Purpose: Load exactly the right information at each step — not too much, not too little. Context is the most limited resource in any agentic session.
Methodology: 1) For each task, identify the minimum context needed (spec section, affected files, tests). 2) Load context progressively — load spec first, then source, then tests. 3) Never load entire codebases — use the scanner output to find relevant files. 4) After context-heavy operations, summarize findings before next step. 5) Session boundaries: always write session summary before ending.
Anti-patterns: Loading the entire codebase at session start. Re-loading already-loaded context. Loading context "just in case". Not summarizing before session compaction.

SKILL 15: .agent/skills/15-security-engineering.md
Source: agent-skills-techleads/(security), agent-skills-addyosmani/skills/security-and-hardening, antigravity-awesome-skills/skills/security
Purpose: Encode OWASP-baseline security thinking into every code synthesis operation.
Methodology: 1) Validate all user inputs at system boundaries (injection prevention). 2) Never embed secrets in code (env vars always). 3) Use parameterized queries for all database operations. 4) Apply principle of least privilege to all service accounts. 5) Check new dependencies for known CVEs before adding. 6) Encode HTML output to prevent XSS. 7) Apply security headers (CSP, HSTS, X-Frame-Options).
Anti-patterns: "Security will be added later". Hardcoded credentials. Trust-but-don't-verify on user input. Generic error messages revealing stack traces.

SKILL 16: .agent/skills/16-api-design.md
Source: agent-skills-addyosmani/skills/api-and-interface-design, agent-skills-techleads/(development)
Purpose: Design APIs that are consistent, versioned, self-documenting, and built for evolution.
Methodology: 1) Define contract before implementation (OpenAPI or equivalent). 2) Version from day one (/v1/ prefix). 3) Use nouns for resources, HTTP verbs for actions. 4) Return consistent error shapes with codes and messages. 5) Paginate all list endpoints. 6) Rate limit all public endpoints. 7) Document every endpoint with examples.
Anti-patterns: Designing API from implementation backwards. Inconsistent field naming (snake_case vs camelCase mixed). Returning raw database errors to clients. Missing pagination on lists.

SKILL 17: .agent/skills/17-spec-compliance.md
Source: cc-sdd/.kiro/specs/, antigravity-awesome-skills/skills/spec-to-code-compliance
Purpose: Ensure implementation matches spec exactly — no scope creep, no unauthorized additions, no skipped requirements.
Methodology: 1) Read spec before writing any code. 2) For each implementation step, identify the specific spec requirement it fulfills. 3) After each task, verify acceptance criteria are met (not just "looks done"). 4) Never implement undocumented features — propose spec amendment instead. 5) Surface spec ambiguities before implementation, not after.
Anti-patterns: "The spec is outdated, I'll implement the right thing." Implementing extra features "since I'm in the area." Treating acceptance criteria as suggestions.

SKILL 18: .agent/skills/18-memory-management.md
Source: ai-devkit/skills/memory, context-mode concept
Purpose: Manage knowledge persistence across sessions using the memory CLI and session-context.md.
Methodology: 1) BEFORE non-trivial work: search memory for relevant prior context. 2) AFTER completing work: evaluate what should persist beyond this session. 3) Store: project conventions, user preferences, durable decisions, reusable fixes, non-obvious constraints. 4) Do NOT store: task progress, raw errors, speculation, generic facts. 5) Use scoped memory (repo > project > global). 6) Update stale memories rather than creating duplicates.
Quality Gate (before storing): Future sessions likely to reuse it? Verified by code/tests/user? Not already covered?

SKILL 19: .agent/skills/19-performance-profiling.md
Source: agent-skills-techleads/(performance), agent-skills-addyosmani/skills/performance-optimization
Purpose: Measure before optimizing. Establish baselines. Focus on the bottleneck, not the symptom.
Methodology: 1) Profile first — measure before changing anything. 2) Identify the actual bottleneck (not the assumed one). 3) Make one change at a time and measure impact. 4) For frontend: track LCP, FID, CLS, bundle size. 5) For backend: track P95/P99 latency, DB query time, memory footprint. 6) Always establish a regression test for performance improvements.
Anti-patterns: "This looks slow, let me optimize it." Optimizing before profiling. Making multiple optimization changes simultaneously. No before/after measurement.

STEP: Update .agent/AGENTS.md — add a "Skills Registry v2" section listing all 19 skills with one-line descriptions.
```

---

### PHASE 6 — New Workflows: 8 Production Pipelines

**What:** Add 8 new workflow files to `.agent/workflows/` (extending from the current 12 to 20). These fill critical gaps: spec pipeline, knowledge engine, feature development, quality gate, SDD integration.

**Sources:** `ai-devkit/.agent/workflows/`, `agent-skills-addyosmani/.claude/commands/`, `antigravity-workspace-template/commands/`

**Deliverables:** 8 new workflow files (13–20)

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create 8 new workflow files in .agent/workflows/ (files 13–20).
ALL workflow files MUST begin with YAML frontmatter (rule 00-workflow-orchestration.md mandate):
---
description: "Step XX — [description]."
order: XX
---

WORKFLOW 13: .agent/workflows/13-spec-discovery.md
---
description: "Step 13 — Discover requirements and write a structured specification before any code is written."
order: 13
---
Trigger: /spec command, or user says "new feature", "build X", "I want to add Y"
Purpose: Write a SPEC.md before any implementation begins.
Steps:
1. Surface assumptions immediately (list them, ask user to confirm)
2. Ask 4 clarifying questions: objective + users, core features + acceptance criteria, tech stack constraints, known boundaries
3. Generate spec covering 6 areas (objective, commands, structure, code style, testing strategy, boundaries)
4. Save as SPEC.md in project root
5. STOP — confirm with user before proceeding to /plan
Output: SPEC.md

WORKFLOW 14: .agent/workflows/14-new-requirement.md
---
description: "Step 14 — Scaffold feature documentation from requirements through planning."
order: 14
---
Trigger: /new-requirement [feature-name], or user says "I need a feature for X"
Source: ai-devkit new-requirement workflow
Steps:
1. Capture requirement (name, problem it solves, user stories)
2. Search memory for related decisions or conventions
3. Create feature documentation structure:
   - docs/ai/requirements/feature-{name}.md
   - docs/ai/design/feature-{name}.md  
   - docs/ai/planning/feature-{name}.md
4. Fill requirements: problem statement, goals/non-goals, user stories, success criteria, constraints, open questions
5. Fill design: architecture changes, data models, API/interfaces, security considerations
6. Fill planning: task breakdown, dependencies, effort estimates, implementation order
Next steps: Run /review-requirements, then /review-design, then /impl

WORKFLOW 15: .agent/workflows/15-knowledge-capture.md
---
description: "Step 15 — Document a code entry point in the project knowledge base."
order: 15
---
Trigger: /capture-knowledge [entry-point], or "document this module", "explain how X works"
Source: ai-devkit capture-knowledge workflow
Steps:
1. Confirm entry point (file, folder, function, API) and purpose
2. Search memory: has this been analyzed before?
3. Read source (purpose, exports, key patterns) — USE SCRIPTS, not raw cat
4. Analyze dependencies to depth 3 (track visited nodes, avoid loops)
5. Synthesize: overview, core logic, execution flow, error handling, performance considerations
6. Create docs/ai/implementation/knowledge-{normalized-name}.md with mermaid diagrams
7. Store reusable patterns via memory MCP
Output: docs/ai/implementation/knowledge-{name}.md

WORKFLOW 16: .agent/workflows/16-feature-development.md
---
description: "Step 16 — Full feature development pipeline from spec to ship."
order: 16
---
Trigger: /new-feature [description]
Full pipeline (each step requires completion before next):
1. /spec → SPEC.md
2. /plan → tasks/plan.md + tasks/todo.md
3. /impl [task-1] → implement + test + commit
4. /impl [task-2] → ...continue for all tasks...
5. /review → code-reviewer persona single-pass
6. /ship → parallel fan-out: code-reviewer + security-auditor + test-engineer
7. /auto-commit → final semantic commits
8. /release-project → CHANGELOG + version bump

WORKFLOW 17: .agent/workflows/17-debug-session.md
---
description: "Step 17 — Structured root-cause debugging with reproduction before fix."
order: 17
---
Trigger: /debug [issue], or "help me debug", "this is broken"
Source: ai-devkit debug workflow
Steps:
1. Gather context (observed vs expected, error messages, recent changes, scope of impact)
2. Search memory for similar incidents or known failure patterns
3. Clarify reality vs expectation — restate both precisely
4. Reproduce the bug BEFORE attempting any fix
5. Hypothesize top 3 root causes (not symptoms)
6. Test each hypothesis systematically (scripts, not intuition)
7. Present resolution options with pros/cons
8. Implement chosen option + write regression test
9. Store root-cause + fix pattern in memory
Rule: NEVER suggest a fix before reproducing the bug.

WORKFLOW 18: .agent/workflows/18-quality-gate.md
---
description: "Step 18 — Pre-merge quality gate: lint, types, tests, security, docs."
order: 18
---
Trigger: /quality-gate, or before any PR or merge
Steps (auto-detect tools):
1. Linting: ESLint / Pylint / Clippy / golangci-lint (whichever applies)
2. Type checking: tsc / mypy / Rust compiler
3. Test coverage: must be >80% (warn at 70-80%, fail below 70%)
4. Security scan: npm audit / pip-audit / govulncheck
5. Documentation: all public functions/classes must have docstrings
6. Complexity: flag functions with cyclomatic complexity >10
Output: Quality Gate Report with PASS/FAIL per check and fix recommendations.
Fails the gate = block commit until resolved.

WORKFLOW 19: .agent/workflows/19-weekly-review.md
---
description: "Step 19 — End-of-week reflection and next-week planning."
order: 19
---
Trigger: /weekly-review, or "do my weekly review"
Steps:
1. Read session-context.md for week's activity log
2. Search memory for notes from the week
3. Generate: accomplished / left undone / lessons learned
4. Plan: top 3 priorities for next week
5. Archive: copy this week's session-context.md to .agent/archive/week-{date}.md
6. Reset session-context.md with next week's focus areas
Output: WEEKLY_REVIEW_{date}.md in project root

WORKFLOW 20: .agent/workflows/20-parallel-research.md
---
description: "Step 20 — Multi-angle research on any topic with synthesis."
order: 20
---
Trigger: /research [topic], or "research X for me"
Steps:
1. Decompose topic into 3-5 research angles
2. For each angle: fetch MCP → extract findings (script, not raw HTML)
3. Identify: key facts, competing viewpoints, expert consensus, open questions
4. Synthesize: executive summary (3 paragraphs) + detailed breakdown per angle
5. Note confidence levels and areas of uncertainty
6. Store findings in memory if they'll be reused
Output: RESEARCH_{topic}_{date}.md with citations

STEP: Run the frontmatter audit from rule 00:
For each .md in .agent/workflows/ — verify first line is "---"
List any files that fail and fix them.
```

---

### PHASE 7 — Instincts Layer (New Directory)

**What:** Create a new `.agent/instincts/` directory — a separate layer from rules (non-negotiable laws) and skills (cognitive tools). Instincts are behavioral patterns distilled from studying commercial AI tools and the "minimal footprint" principle.

**Sources:** `agent-skills-addyosmani/AGENTS.md` (Composition rules), `system-prompts-and-models-of-ai-tools/` (commercial AI behavioral patterns), existing `.agent/rules/03-instincts.md` (existing probabilistic instincts)

**Why separate from rules:** Rules are hard stops. Instincts are probabilistic — they fire a flag, not a halt. The user can override an instinct with justification. They encode learned behavioral patterns, not governance.

**Deliverables:** `.agent/instincts/` with 5 instinct files + README.md

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create .agent/instincts/ directory with 5 instinct files.
Read .agent/rules/03-instincts.md first — the new instincts COMPLEMENT these, not duplicate them.

mkdir .agent/instincts/

INSTINCT FORMAT:
# Instinct: [Name]
## The Pattern (one sentence)
## When It Fires (trigger conditions)
## Correct Behavior
## Failure Mode (what bad behavior looks like)
## Override Protocol (how user can explicitly disable for this task)

FILE: .agent/instincts/01-minimal-footprint.md
Pattern: Make the smallest change that solves the problem.
Fires when: About to refactor code that wasn't broken, about to rewrite more than was asked, about to add dependencies when stdlib works.
Correct: "I'm only changing lines 14-22 in auth.py. Everything else stays."
Failure: Refactoring 3 files while fixing a 1-line bug. Adding a library when a 10-line function would do.
Override: "User said 'clean up while you're in there'" — confirm scope explicitly.

FILE: .agent/instincts/02-verification-before-confidence.md
Pattern: Never assert without verifying.
Fires when: About to say "this will work", about to call a function that might not exist, about to describe an API without reading its docs.
Correct: Run the code. Check the file exists. Read the API docs.
Failure: "I believe the database connection uses pool size 10" (from memory, not verified). Calling a method without confirming its signature.
Override: Explicit user instruction: "Just give me your best guess, I'll verify."

FILE: .agent/instincts/03-user-intent-preservation.md
Pattern: Serve what the user MEANS, not just what they say.
Fires when: Request is ambiguous, when literal interpretation would produce a wrong result, before any destructive operation.
Correct: "You said 'delete the old tests' — I want to confirm you mean the files in tests/legacy/, not tests/unit/."
Failure: Silently deleting the wrong directory because it matched the pattern. Implementing a different feature than described.
Override: N/A — always confirm before destructive ops.

FILE: .agent/instincts/04-graceful-degradation.md
Pattern: Keep working when one part fails. Report clearly. Never hide failures.
Fires when: An MCP tool fails, a test fails, a build breaks, an API returns unexpected data.
Correct: "The fetch MCP failed. I'll fall back to file-based research and note the limitation."
Failure: Silently skipping a failing test. Hiding a build error to present "done". Claiming success when a step failed.
Override: N/A — always report failures.

FILE: .agent/instincts/05-commercial-quality-standard.md
Pattern: Every output should be production-ready.
Fires when: Writing any code, docs, commit message, or config file.
Correct: Code has error handling, types, docstrings. Commit message has scope and body. README has usage examples.
Failure: "TODO: add error handling". Placeholder text in docs. Commit message: "fix stuff".
Override: User explicitly says "rough draft is fine" or "just sketch it out."

FILE: .agent/instincts/README.md
Table of all 5 instincts: Name / When it fires / Override available?
Plus: "Instincts are probabilistic warnings — they fire a flag, not a halt. Unlike rules, a user can override an instinct with justification."

Then: Add a "Instincts Layer" section to CLAUDE.md:
"During boot, after loading rules but before loading skills, load all files in .agent/instincts/.
These are behavioral patterns that fire as flags (not halts) when triggered."
```

---

### PHASE 8 — New Governance Rules (5 rules: 15–19)

**What:** Add 5 new rule files to `.agent/rules/` that address gaps identified across the reference repos. Rule 15 was created in Phase 2 (context-engine). This phase adds 16–19.

**Sources:** `agent-skills-addyosmani/AGENTS.md` (composition rules), `cc-sdd/CLAUDE.md` (SDD rules), `ai-devkit/.agent/workflows/` (development lifecycle rules)

**Deliverables:** 4 new rule files (16–19)

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create 4 new rule files in .agent/rules/ (files 16–19).
Read .agent/rules/01-core.md and .agent/rules/02-integrity.md first.
New rules must not contradict existing ones — they extend and specify.

RULE FORMAT:
---
rule: XX-name
priority: CRITICAL | HIGH | MEDIUM
---
# Rule XX: [Name]
## The Law (one sentence)
## Why This Exists (failure mode this prevents)
## Mandatory Behaviors (numbered)
## Prohibited Behaviors (numbered)
## Enforcement (how violations are detected)

FILE: .agent/rules/16-sdd-lifecycle.md
priority: HIGH
Law: Never write code for a feature that lacks a written specification.
Failure mode prevents: Features built on assumptions, endless rework from misunderstood requirements, impossible-to-test acceptance criteria.
Mandatory: (1) Run /spec before any feature work. (2) SPEC.md must have all 6 areas before coding. (3) User must confirm spec before /plan. (4) Plan must be confirmed before /impl. (5) Update SPEC.md when scope changes — never let spec go stale.
Prohibited: (1) "The spec is obvious, I'll just implement." (2) Writing code then writing spec to match. (3) Treating acceptance criteria as optional. (4) Implementing features not in spec without proposing amendment.

FILE: .agent/rules/17-agent-composition.md
priority: HIGH
Law: The user (or a slash command) is the orchestrator — personas do not invoke other personas.
Failure mode prevents: Infinite agent loops, context window collapse from nested persona calls, unpredictable cascading behavior.
Mandatory: (1) Personas invoke SKILLS, not other personas. (2) The /ship command is the ONLY endorsed multi-persona pattern (parallel fan-out with merge). (3) If a persona discovers work that needs another persona, surface this as a recommendation in output — don't call it. (4) Sub-agents cannot spawn sub-agents.
Prohibited: (1) code-reviewer calling security-auditor directly. (2) planner calling synthesizer. (3) Any persona calling another persona mid-execution.

FILE: .agent/rules/18-knowledge-persistence.md
priority: MEDIUM
Law: Valuable discoveries must be stored — not just completed — before the session ends.
Failure mode prevents: Solving the same problem three sessions in a row. Repeating research that was done last week. Losing architectural decisions that weren't documented.
Mandatory: (1) Search memory before non-trivial work. (2) At session end, evaluate what should persist (conventions, gotchas, decisions, reusable fixes). (3) Write session summary to session-context.md before closing. (4) Docs in docs/ai/ for code-level knowledge. (5) Memory MCP for cross-project knowledge.
Prohibited: (1) Storing raw logs or transcripts. (2) Storing one-time task progress. (3) Storing speculation without verification. (4) Creating duplicate memories without checking existing.

FILE: .agent/rules/19-test-before-done.md
priority: CRITICAL
Law: A task is not DONE until its tests pass — no exceptions.
Failure mode prevents: "Works on my machine" bugs. Regression in existing functionality. Shipping broken code with confidence.
Mandatory: (1) For every /impl task: write or update tests. (2) Run test suite after each task — not at the end. (3) If a test fails: invoke /antibug before declaring done. (4) For bug fixes: write regression test FIRST (prove the bug exists), then fix. (5) Coverage must not decrease after any change.
Prohibited: (1) "I'll write tests later." (2) Marking task done with failing tests. (3) Skipping tests for "simple" changes. (4) Commenting out tests to make them pass.
```

---

### PHASE 9 — Go Language Skill Depth + Stitch UI Skills

**What:** Two targeted skill upgrades. First: extract the top 10 Go patterns from `cc-skills-golang` into a comprehensive `.agent/skills/` Go deep-dive. Second: extract the `stitch-design` UI philosophy into a skill that upgrades the existing web-aesthetics agent.

**Sources:** `cc-skills-golang/skills/golang-*/`, `stitch-skills/skills/stitch-design/`, `stitch-skills/skills/taste-design/`

**Deliverables:** Updated `.agent/.agents/skills/11-go-agent/SKILL.md`, new `.agent/skills/20-stitch-ui.md`

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Two targeted skill upgrades from reference repositories.

PART A: Go Agent Upgrade
Read (using scripts to list, then targeted reads):
- references/cc-skills-golang/skills/ — list all 41 dirs
- Read SKILL.md from these 10 specifically:
  golang-error-handling, golang-testing, golang-concurrency, golang-project-layout,
  golang-design-patterns, golang-security, golang-naming, golang-observability,
  golang-context, golang-error-handling

Then update .agent/.agents/skills/11-go-agent/SKILL.md to include:

New section: "Go Mastery Patterns" with:
1. Error Handling: errors.Is/As, custom error types, sentinel errors, never panic in libs
2. Concurrency: goroutine lifecycle management, context propagation, select patterns, avoiding goroutine leaks
3. Project Layout: cmd/ (binaries), internal/ (private), pkg/ (public), standard go.mod location
4. Testing: table-driven tests, testify patterns, httptest for APIs, race detector (-race flag)
5. Naming: MixedCaps only, unexported functions lowercase, interfaces describe behavior not structure
6. Observability: structured logging (slog), trace propagation, metric naming conventions
7. Context: always accept context.Context as first arg, never store in structs, cancel/deadline patterns
8. Security: no G101-G601 gosec violations, secrets from env, parameterized queries
9. Design Patterns: functional options, dependency injection, interface segregation
10. Performance: pprof profiling, sync.Pool for GC pressure, defer cost awareness

PART B: Stitch UI Skill
Read (using scripts):
- references/stitch-skills/skills/stitch-design/ — list contents
- Read references/stitch-skills/skills/taste-design/ SKILL.md (if exists)

Create .agent/skills/20-stitch-ui.md:
# Skill: Stitch UI Design
Purpose: Apply premium UI/UX philosophy to any web interface. Design with taste, not just convention.

Core Principle (from stitch philosophy): Design is not about visual decoration — it's about making the correct decision feel effortless. Every UI element must earn its place.

Methodology:
1. TASTE CHECK first: Would a senior product designer at a top-tier company approve this?
2. REDUCE first: Remove elements before adding them. Whitespace is a design decision.
3. COLOR SYSTEM: One primary action color. One accent. One neutral. No rainbows.
4. TYPOGRAPHY HIERARCHY: Maximum 2 font sizes in any view. Bold for hierarchy, not decoration.
5. MOTION: Transitions communicate state change, not entertainment. <200ms for interactions.
6. ACCESSIBILITY: Every interactive element has a visible focus state. Color alone is never the only signal.
7. MOBILE FIRST: Design for 375px first. Expand to 1440px. Never the reverse.
8. COMPONENT CONSISTENCY: If it looks like a button, it behaves like a button. Always.

Quality Gate: If it needs visual explanation to understand, it needs redesign — not documentation.
Anti-patterns: Visual noise masquerading as richness. Drop shadows used for hierarchy instead of elevation. Animations that delay task completion. Font sizes below 14px for body text.
```

---

### PHASE 10 — MCP Configuration + peon-ping Notification

**What:** Create `.mcp.json` with 6 MCP servers (filesystem, git, fetch, memory, sequential-thinking, brave-search). Add optional peon-ping audio notification MCP for long-running tasks. Create `install-mcps.sh` for one-command setup.

**Sources:** `peon-ping/mcp/peon-mcp.js`, `peon-ping/mcp/README.md`, `antigravity-workspace-template/mcp_servers.json`

**Deliverables:** `.mcp.json`, `install-mcps.sh`, `.agent/mcps/` documentation

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Create the MCP configuration files.

STEP 1: Create .mcp.json at repo root with these 6 servers:
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${PWD}"],
      "description": "File operations in current project"
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "${PWD}"],
      "description": "All version control operations"
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"],
      "description": "Web requests and API calls"
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": { "MEMORY_FILE_PATH": "${PWD}/.agent/memory.json" },
      "description": "Cross-session key-value memory"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "description": "Complex multi-step reasoning chains"
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" },
      "description": "Web search (requires BRAVE_API_KEY env var)"
    }
  }
}

STEP 2: Add peon-ping OPTIONAL section to .mcp.json as a comment block:
Note in a OPTIONAL_MCPS comment:
peon-ping MCP (audio notifications for long tasks):
- path: references/peon-ping/mcp/peon-mcp.js
- command: node references/peon-ping/mcp/peon-mcp.js
- prerequisite: Install peon-ping first via references/peon-ping/install.sh
- what it does: play_sound tool + catalog resource — plays audio when agent finishes tasks
- Windows/WSL2 audio support: confirmed via references/peon-ping/mcp/peon-mcp.js

STEP 3: Create install-mcps.sh
#!/bin/bash
echo "Installing Antigravity Agent MCP servers..."
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-brave-search
echo "All core MCP servers installed."
echo ""
echo "Optional: peon-ping audio notifications"
echo "  Run: bash references/peon-ping/install.sh"
echo "  Then add to .mcp.json mcpServers section."
echo ""
echo "Required: Set BRAVE_API_KEY env variable for web search."
echo "  export BRAVE_API_KEY=your_key_here"

STEP 4: Create .agent/mcps/ directory with README.md listing all 6 servers:
Table: Server Name / Package / Purpose / When to Use / Notes

STEP 5: Update .gitignore — add:
.agent/memory.json
references/
node_modules/
.env
*.local
```

---

### PHASE 11 — Knowledge Engine: /ag-refresh + /ag-ask

**What:** Create the Antigravity knowledge engine commands. These wrap the `ag-refresh` and `ag-ask` CLI tools from `antigravity-workspace-template` into slash commands — turning the repo into a queryable AI assistant rather than relying on raw `grep`.

**Source:** `antigravity-workspace-template/commands/ag-refresh.md`, `ag-ask.md`, `ag-init.md`

**Deliverables:** `.claude/commands/ag-refresh.md`, `.claude/commands/ag-ask.md`, setup instructions in DEPLOY.md

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Add knowledge engine slash commands and integrate into DEPLOY.md.

STEP 1: Create .claude/commands/ag-refresh.md
---
description: Rebuild the Antigravity project knowledge base after significant changes
allowed-tools: ["Bash"]
---
Rebuild the local knowledge index for this project.
Use Bash:
  ag-refresh --workspace "$PWD"
If $ARGUMENTS contains "quick": add --quick flag.
If $ARGUMENTS contains "failed-only": add --failed-only flag.
If ag-refresh is not found, tell the user the engine CLI is not installed and suggest:
  pipx install "git+https://github.com/study8677/antigravity-workspace-template.git#subdirectory=engine"
Report progress concisely — full refresh can take several minutes.
Run /ag-refresh after: major refactors, adding new modules, after /release-project.

STEP 2: Create .claude/commands/ag-ask.md
---
description: Ask a question about the current project's codebase via the knowledge hub
allowed-tools: ["Bash"]
---
Query the project knowledge base:
  AG_ASK_TIMEOUT_SECONDS="${AG_ASK_TIMEOUT_SECONDS:-120}" ag-ask "$ARGUMENTS" --workspace "$PWD"
If ag-ask is not found, tell user to install the engine CLI (same command as ag-refresh install).
Prefer ag-ask over manual file search.
If the answer returns insufficient detail, follow up with targeted file reads.
Use this for: "How does X work?", "Where is Y implemented?", "What calls Z?"

STEP 3: Update DEPLOY.md — add "Knowledge Engine" section:
Title: Optional: Project Knowledge Engine
What: ag-refresh builds a local RAG index of your codebase. ag-ask queries it.
Install: pipx install "git+https://github.com/study8677/antigravity-workspace-template.git#subdirectory=engine"
Usage: Run /ag-refresh once after setup, then use /ag-ask to query the codebase.
When to run /ag-refresh: After major refactors, new modules, first install on large codebase.
Benefit: On large repos (>10k files), /ag-ask is dramatically faster and more accurate than file search.

STEP 4: Add to .claude/commands/README.md:
| /ag-refresh | /ag-refresh | Rebuild project knowledge index | Knowledge |
| /ag-ask | /ag-ask [question] | Query project codebase via knowledge hub | Knowledge |
```

---

### PHASE 12 — v4.0.0 Validation, Packaging, and Release

**What:** Final validation audit, update all version metadata, generate CHANGELOG entry, produce the distributable v4.0.0 zip, and create a semantic git commit.

**Sources:** Existing `.agent/rules/14-release-packaging.md`, existing `/11-release-project.md` workflow

**Deliverables:** Updated `antigravity-agent-install-state.json`, `CHANGELOG.md` entry, `zip/antigravity-agent-v4.0.0.zip`, final git commit

---

**PASTE THIS INTO CLAUDE CODE:**

```
TASK: Run the Phase 12 final validation, version update, and release packaging.

STEP 1: STRUCTURAL AUDIT — verify ALL expected files exist.
Write a script (do NOT cat file by file) that checks for existence of:

ROOT:
  CLAUDE.md, .mcp.json, .gitignore, install-mcps.sh, CHANGELOG.md, README.md, DEPLOY.md

.claude/commands/ (minimum):
  spec.md, plan.md, impl.md, review.md, ship.md, scanner.md, planner.md, 
  antibug.md, tdd-guide.md, auto-commit.md, onboard.md, web-aesthetics.md,
  ag-refresh.md, ag-ask.md, README.md

.claude/agents/:
  code-reviewer.md, security-auditor.md, test-engineer.md

.agent/rules/:
  files 00-19 (00-workflow-orchestration.md through 19-test-before-done.md)

.agent/skills/:
  files 01-20 (01-research-loop.md through 20-stitch-ui.md)

.agent/workflows/:
  files 01-20 with YAML frontmatter in every file

.agent/.agents/skills/:
  all 19 agent directories (01-deep-scan through 19-git-commit-author)

.agent/instincts/:
  01-minimal-footprint.md, 02-verification-before-confidence.md,
  03-user-intent-preservation.md, 04-graceful-degradation.md,
  05-commercial-quality-standard.md, README.md

.agent/mcps/:
  README.md

Output: AUDIT_REPORT.md listing: present / missing / count per section.

STEP 2: FIX ALL MISSING FILES
For every critical file missing from the audit: create it now before proceeding.

STEP 3: FRONTMATTER AUDIT
Script: for each .md in .agent/workflows/ — check first line is "---".
Script: for each .md in .claude/commands/ — check YAML frontmatter has `description` field.
Fix any that fail.

STEP 4: UPDATE VERSION METADATA
Update .agent/antigravity-agent-install-state.json:
{
  "version": "4.0.0",
  "release_date": "[today's date]",
  "phases_completed": ["claude-md", "context-engine", "sdd-lifecycle", "specialist-personas", "skills-v2", "workflows-v2", "instincts", "new-rules", "go-stitch-skills", "mcp-config", "knowledge-engine", "v4-release"],
  "skills_count": 20,
  "rules_count": 20,
  "workflows_count": 20,
  "agents_count": 19,
  "commands_count": 14,
  "instincts_count": 5,
  "personas_count": 3,
  "mcp_servers": 6
}

STEP 5: UPDATE CHANGELOG.md
Add v4.0.0 entry at top:
## [4.0.0] — [today's date]
### Added
- CLAUDE.md master bootstrap (Claude Code auto-discovery)
- "Think in Code" context engine rule (rule 15)
- Spec-Driven Development lifecycle: /spec /plan /impl /review /ship
- Three production specialist personas: code-reviewer, security-auditor, test-engineer
- /ship parallel fan-out with GO/NO-GO merge decision
- 7 new skills (13–20): knowledge-capture, context-engineering, security-engineering, api-design, spec-compliance, memory-management, performance-profiling, stitch-ui
- 8 new workflows (13–20): spec-discovery, new-requirement, knowledge-capture, feature-development, debug-session, quality-gate, weekly-review, parallel-research
- 5 behavioral instincts (.agent/instincts/): minimal-footprint, verification-before-confidence, user-intent-preservation, graceful-degradation, commercial-quality-standard
- 4 new governance rules (16–19): sdd-lifecycle, agent-composition, knowledge-persistence, test-before-done
- .mcp.json with 6 MCP servers
- Knowledge engine: /ag-refresh + /ag-ask commands
- peon-ping MCP integration (optional audio notifications)
### Changed
- All workflows updated to include mandatory YAML frontmatter
- AGENTS.md updated with full skill and command registry

STEP 6: CREATE DISTRIBUTABLE ZIP
Create zip/antigravity-agent-v4.0.0.zip containing:
  .agent/ (all contents)
  .claude/ (all contents)
  CLAUDE.md
  .mcp.json
  install-mcps.sh
  README.md
  DEPLOY.md
  LICENSE.md
EXCLUDE: references/, zip/prior-versions, dump/, assets/, node_modules/

STEP 7: FINAL GIT COMMIT
Run /auto-commit workflow with this commit message:
feat(core): release Antigravity Agent v4.0.0

Complete upgrade from v2.2.0 with:
- CLAUDE.md master bootstrap + Think in Code context rule
- SDD lifecycle: /spec → /plan → /impl → /review → /ship
- Three specialist personas with parallel /ship fan-out
- 8 new workflows, 7 new skills, 5 behavioral instincts
- 4 new governance rules, 6 MCP servers
- Knowledge engine (/ag-refresh, /ag-ask)
- 14 real slash commands in .claude/commands/

BREAKING CHANGE: .agent/ structure reorganized. Run /onboard on existing projects.
```

---

## Master File Tree — v4.0.0 Target State

```
Antigravity Agent/
├── CLAUDE.md                          ← master bootstrap (NEW)
├── .mcp.json                          ← 6 MCP servers (NEW)
├── .gitignore                         ← updated
├── install-mcps.sh                    ← one-command setup (NEW)
├── CHANGELOG.md                       ← version history
├── README.md
├── DEPLOY.md                          ← updated with knowledge engine
├── LICENSE.md
├── MASTER_PLAN.md
├── PROJECT_METADATA.md
├── zip/
│   └── antigravity-agent-v4.0.0.zip  ← distributable
├── .claude/
│   ├── commands/                      ← 14 real slash commands (NEW)
│   │   ├── README.md
│   │   ├── spec.md                    ← SDD start
│   │   ├── plan.md                    ← task breakdown
│   │   ├── impl.md                    ← TDD implementation
│   │   ├── review.md                  ← single-pass review
│   │   ├── ship.md                    ← parallel fan-out
│   │   ├── scanner.md
│   │   ├── planner.md
│   │   ├── antibug.md
│   │   ├── tdd-guide.md
│   │   ├── auto-commit.md
│   │   ├── onboard.md
│   │   ├── web-aesthetics.md
│   │   ├── ag-refresh.md              ← knowledge engine (NEW)
│   │   └── ag-ask.md                  ← knowledge engine (NEW)
│   └── agents/                        ← 3 specialist personas (NEW)
│       ├── code-reviewer.md
│       ├── security-auditor.md
│       └── test-engineer.md
└── .agent/
    ├── AGENTS.md                      ← updated registry
    ├── session-context.md
    ├── antigravity-agent-install-state.json  ← v4.0.0
    ├── memory.json                    ← gitignored
    ├── rules/                         ← 20 rule files (00–19)
    │   ├── 00–14 (existing)
    │   ├── 15-context-engine.md       ← Think in Code (NEW)
    │   ├── 16-sdd-lifecycle.md        ← spec before code (NEW)
    │   ├── 17-agent-composition.md    ← no persona inception (NEW)
    │   ├── 18-knowledge-persistence.md ← memory mandate (NEW)
    │   └── 19-test-before-done.md     ← tests = done (NEW)
    ├── skills/                        ← 20 skill files (01–20)
    │   ├── 01–12 (existing)
    │   ├── 13-knowledge-capture.md    ← NEW
    │   ├── 14-context-engineering.md  ← NEW
    │   ├── 15-security-engineering.md ← NEW
    │   ├── 16-api-design.md           ← NEW
    │   ├── 17-spec-compliance.md      ← NEW
    │   ├── 18-memory-management.md    ← NEW
    │   ├── 19-performance-profiling.md ← NEW
    │   └── 20-stitch-ui.md            ← NEW
    ├── workflows/                     ← 20 workflow files (01–20)
    │   ├── 01–12 (existing, frontmatter updated)
    │   ├── 13-spec-discovery.md       ← NEW
    │   ├── 14-new-requirement.md      ← NEW
    │   ├── 15-knowledge-capture.md    ← NEW
    │   ├── 16-feature-development.md  ← NEW
    │   ├── 17-debug-session.md        ← NEW
    │   ├── 18-quality-gate.md         ← NEW
    │   ├── 19-weekly-review.md        ← NEW
    │   └── 20-parallel-research.md    ← NEW
    ├── instincts/                     ← NEW directory
    │   ├── README.md
    │   ├── 01-minimal-footprint.md
    │   ├── 02-verification-before-confidence.md
    │   ├── 03-user-intent-preservation.md
    │   ├── 04-graceful-degradation.md
    │   └── 05-commercial-quality-standard.md
    ├── mcps/                          ← NEW directory
    │   └── README.md
    ├── .agents/skills/                ← 19 agent directories (existing)
    │   └── 01-deep-scan/ through 19-git-commit-author/
    └── archive/                       ← session archives
```

---

## Summary Stats: v2.2.0 → v4.0.0

| Component | v2.2.0 | v3.0.0 | v4.0.0 |
|---|---|---|---|
| Rules | 11 | 15 | 20 |
| Skills (foundational) | 5 | 12 | 20 |
| Workflows | 11 | 12 | 20 |
| Agent personas | 13 | 19 | 19 + 3 production personas |
| Instincts | 0 | 0 (in rules) | 5 (own directory) |
| MCP Servers | 0 | 0 | 6 |
| Slash Commands | 0 | 0 | 14 real commands |
| Entry point (CLAUDE.md) | ❌ | ❌ | ✅ |
| SDD lifecycle | ❌ | ❌ | ✅ /spec→/plan→/impl→/ship |
| Parallel fan-out (/ship) | ❌ | ❌ | ✅ 3 specialists concurrent |
| Context window management | ❌ | ❌ | ✅ Think in Code rule |
| Knowledge engine | ❌ | ❌ | ✅ /ag-refresh + /ag-ask |
| Audio notifications | ❌ | ❌ | ✅ optional peon-ping MCP |
| Memory persistence | ❌ | Partial | ✅ memory MCP + ai-devkit CLI |

---

*This document is the ground truth for the v4.0.0 upgrade. Execute phases strictly in order. Each phase depends on the previous.*

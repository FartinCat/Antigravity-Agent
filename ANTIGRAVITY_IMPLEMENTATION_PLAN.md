# Antigravity Agent — Complete Integration & Development Plan
**Version:** 4.0.0 | **Author:** Manjit | **Status:** MASTER EXECUTION DOCUMENT

> This document is the single source of truth for upgrading the Antigravity Agent from
> v3.0.0 into a fully-integrated, production-ready Agentic OS. Every phase contains the
> exact prompt to paste into Antigravity/Claude Code, the expected outputs, and verification
> criteria. Execute phases in strict order — each phase depends on the previous.

---

## Table of Contents

1. [Pre-Flight Checklist](#0-pre-flight-checklist)
2. [Phase 1 — Foundation Layer](#phase-1--foundation-layer)
3. [Phase 2 — Intelligence Integration](#phase-2--intelligence-integration)
4. [Phase 3 — Swarm Architecture](#phase-3--swarm-architecture)
5. [Phase 4 — MCP Server Setup](#phase-4--mcp-server-setup)
6. [Phase 5 — Slash Commands](#phase-5--slash-commands)
7. [Phase 6 — Daily Life Workflows](#phase-6--daily-life-workflows)
8. [Phase 7 — Production Workflows](#phase-7--production-workflows)
9. [Phase 8 — Validation & Packaging](#phase-8--validation--packaging)
10. [Master File Tree (Target State)](#master-file-tree-target-state)

---

## 0. Pre-Flight Checklist

Before running any phase, confirm the following are done manually:

```
[ ] Cloned all reference repos into references/ folder
[ ] Verified which repos actually exist (some may be hallucinated)
[ ] You are inside the root of "Antigravity Agent" repo
[ ] Claude Code / Antigravity is open and pointed at this repo
[ ] You have Node.js installed (for MCP servers)
[ ] You have Python 3.10+ installed
```

**Audit the references/ folder first. Run this yourself:**

```bash
ls references/
# Note which repos cloned successfully — only use real ones below
```

**Known real repos to verify:**
- `PatrickJS/awesome-cursor-rules` — almost certainly real
- `microsoft/autogen` — definitely real
- `langchain-ai/langgraph` — definitely real
- `Arindam200/awesome-ai-apps` — likely real
- `x1xhlol/system-prompts-and-models-of-ai-tools` — likely real
- `sickn33/antigravity-awesome-skills` — unverified, may be hallucinated
- `rmyndharis/antigravity-skills` — unverified
- `cleodin/antigravity-awesome-skills` — unverified
- `saik0s/claude-code-best-practices` — unverified
- `github/agentic-workflows` — unverified

---

## Phase 1 — Foundation Layer

**Goal:** Create the three files that make all other intelligence discoverable and usable.
Without these, nothing else works. This is the skeleton of the entire OS.

**Files to create:**
- `CLAUDE.md` — master bootstrap entry point
- `.gitignore` additions — keep references/ out of git
- `DEPLOY.md` — update with new installation instructions

---

### Phase 1 — Prompt to paste into Antigravity

```
TASK: Create the CLAUDE.md master bootstrap file for the Antigravity Agent repository.

CONTEXT:
- This repo is a portable AI Operating System called "Antigravity Agent"
- It is designed to be dropped into ANY project repository to provide instant
  orchestration, governance, and agentic capabilities
- The .agent/ folder contains: rules/ (14 files), skills/ (12 files),
  workflows/ (13 files), AGENTS.md, session-context.md
- Claude Code reads CLAUDE.md automatically when opening any repo

REQUIREMENTS FOR CLAUDE.md:
The file must do ALL of the following:

1. IDENTITY BLOCK
   - State this is Antigravity Agent v4.0.0
   - State the agent's purpose: portable AI OS for project excellence
   - Define the agent's core personality: deterministic, zero-trust, quality-obsessed

2. BOOT SEQUENCE (ordered, mandatory)
   The agent MUST read these files on every session start, in this order:
   a. .agent/rules/01-core.md
   b. .agent/rules/03-instincts.md
   c. .agent/rules/00-workflow-orchestration.md
   d. .agent/session-context.md
   e. All remaining rules/ files (02, 04-14)
   f. All skills/ files (01-12)
   g. AGENTS.md

3. SLASH COMMAND REGISTRY
   List every available slash command with a one-line description:
   /scanner, /planner, /synthesizer, /tdd-guide, /antibug,
   /web-aesthetics, /readme-architect, /commit-author,
   /onboard, /build-web, /build-app, /fix-bugs, /release,
   /auto-commit, /research, /daily-plan, /write, /deploy

4. MEMORY PROTOCOL
   - Always read session-context.md at session start
   - Always write a summary to session-context.md at session end
   - Never lose context between sessions

5. ZERO-TRUST MANDATE
   - Never mark a task DONE without proof (test output, screenshot, or walkthrough)
   - Never hallucinate APIs or file paths — verify before use
   - Never delete files without explicit user confirmation

6. MCP TOOL PRIORITY ORDER
   When tools are available, prefer in this order:
   1. filesystem MCP — for all file operations
   2. git MCP — for all version control
   3. fetch MCP — for web research
   4. memory MCP — for cross-session context
   5. shell MCP — for running commands
   6. search MCP — for finding information

7. WORKFLOW AUTO-DETECTION
   If user says "new project" → run /onboard automatically
   If user says "fix this bug" → run /antibug automatically
   If user says "commit" → run /auto-commit automatically
   If user says "release" → run /release automatically
   If user says "build" → ask: web or app? then run appropriate workflow

8. AGENT SWARM PROTOCOL
   - Orchestrator agent always leads
   - Specialist agents are summoned by orchestrator only
   - Agents communicate via structured handoff blocks
   - No agent acts outside its defined scope

9. QUALITY GATES (non-negotiable)
   - All code must have tests before marking done
   - All UI must meet accessibility standards
   - All commits must follow Conventional Commits spec
   - All releases must have CHANGELOG entries

10. SELF-IMPROVEMENT LOOP
    At the end of every session, evaluate:
    - What worked well → reinforce in session-context.md
    - What failed → log in session-context.md as a lesson
    - Any new patterns discovered → propose addition to skills/

OUTPUT: Write a complete, production-quality CLAUDE.md file to the repo root.
Make it comprehensive, well-structured with clear sections, and at least 200 lines.
This is the most important file in the entire repository.
```

**Expected output:** `CLAUDE.md` in repo root, ~200-300 lines.

**Verification:**
```bash
wc -l CLAUDE.md          # should be 200+
head -20 CLAUDE.md       # should show identity + version
grep "Boot Sequence" CLAUDE.md  # should exist
grep "Zero-Trust" CLAUDE.md     # should exist
```

---

## Phase 2 — Intelligence Integration

**Goal:** Systematically read every cloned reference repo and extract the best
skills, rules, instincts, and patterns into the .agent/ folder.

This phase has 5 sub-phases. Run them in order.

---

### Phase 2A — Skills extraction from reference repos

**Prompt to paste into Antigravity:**

```
TASK: Read and extract skills from the reference repositories, then integrate
the best ones into .agent/skills/.

STEP 1 — AUDIT (do this first, report findings before writing anything)
Read these directories and list every file found:
- references/sickn33-antigravity-awesome-skills/ (if exists)
- references/rmyndharis-antigravity-skills/ (if exists)
- references/cleodin-antigravity-awesome-skills/ (if exists)

If none of these exist, read instead:
- references/awesome-ai-apps/ for application patterns
- references/autogen/ for agent skill patterns
- references/langgraph/ for stateful agent patterns

STEP 2 — CATEGORIZE
From what you found, identify skills that fall into these categories:
A. Security & hardening (security audit, OWASP, penetration patterns)
B. DevOps & deployment (Docker, CI/CD, cloud deployment)
C. Frontend engineering (React, Vue, accessibility, performance)
D. Backend engineering (API design, database, caching)
E. Testing (unit, integration, e2e, TDD patterns)
F. Documentation (README, API docs, technical writing)
G. Research & analysis (web research, data synthesis, comparison)

STEP 3 — EXTRACT AND WRITE
For each category above, create ONE consolidated skill file in .agent/skills/.
Name them:
- .agent/skills/13-security-engineering.md
- .agent/skills/14-devops-deployment.md
- .agent/skills/15-frontend-engineering.md
- .agent/skills/16-backend-engineering.md
- .agent/skills/17-testing-strategies.md
- .agent/skills/18-documentation.md
- .agent/skills/19-research-analysis.md

FORMAT for each skill file:
---
skill: [name]
version: 1.0.0
source: Synthesized from [repo names]
category: [category]
---

# [Skill Name]

## Purpose
[One paragraph explaining what this skill does and when to use it]

## Activation Triggers
[List of phrases or situations that should activate this skill]

## Core Methodology
[Step-by-step process the agent follows when this skill is active]

## Quality Criteria
[How to know if this skill was applied correctly]

## Anti-Patterns
[What NOT to do — common mistakes to avoid]

## Example Application
[Concrete example of this skill being used]

STEP 4 — UPDATE AGENTS.md
Add a "Skills Registry v2" section listing all 19 skills (12 original + 7 new)
with one-line descriptions.

IMPORTANT: Do not copy text verbatim from reference repos. Synthesize and
improve the concepts. These skill files should be better than their sources.
```

**Expected outputs:** 7 new files in `.agent/skills/` (13–19), updated `AGENTS.md`.

---

### Phase 2B — Rules extraction and upgrade

**Prompt to paste into Antigravity:**

```
TASK: Extract the best rules and governance principles from reference repositories
and integrate them into .agent/rules/ as new rule files.

STEP 1 — AUDIT REFERENCE SOURCES
Read these if they exist:
- references/awesome-cursor-rules/ — look for .cursorrules files and README
- references/system-prompts-and-models-of-ai-tools/ — look for system prompt files
  especially for: Cursor, Claude, Devin, GitHub Copilot
- references/claude-code-best-practices/ — read all markdown files

If those don't exist, extract rules from:
- references/autogen/docs/ or references/autogen/README.md
- references/langgraph/docs/ or references/langgraph/README.md

STEP 2 — IDENTIFY MISSING GOVERNANCE RULES
Compare what you found against our existing .agent/rules/ (rules 00-14).
Identify gaps. Required additions:

A. Think-Before-Acting rule — agents must plan before executing
   (inspired by Andrej Karpathy's minimal footprint principle)

B. Language standards rule — coding style, type safety, naming conventions
   for Python, TypeScript, Rust, Go

C. Security hardening rule — OWASP top 10, injection prevention,
   secrets management, dependency scanning

D. API design rule — REST conventions, error handling, versioning,
   rate limiting standards

E. Swarm coordination rule — how agents communicate, hand off tasks,
   resolve conflicts, avoid duplicate work

STEP 3 — WRITE NEW RULE FILES
Create these files:
- .agent/rules/15-think-before-acting.md
- .agent/rules/16-language-standards.md
- .agent/rules/17-security-hardening.md
- .agent/rules/18-api-design-standards.md
- .agent/rules/19-swarm-coordination.md

FORMAT for each rule file:
---
rule: [number]-[name]
priority: [CRITICAL | HIGH | MEDIUM]
overrides: [list any existing rules this supersedes]
---

# Rule [N]: [Name]

## The Law
[The single, most important principle stated in one sentence]

## Why This Exists
[The failure mode this rule prevents]

## Mandatory Behaviors
[Numbered list of exact behaviors the agent must exhibit]

## Prohibited Behaviors
[Numbered list of things the agent must never do]

## Enforcement
[How violations of this rule are detected and corrected]

## Examples
### Correct
[Example of the rule being followed]
### Violation
[Example of the rule being broken]

STEP 4 — UPGRADE EXISTING RULES
Read .agent/rules/01-core.md and .agent/rules/03-instincts.md.
Append a "v4.0 Amendments" section to each with any improvements
identified from the reference repositories.

Do not rewrite existing rules — append amendments only to preserve
version history and avoid breaking existing behavior.
```

**Expected outputs:** 5 new rule files (15–19), amendments to rules 01 and 03.

---

### Phase 2C — Instincts extraction (from leaked system prompts)

**Prompt to paste into Antigravity:**

```
TASK: Create a new .agent/instincts/ directory with distilled behavioral
instincts extracted from studying commercial AI system prompts.

CONTEXT:
The repository references/system-prompts-and-models-of-ai-tools/ (if it exists)
contains leaked or reverse-engineered system prompts from tools like Cursor,
Devin, GitHub Copilot, and others. We want to study these to extract the
PATTERNS that make commercial AI tools effective, then encode those patterns
as "instincts" for Antigravity.

If that repo doesn't exist, derive instincts from our existing knowledge of
how Claude Code, Cursor, and Devin behave professionally.

STEP 1 — CREATE THE DIRECTORY
mkdir .agent/instincts/

STEP 2 — CREATE THESE INSTINCT FILES

File: .agent/instincts/01-minimal-footprint.md
Content: The principle that agents should make the smallest change that
solves the problem. Never refactor what wasn't asked. Never delete
what wasn't broken. Always prefer targeted edits over sweeping rewrites.
Include: triggers, application rules, examples of minimal vs maximal footprint.

File: .agent/instincts/02-verification-before-confidence.md
Content: The instinct to verify before asserting. Never say "this will work"
without running it. Never claim a file exists without checking. Never describe
an API without reading its documentation. Include specific verification
commands for different scenarios.

File: .agent/instincts/03-user-intent-preservation.md
Content: The instinct to always serve what the user MEANS, not just what they
say. Ask clarifying questions for ambiguous tasks. Never silently reinterpret
a request. Always confirm before destructive operations. State assumptions
explicitly.

File: .agent/instincts/04-graceful-degradation.md
Content: The instinct to keep working even when one part fails. If an MCP
tool fails, fall back to file reading. If a test fails, report it clearly
and propose a fix rather than hiding it. Never silently skip failures.

File: .agent/instincts/05-commercial-quality-standard.md
Content: The instinct that every output should be production-ready.
Code should be ready to deploy. Docs should be ready to publish.
Commits should be ready for code review. Never produce "good enough for now"
output. Standards: error handling, logging, documentation, type safety.

STEP 3 — CREATE INDEX FILE
File: .agent/instincts/README.md
List all instincts with: name, one-line description, priority level,
and when it activates. This is the quick-reference guide.

STEP 4 — REFERENCE IN CLAUDE.md
Add a section to CLAUDE.md titled "Instincts Layer" that instructs the
agent to load all files in .agent/instincts/ during boot sequence,
after loading rules but before loading skills.
```

**Expected outputs:** `.agent/instincts/` directory with 5 instinct files + README.

---

### Phase 2D — Synthesize the dump/ folder

**Prompt to paste into Antigravity:**

```
TASK: The dump/plan/ folder contains suggestions from 5 different AI models
(ChatGPT, Claude, DeepSeek, Gemini, Perplexity). Extract all valuable
intelligence from these and integrate it into the agent.

STEP 1 — READ ALL SUGGESTION FILES
Read every file in dump/plan/:
- ANTIGRAVITY_AGENT_MASTER_PLAN.md
- suggestionbychatgpt.txt
- suggestionbyclaude.txt
- suggestionbydeepseek.txt
- suggestionbygemini.txt
- suggestionbyperplexity.txt

STEP 2 — SYNTHESIZE ACROSS ALL MODELS
For each suggestion file, extract:
- Architectural improvements suggested
- Missing features identified
- Workflow improvements proposed
- Risk or weakness identified
- Unique insight not mentioned by other models

Create a synthesis matrix: which models agreed on what, which had unique insights.

STEP 3 — CREATE INTEGRATION REPORT
Write .agent/SYNTHESIS_REPORT.md documenting:
- Top 10 insights agreed upon by 3+ models
- Top 5 unique insights (one from each model)
- Decisions made: which suggestions were adopted, which were rejected and why
- Remaining suggestions for future versions

STEP 4 — MIGRATE DUMP CONTENTS
Once synthesized, move dump/ contents into a proper archive:
- Create .agent/archive/v3-planning-dump/ 
- Move all dump/plan/ files there
- Update dump/ folder to be empty (or remove it)
- This satisfies Rule 09 (dump-awareness)

STEP 5 — APPLY INSIGHTS
For any suggestion that was adopted, implement it now:
- New rule → add to .agent/rules/
- New skill → add to .agent/skills/  
- New workflow → add to .agent/workflows/
- New instinct → add to .agent/instincts/
- Architectural change → document in MASTER_PLAN.md

Do not leave insights as "notes." Every adopted suggestion must result in
a concrete file change.
```

**Expected outputs:** `.agent/SYNTHESIS_REPORT.md`, `.agent/archive/v3-planning-dump/`, new files from applied insights.

---

### Phase 2E — Workflow integration from reference repos

**Prompt to paste into Antigravity:**

```
TASK: Extract workflow patterns from reference repositories and integrate
the best ones into .agent/workflows/.

STEP 1 — AUDIT WORKFLOW SOURCES
Read these if they exist:
- references/agentic-workflows/ — all workflow definition files
- references/awesome-ai-apps/ — application patterns that imply workflows
- references/langgraph/ — state machine and agent workflow patterns
- references/autogen/ — multi-agent conversation workflow patterns

STEP 2 — IDENTIFY MISSING WORKFLOWS
Our current workflows (01-13) cover: scanner, onboard, scaffold, plan-synthesis,
build-website, build-app, tdd, fix-bugs, performance, write-report,
cross-agent-validator, release, auto-commit.

Missing workflows to add:
A. /14-pr-review — automated pull request review with quality scoring
B. /15-dependency-audit — scan all dependencies for outdated/vulnerable packages
C. /16-api-test — generate and run API tests against any endpoint
D. /17-migrate-database — safe schema migration with rollback plan
E. /18-security-scan — comprehensive OWASP-based security audit
F. /19-documentation-gen — auto-generate docs from code (API, README, CHANGELOG)

STEP 3 — WRITE WORKFLOW FILES
For each missing workflow, create .agent/workflows/[N]-[name].md

FORMAT for each workflow:
---
workflow: [N]-[name]
version: 1.0.0
trigger: /[command-name]
estimated_time: [X minutes]
requires_mcp: [list of MCP servers needed]
---

# Workflow [N]: [Name]

## Purpose
[What problem this workflow solves]

## Trigger Conditions
[When to run this workflow, including automatic triggers]

## Pre-conditions
[What must be true before this workflow can run]

## Execution Steps
### Step 1: [Name]
**Agent:** [which agent or the orchestrator]
**Action:** [exact action to take]
**Tool:** [which MCP tool or built-in capability]
**Output:** [what this step produces]
**Failure handling:** [what to do if this step fails]

[repeat for each step]

## Output Artifacts
[List of files/reports/commits this workflow produces]

## Success Criteria
[How to verify the workflow completed successfully]

## Rollback Procedure
[How to undo this workflow if something went wrong]

STEP 4 — UPDATE WORKFLOW REGISTRY
In .agent/rules/00-workflow-orchestration.md, add entries for workflows 14-19
so the orchestrator knows when to invoke them automatically.
```

**Expected outputs:** 6 new workflow files (14–19), updated workflow orchestration rule.

---

## Phase 3 — Swarm Architecture

**Goal:** Create the multi-agent swarm system. This is what transforms the repo
from a collection of prompts into a true Agentic OS.

---

### Phase 3A — Create the agents/ directory

**Prompt to paste into Antigravity:**

```
TASK: Create .agent/agents/ directory containing all specialist agent definitions
for the Antigravity swarm.

CONTEXT:
The swarm follows a hub-and-spoke model:
- One Orchestrator agent leads every operation
- Specialist agents are summoned by the orchestrator
- Agents communicate via structured JSON handoff blocks
- No agent acts outside its defined domain

STEP 1 — CREATE THE DIRECTORY
mkdir .agent/agents/

STEP 2 — CREATE THE ORCHESTRATOR AGENT
File: .agent/agents/00-orchestrator.md

The orchestrator must:
- Read the user's request and decompose it into sub-tasks
- Determine which specialist agents are needed
- Assign tasks in the correct dependency order
- Monitor progress and handle failures
- Synthesize results into a coherent response
- Never do specialist work itself — always delegate

Include:
- Decision tree for routing to specialists
- Handoff block format (JSON structure for agent-to-agent communication)
- Conflict resolution protocol (when two agents disagree)
- Progress reporting format

STEP 3 — CREATE SPECIALIST AGENTS

File: .agent/agents/01-coder.md
Domain: Writing, editing, and reviewing code
Specializations: Python, TypeScript, Rust, Go, Shell
Constraints: Only writes code. Does not plan, design, or deploy.
Quality gates: Must include types, error handling, and docstrings

File: .agent/agents/02-reviewer.md
Domain: Code review, security audit, quality assessment
Specializations: Bug detection, performance analysis, security scanning
Constraints: Only reviews. Does not write code.
Output format: Structured review report with severity ratings

File: .agent/agents/03-researcher.md
Domain: Information gathering, synthesis, and analysis
Specializations: Web research, documentation reading, API exploration
Tools required: fetch MCP, search MCP
Constraints: Only gathers and reports. Does not write code.
Output format: Structured research brief with citations

File: .agent/agents/04-architect.md
Domain: System design, technical planning, architecture decisions
Specializations: API design, database schema, system topology
Constraints: Only designs. Does not implement.
Output format: Architecture decision records (ADR format)

File: .agent/agents/05-devops.md
Domain: Deployment, infrastructure, CI/CD, monitoring
Specializations: Docker, GitHub Actions, cloud platforms
Tools required: shell MCP, filesystem MCP, git MCP
Constraints: Only manages deployment. Does not write application code.

File: .agent/agents/06-writer.md
Domain: Documentation, README, reports, commit messages
Specializations: Technical writing, changelog generation, API docs
Constraints: Only writes documentation and prose. Does not write code.
Output format: Publication-ready markdown

STEP 4 — HANDOFF PROTOCOL
Create .agent/agents/HANDOFF_PROTOCOL.md defining:

The exact JSON structure agents use to communicate:
{
  "from_agent": "orchestrator",
  "to_agent": "coder",
  "task_id": "unique-id",
  "task_type": "write|review|research|design|deploy|document",
  "priority": "critical|high|medium|low",
  "context": {
    "files_to_read": [],
    "files_to_modify": [],
    "constraints": [],
    "acceptance_criteria": []
  },
  "deadline": "immediate|next-step|end-of-session",
  "on_failure": "retry|escalate|skip|abort"
}

STEP 5 — UPDATE CLAUDE.md
Add a "Swarm Activation" section explaining how to summon the full swarm
vs individual agents, and when each mode is appropriate.
```

**Expected outputs:** `.agent/agents/` with 8 files (6 agents + handoff protocol + README).

---

### Phase 3B — Create the swarm orchestration workflow

**Prompt to paste into Antigravity:**

```
TASK: Create the master swarm orchestration workflow that enables multi-agent
collaboration on complex tasks.

File to create: .agent/workflows/20-swarm-orchestration.md

This workflow is special — it is the meta-workflow that runs OTHER workflows
using multiple agents simultaneously or in sequence.

The file must define:

PART 1: SWARM ACTIVATION PROTOCOL
- Conditions that trigger a full swarm (vs single-agent operation)
- How the orchestrator decomposes a complex request
- How work is parallelized vs serialized
- Maximum concurrency (suggest: 3 agents active at once)

PART 2: EXAMPLE SWARM OPERATIONS

Example A: "Build a production-ready REST API"
- Architect agent: design endpoints and data model
- Coder agent: implement the API
- Reviewer agent: audit the code
- Writer agent: generate API documentation
- DevOps agent: create deployment config
Show the exact handoff sequence and dependencies.

Example B: "Research and implement a new feature"
- Researcher agent: gather information about the feature
- Architect agent: design the implementation approach
- Coder agent: implement
- Reviewer agent: review
Show how research results flow into architectural decisions.

Example C: "Full security audit and remediation"
- Researcher agent: gather threat intelligence
- Reviewer agent: audit the codebase
- Coder agent: implement fixes
- DevOps agent: update security configs
- Writer agent: generate audit report

PART 3: FAILURE HANDLING
- What happens when one agent in a chain fails
- How to recover mid-swarm
- When to abort vs retry vs escalate to user

PART 4: PROGRESS REPORTING FORMAT
Define the standard format for reporting swarm progress to the user:
"[Swarm: 3/5 tasks complete] [Active: Coder] [Next: Reviewer] [ETA: 10min]"

PART 5: SWARM COMPLETION PROTOCOL
- How all agents report results to orchestrator
- How orchestrator synthesizes final output
- Required artifacts at swarm completion
- Session-context.md update requirements
```

**Expected outputs:** `.agent/workflows/20-swarm-orchestration.md`.

---

## Phase 4 — MCP Server Setup

**Goal:** Wire up 6 MCP servers that give the agent real tools to interact
with the filesystem, git, web, memory, shell, and search.

---

### Phase 4A — Create .mcp.json

**Prompt to paste into Antigravity:**

```
TASK: Create the .mcp.json configuration file for the Antigravity Agent.
This file tells Claude Code which MCP servers to connect to.

STEP 1 — RESEARCH
Read the official MCP server documentation by fetching:
https://modelcontextprotocol.io/docs/tools/inspector
https://github.com/modelcontextprotocol/servers

STEP 2 — CREATE .mcp.json
Write the configuration for these 6 MCP servers:

1. filesystem — for reading/writing files safely
   Package: @modelcontextprotocol/server-filesystem
   Config: allow access to current working directory and home directory

2. git — for all version control operations
   Package: @modelcontextprotocol/server-git
   Config: allow operations on current repo

3. fetch — for web requests and API calls
   Package: @modelcontextprotocol/server-fetch
   Config: no restrictions (agent instincts handle safety)

4. memory — for persistent cross-session key-value storage
   Package: @modelcontextprotocol/server-memory
   Config: store memory file at .agent/memory.json

5. sequential-thinking — for complex multi-step reasoning
   Package: @modelcontextprotocol/server-sequential-thinking
   Config: default settings

6. brave-search — for web search (requires BRAVE_API_KEY env variable)
   Package: @modelcontextprotocol/server-brave-search
   Config: read API key from environment

FORMAT for .mcp.json:
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/name", ...additional-args],
      "env": { "ENV_VAR": "value" }
    }
  }
}

STEP 3 — CREATE .agent/mcps/ DIRECTORY
Create documentation for each MCP server:

File: .agent/mcps/README.md
Overview of all 6 MCP servers and when to use each

File: .agent/mcps/01-filesystem.md
- What it does
- Available tools and their parameters
- When to use vs native file operations
- Security considerations

File: .agent/mcps/02-git.md
- Available git operations
- Conventional commit format enforced
- Branch naming conventions
- When to commit vs stage

File: .agent/mcps/03-fetch.md
- How to make API calls
- Handling authentication
- Rate limiting awareness
- Caching strategy

File: .agent/mcps/04-memory.md
- Key naming conventions
- What to store vs what to keep in session-context.md
- Memory expiration strategy
- Format: always store as JSON with timestamp

File: .agent/mcps/05-sequential-thinking.md
- When to activate (complex multi-step problems)
- How to structure thoughts
- Integration with swarm handoffs

File: .agent/mcps/06-brave-search.md
- Query formulation best practices
- Result interpretation
- When to search vs use existing knowledge
- Citation format

STEP 4 — INSTALLATION SCRIPT
Create install-mcps.sh:
#!/bin/bash
# Install all MCP server packages
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-brave-search
echo "All MCP servers installed."
echo "Remember to set BRAVE_API_KEY in your environment."

STEP 5 — UPDATE .gitignore
Add to .gitignore:
.agent/memory.json    (personal memory, not for git)
references/           (reference repos, not for git)
node_modules/
.env
```

**Expected outputs:** `.mcp.json`, `install-mcps.sh`, `.agent/mcps/` with 7 files, updated `.gitignore`.

---

## Phase 5 — Slash Commands

**Goal:** Create `.claude/commands/` directory with every agent as a real,
invocable slash command in Claude Code.

---

### Phase 5 — Prompt to paste into Antigravity

```
TASK: Create the .claude/commands/ directory and populate it with slash
command files for every agent and workflow in the Antigravity system.

BACKGROUND:
Claude Code reads .claude/commands/*.md files and makes them available as
/command-name slash commands. When invoked, the file content is injected
as context. These replace the "described in AGENTS.md" approach with
actual working commands.

STEP 1 — CREATE DIRECTORY
mkdir -p .claude/commands/

STEP 2 — CREATE CORE AGENT COMMANDS

File: .claude/commands/scanner.md
Trigger: /scanner
Purpose: Map the entire repository before any work begins.
Content must instruct the agent to:
- List all directories and files
- Identify the tech stack (languages, frameworks, tools)
- Find entry points, config files, test directories
- Detect anti-patterns (missing tests, no .gitignore, dump folders)
- Read package.json / pyproject.toml / Cargo.toml / go.mod (whichever exists)
- Output a structured SCAN_REPORT.md
- Update session-context.md with findings

File: .claude/commands/planner.md
Trigger: /planner
Purpose: Create a strategic implementation plan for any feature or change.
Content must instruct the agent to:
- Read session-context.md for current project state
- Understand the goal fully before planning
- Break the goal into atomic, testable tasks
- Assign each task to the appropriate specialist agent
- Identify dependencies between tasks
- Estimate complexity (simple/medium/complex) for each task
- Output TASK_PLAN.md with numbered, ordered task list
- Get user confirmation before execution begins

File: .claude/commands/antibug.md
Trigger: /antibug
Purpose: Deep logical audit and bug fixing.
Content must instruct the agent to:
- Read the file(s) or describe the bug first
- Reproduce the bug before attempting to fix
- Identify root cause (not just symptoms)
- Propose fix with explanation
- Write a regression test for the fix
- Apply fix and verify test passes
- Document the bug and fix in session-context.md

File: .claude/commands/tdd-guide.md
Trigger: /tdd-guide
Purpose: Enforce strict TDD Red-Green-Refactor cycle.
Content must instruct the agent to:
- Write failing test FIRST (Red)
- Write minimal code to pass the test (Green)
- Refactor while keeping tests green (Refactor)
- Never write implementation code without a test
- Report test coverage after completion

File: .claude/commands/web-aesthetics.md
Trigger: /web-aesthetics
Purpose: Audit and upgrade UI/UX to premium standards.
Content must instruct the agent to:
- Audit current UI for: layout consistency, color system, typography,
  spacing, accessibility (WCAG AA), responsive design, loading states
- Identify the top 5 visual improvements
- Implement with: glassmorphism or clean flat design, vibrant but accessible
  colors, smooth transitions, proper focus states
- Verify on mobile viewport (375px) and desktop (1440px)
- Run accessibility audit (contrast ratios, ARIA labels)

File: .claude/commands/readme-architect.md
Trigger: /readme-architect
Purpose: Generate professional, complete README.md.
Must include: badges, demo GIF placeholder, features list, quick start,
detailed installation, usage examples, API reference, contributing guide,
license, and contact.

File: .claude/commands/commit-author.md
Trigger: /commit-author
Purpose: Analyze all changes and create atomic, Conventional Commits.
Must: read git diff, group changes by type (feat/fix/chore/docs/test/refactor),
write commit messages with scope and body, never combine unrelated changes.

File: .claude/commands/synthesizer.md
Trigger: /synthesizer
Purpose: Merge multiple plans or approaches into one coherent strategy.
Used when: multiple AI suggestions exist, multiple team proposals exist,
or when resolving conflicting approaches. Output: MASTER_PLAN.md update.

STEP 3 — CREATE WORKFLOW COMMANDS

File: .claude/commands/onboard.md
Trigger: /onboard
Runs: workflow 02-onboard-project.md
Additional context: Runs /scanner first, then health-checks, stack detection,
and creates project metadata.

File: .claude/commands/build-web.md
Trigger: /build-web
Runs: workflow 05a-build-website.md
Additional context: Activates the full swarm for web development.

File: .claude/commands/build-app.md
Trigger: /build-app
Runs: workflow 05b-build-app.md
Additional context: Activates the full swarm for software development.

File: .claude/commands/fix-bugs.md
Trigger: /fix-bugs
Runs: workflow 07-fix-bugs.md
Additional context: Runs antibug on all reported issues.

File: .claude/commands/release.md
Trigger: /release
Runs: workflow 11-release-project.md
Additional context: Full pre-release checklist, versioning, CHANGELOG generation.

File: .claude/commands/auto-commit.md
Trigger: /auto-commit
Runs: workflow 12-auto-commit.md
Additional context: Analyzes all staged changes and commits semantically.

File: .claude/commands/security-scan.md
Trigger: /security-scan
Runs: workflow 18-security-scan.md
Additional context: Activates reviewer agent with security specialization.

File: .claude/commands/swarm.md
Trigger: /swarm
Runs: workflow 20-swarm-orchestration.md
Additional context: Activates the full multi-agent swarm for complex tasks.

STEP 4 — CREATE COMMANDS INDEX
File: .claude/commands/README.md
A quick reference table: command name, trigger, purpose, estimated time.

STEP 5 — VERIFY
List all files created in .claude/commands/ and confirm each file
starts with a clear purpose statement and ends with expected output artifacts.
```

**Expected outputs:** `.claude/commands/` with 18 command files + README.

---

## Phase 6 — Daily Life Workflows

**Goal:** Create personal automation workflows that make Antigravity useful
for everyday tasks, not just coding projects.

---

### Phase 6 — Prompt to paste into Antigravity

```
TASK: Create a .agent/daily-life/ directory with workflows for personal
productivity and day-to-day automation.

CONTEXT:
Beyond coding, this agent should help with: planning the day, research,
writing, email drafting, summarizing documents, and learning new topics.
These workflows should feel personal and frictionless.

STEP 1 — CREATE DIRECTORY
mkdir .agent/daily-life/

STEP 2 — CREATE PERSONAL WORKFLOW FILES

File: .agent/daily-life/01-daily-plan.md
Trigger: /daily-plan or "plan my day"
Purpose: Create a structured daily plan
Process:
- Ask: what are your top 3 priorities today?
- Ask: any meetings or fixed appointments?
- Ask: any blockers from yesterday?
- Generate: time-blocked schedule with focus periods
- Generate: top 3 tasks as atomic, executable steps
- Output: TODAY.md in current directory
Format: Clean markdown with time blocks, priorities, and a "brain dump" section

File: .agent/daily-life/02-research.md
Trigger: /research [topic] or "research [topic] for me"
Purpose: Deep research on any topic with synthesis
Process:
- Use fetch and search MCPs to gather information
- Read at least 5 sources
- Identify: key facts, competing viewpoints, expert consensus, open questions
- Synthesize into: executive summary (3 paragraphs) + detailed breakdown
- Output: RESEARCH_[topic]_[date].md
Include: citations with URLs, confidence levels, areas of uncertainty

File: .agent/daily-life/03-write.md
Trigger: /write [type] or "write a [blog post / essay / email / report]"
Purpose: Professional writing assistance
Process:
- Understand: audience, tone, purpose, length
- Create: outline first, get approval
- Write: full draft in specified format
- Self-review: check for clarity, flow, grammar
- Output: DRAFT_[title]_[date].md
Supported types: blog post, technical article, essay, report, proposal

File: .agent/daily-life/04-summarize.md
Trigger: /summarize or "summarize this [document / article / video transcript]"
Purpose: Distill long content into key insights
Process:
- Read the full content first
- Identify: main thesis, key arguments, supporting evidence, conclusions
- Output: 3-level summary
  Level 1: One sentence (the whole thing in 20 words)
  Level 2: One paragraph (the key insights)
  Level 3: Structured breakdown (headings, bullets)
- Flag: anything important or surprising

File: .agent/daily-life/05-draft-email.md
Trigger: /draft-email or "draft an email to [person] about [topic]"
Purpose: Professional email drafting
Process:
- Understand: relationship to recipient, purpose, desired outcome, tone
- Draft: subject line, body, call to action
- Offer: 2 versions (formal and conversational)
- Review: length (concise), clarity, politeness

File: .agent/daily-life/06-learn.md
Trigger: /learn [topic] or "teach me [topic]"
Purpose: Structured learning on any topic
Process:
- Assess: current knowledge level (beginner/intermediate/advanced)
- Create: learning path with 5-7 progressive concepts
- Teach: each concept with explanation + example + analogy
- Test: ask questions to verify understanding
- Output: LEARNING_[topic].md with notes and resources

File: .agent/daily-life/07-code-review.md
Trigger: /review [file] or "review my code"
Purpose: Personal code review before committing
Process:
- Read the code completely before commenting
- Review for: correctness, readability, performance, security, tests
- Rate: 1-10 with reasoning
- Provide: specific, actionable feedback
- Offer: to fix the top 3 issues

File: .agent/daily-life/08-debug-help.md
Trigger: /debug or "help me debug this"
Purpose: Interactive debugging assistant
Process:
- Read the error message and stack trace
- Ask: what did you expect vs what happened?
- Hypothesize: top 3 possible causes
- Test: each hypothesis systematically
- Never guess — always verify

File: .agent/daily-life/09-note-to-self.md
Trigger: /note [text] or "remember that [text]"
Purpose: Personal note-taking with memory MCP
Process:
- Store note in memory MCP with timestamp and category
- Also append to .agent/personal-notes.md
- Categories: idea, todo, reminder, learning, reference
- Retrieve with: /notes [search-term]

File: .agent/daily-life/10-weekly-review.md
Trigger: /weekly-review or "do my weekly review"
Purpose: End-of-week reflection and planning
Process:
- Read session-context.md for the week's activity
- Read memory MCP for notes from the week
- Generate: what was accomplished, what was left undone, lessons learned
- Plan: top priorities for next week
- Output: WEEKLY_REVIEW_[date].md
- Archive: this week's session-context.md

STEP 3 — CREATE COMMAND ALIASES IN .claude/commands/
For each daily-life workflow, create a corresponding .claude/commands/ file
so they appear as slash commands in Claude Code.

STEP 4 — UPDATE CLAUDE.md
Add a "Personal Productivity Mode" section explaining:
- How to activate daily life workflows
- The difference between project mode and personal mode
- How memory persists across personal sessions
```

**Expected outputs:** `.agent/daily-life/` with 10 workflow files, 10 new `.claude/commands/` files.

---

## Phase 7 — Production Workflows

**Goal:** Complete the production-readiness system with advanced workflows
for deploying, monitoring, and maintaining real applications.

---

### Phase 7 — Prompt to paste into Antigravity

```
TASK: Create advanced production workflows for deploying and maintaining
real applications using the Antigravity Agent swarm.

STEP 1 — CREATE DEPLOYMENT WORKFLOW
File: .agent/workflows/21-deploy-production.md
Trigger: /deploy-production
Process:
1. Pre-deploy checklist:
   - All tests passing?
   - No console.error or TODO in changed files?
   - Environment variables documented?
   - CHANGELOG updated?
   - Version bumped?
2. Build verification:
   - Run build command
   - Check bundle size (warn if >500KB)
   - Run lighthouse/performance audit
3. Deploy steps (framework-agnostic):
   - Detect deploy target (Vercel / Railway / Docker / VPS)
   - Execute deployment
   - Verify deployment health check URL responds
4. Post-deploy:
   - Tag git release
   - Update DEPLOY.md with date and version
   - Notify via session-context.md

STEP 2 — CREATE CODE QUALITY WORKFLOW
File: .agent/workflows/22-quality-gate.md
Trigger: /quality-gate
Process (runs before any PR or merge):
1. Linting — ESLint / Pylint / Clippy (detect tool automatically)
2. Type checking — TypeScript / mypy / Rust compiler
3. Test coverage — must be >80%
4. Security scan — known vulnerabilities in dependencies
5. Documentation — public functions/classes must have docstrings
6. Complexity — flag any function with cyclomatic complexity >10
Output: Quality Gate Report with PASS/FAIL per check

STEP 3 — CREATE FEATURE DEVELOPMENT WORKFLOW
File: .agent/workflows/23-feature-development.md
Trigger: /new-feature [description]
Full pipeline:
1. Researcher agent: gather requirements and research similar implementations
2. Architect agent: design the feature (API contract, data model, component tree)
3. Planner: break into tasks with acceptance criteria
4. TDD: write tests first
5. Coder agent: implement
6. Reviewer agent: code review
7. Web-aesthetics (if UI): visual review
8. Quality gate: automated checks
9. Writer agent: update documentation
10. DevOps agent: update deployment if needed
11. Commit author: semantic commit

STEP 4 — CREATE REFACTOR WORKFLOW
File: .agent/workflows/24-refactor.md
Trigger: /refactor [scope]
Process:
1. Understand the scope (file / module / full codebase)
2. Measure before: test coverage, complexity scores, line count
3. Identify: code smells (duplication, god objects, deep nesting)
4. Prioritize: by impact and risk
5. Refactor incrementally: one concern at a time
6. Run tests after each change
7. Measure after: same metrics
8. Never break public interfaces without documentation

STEP 5 — CREATE MONITORING SETUP WORKFLOW
File: .agent/workflows/25-setup-monitoring.md
Trigger: /setup-monitoring
Process:
1. Detect tech stack
2. Add error tracking (Sentry integration)
3. Add performance monitoring (Web Vitals for frontend)
4. Add structured logging (with log levels)
5. Add health check endpoint /health
6. Add uptime check documentation
7. Generate RUNBOOK.md (how to respond to incidents)

STEP 6 — WRITE RUNBOOK TEMPLATE
File: .agent/templates/RUNBOOK_TEMPLATE.md
Sections: service overview, deployment, common incidents, escalation path,
rollback procedure, contact list.

STEP 7 — WRITE ADR TEMPLATE
File: .agent/templates/ADR_TEMPLATE.md
Architecture Decision Record format:
- Title, Date, Status (proposed/accepted/rejected/deprecated)
- Context, Decision, Consequences
Standard format used by architect agent for all design decisions.
```

**Expected outputs:** 5 new workflow files (21–25), `.agent/templates/` with 2 template files.

---

## Phase 8 — Validation & Packaging

**Goal:** Validate the entire system, fix gaps, version it as v4.0.0,
and package it for distribution.

---

### Phase 8A — Full system validation

**Prompt to paste into Antigravity:**

```
TASK: Perform a complete validation audit of the upgraded Antigravity Agent
repository. This is the final quality gate before v4.0.0 release.

STEP 1 — STRUCTURAL AUDIT
Verify every expected file exists:

ROOT LEVEL:
[ ] CLAUDE.md
[ ] .mcp.json
[ ] .gitignore (with references/, node_modules/, .env)
[ ] README.md
[ ] DEPLOY.md
[ ] LICENSE.md
[ ] install-mcps.sh

.claude/commands/:
[ ] At least 18 command files
[ ] README.md index

.agent/rules/:
[ ] Files 00-19 (original 00-14 + new 15-19)

.agent/skills/:
[ ] Files 01-19 (original 01-12 + new 13-19)

.agent/workflows/:
[ ] Files 01-25 (original 01-13 + new 14-25)

.agent/agents/:
[ ] 00-orchestrator.md
[ ] 01-coder.md through 06-writer.md
[ ] HANDOFF_PROTOCOL.md

.agent/instincts/:
[ ] Files 01-05
[ ] README.md

.agent/mcps/:
[ ] Files 01-06
[ ] README.md

.agent/daily-life/:
[ ] Files 01-10

.agent/templates/:
[ ] RUNBOOK_TEMPLATE.md
[ ] ADR_TEMPLATE.md

.agent/:
[ ] AGENTS.md (updated)
[ ] session-context.md (updated)
[ ] SYNTHESIS_REPORT.md
[ ] archive/v3-planning-dump/

STEP 2 — CONTENT QUALITY AUDIT
For each file, verify:
- Has a clear purpose statement in the first 3 lines
- Has a version/date header
- Uses consistent formatting
- Does not contradict other files in the system
- Is actionable (not just descriptive)

STEP 3 — CROSS-REFERENCE CHECK
- Every agent referenced in CLAUDE.md exists in .agent/agents/
- Every workflow referenced in a command file exists in .agent/workflows/
- Every skill referenced in rules exists in .agent/skills/
- Every MCP server in .mcp.json has documentation in .agent/mcps/

STEP 4 — GENERATE AUDIT REPORT
Write .agent/AUDIT_REPORT_v4.md with:
- Files present: count
- Files missing: list with priority (critical/high/medium)
- Content issues found: list with file and description
- Cross-reference errors: list
- Overall readiness score: X/100

STEP 5 — FIX ALL CRITICAL AND HIGH ISSUES
For every critical or high issue found in Step 4, fix it now.
Rerun the checklist after fixing.

STEP 6 — UPDATE VERSION
In .agent/antigravity-agent-install-state.json, update:
{
  "version": "4.0.0",
  "release_date": "[today's date]",
  "phases_completed": ["foundation", "intelligence", "swarm", "mcp", "commands", "daily-life", "production"],
  "skills_count": 19,
  "rules_count": 20,
  "workflows_count": 25,
  "agents_count": 7,
  "commands_count": 18,
  "instincts_count": 5
}
```

---

### Phase 8B — Final packaging and release

**Prompt to paste into Antigravity:**

```
TASK: Run the /release workflow to package Antigravity Agent v4.0.0.

STEP 1 — Update CHANGELOG.md (create if not exists)
Format: Keep a Changelog (keepachangelog.com)
v4.0.0 entry must list:
- Added: all new files and capabilities
- Changed: all upgraded existing files
- Removed: dump/ folder, old versioning

STEP 2 — Update README.md
Sections required:
- Hero banner (use existing assets/banner.png)
- What is Antigravity Agent (3 sentences)
- Key capabilities (skills, rules, workflows, agents, instincts, MCPs)
- Quick installation (5 steps to get started)
- Slash commands reference table (all /commands)
- Daily life workflows table
- Architecture overview (link to AGENTS.md)
- Contributing guide
- License
Make it look like a premium open-source project README.

STEP 3 — Update DEPLOY.md
Revised installation instructions:
1. Copy .agent/, .claude/, CLAUDE.md, .mcp.json to target repo
2. Run install-mcps.sh
3. Set BRAVE_API_KEY environment variable
4. Open Claude Code in the repo
5. Run /onboard to initialize

STEP 4 — Create the v4.0.0 zip
Create zip/antigravity-agent-v4.0.0.zip containing:
- .agent/
- .claude/
- CLAUDE.md
- .mcp.json
- install-mcps.sh
- README.md
- DEPLOY.md
- LICENSE.md
NOT including: references/, zip/, dump/, assets/, *.md plan files

STEP 5 — Final git commit
Use /auto-commit to stage and commit all changes with:
feat(core): release Antigravity Agent v4.0.0

Complete rewrite with:
- CLAUDE.md master bootstrap
- 7 specialist swarm agents
- 6 MCP server integrations  
- 18 slash commands
- 25 automated workflows
- 10 daily-life personal workflows
- 5 behavioral instincts
- 19 cognitive skills
- 20 governance rules
```

---

## Master File Tree (Target State)

After all 8 phases complete, your repo should look like this:

```
Antigravity Agent/
├── CLAUDE.md                            ← master bootstrap
├── .mcp.json                            ← 6 MCP servers
├── .gitignore                           ← clean
├── install-mcps.sh                      ← one-command setup
├── CHANGELOG.md                         ← version history
├── README.md                            ← premium documentation
├── DEPLOY.md                            ← installation guide
├── LICENSE.md
├── MASTER_PLAN.md
├── PROJECT_METADATA.md
├── MARKET_EVALUATION.md
├── assets/
│   └── banner.png
├── zip/
│   ├── antigravity-agent-v4.0.0.zip    ← distributable
│   └── [older versions...]
├── .claude/
│   └── commands/                        ← 18+ slash commands
│       ├── README.md
│       ├── scanner.md
│       ├── planner.md
│       ├── antibug.md
│       ├── tdd-guide.md
│       ├── web-aesthetics.md
│       ├── readme-architect.md
│       ├── commit-author.md
│       ├── synthesizer.md
│       ├── onboard.md
│       ├── build-web.md
│       ├── build-app.md
│       ├── fix-bugs.md
│       ├── release.md
│       ├── auto-commit.md
│       ├── security-scan.md
│       ├── swarm.md
│       ├── daily-plan.md
│       ├── research.md
│       ├── write.md
│       ├── summarize.md
│       ├── draft-email.md
│       ├── learn.md
│       └── [more...]
└── .agent/
    ├── AGENTS.md                        ← updated registry
    ├── SYNTHESIS_REPORT.md              ← from dump/ content
    ├── AUDIT_REPORT_v4.md              ← validation results
    ├── antigravity-agent-install-state.json
    ├── session-context.md
    ├── memory.json                      ← gitignored
    ├── rules/                           ← 20 rule files (00-19)
    ├── skills/                          ← 19 skill files (01-19)
    ├── workflows/                       ← 25 workflow files (01-25)
    ├── agents/                          ← NEW
    │   ├── 00-orchestrator.md
    │   ├── 01-coder.md
    │   ├── 02-reviewer.md
    │   ├── 03-researcher.md
    │   ├── 04-architect.md
    │   ├── 05-devops.md
    │   ├── 06-writer.md
    │   └── HANDOFF_PROTOCOL.md
    ├── instincts/                       ← NEW
    │   ├── README.md
    │   ├── 01-minimal-footprint.md
    │   ├── 02-verification-before-confidence.md
    │   ├── 03-user-intent-preservation.md
    │   ├── 04-graceful-degradation.md
    │   └── 05-commercial-quality-standard.md
    ├── mcps/                            ← NEW
    │   ├── README.md
    │   ├── 01-filesystem.md
    │   ├── 02-git.md
    │   ├── 03-fetch.md
    │   ├── 04-memory.md
    │   ├── 05-sequential-thinking.md
    │   └── 06-brave-search.md
    ├── daily-life/                      ← NEW
    │   ├── 01-daily-plan.md
    │   ├── 02-research.md
    │   ├── 03-write.md
    │   ├── 04-summarize.md
    │   ├── 05-draft-email.md
    │   ├── 06-learn.md
    │   ├── 07-code-review.md
    │   ├── 08-debug-help.md
    │   ├── 09-note-to-self.md
    │   └── 10-weekly-review.md
    ├── templates/                       ← NEW
    │   ├── RUNBOOK_TEMPLATE.md
    │   └── ADR_TEMPLATE.md
    ├── personal-notes.md               ← gitignored
    └── archive/
        └── v3-planning-dump/           ← moved from dump/
```

---

## Summary Stats (v4.0.0 target)

| Component | v3.0.0 | v4.0.0 |
|---|---|---|
| Rules | 14 | 20 |
| Skills | 12 | 19 |
| Workflows | 13 | 25 |
| Agents | 0 (described) | 7 (real) |
| Instincts | 0 | 5 |
| MCP Servers | 0 | 6 |
| Slash Commands | 0 (real) | 18+ |
| Daily-life Workflows | 0 | 10 |
| Entry point (CLAUDE.md) | ❌ | ✅ |
| Swarm architecture | ❌ | ✅ |
| Cross-session memory | ❌ | ✅ |

---

*This document is the ground truth. When Antigravity asks "what should I build next?" — point it here.*

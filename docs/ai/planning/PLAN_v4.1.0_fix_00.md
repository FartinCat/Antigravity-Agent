# Antigravity Agent — Fix and Enhancement Plan v4.1.0
**Addresses:** Critical bugs + Self-Maintenance + Output Organization + Safe Deletion
**Target version:** 4.1.0
**Execute phases in strict order.**

---

## What This Plan Solves

| Problem | Solution | Phase |
|---|---|---|
| Empty persona files (breaks /ship) | Rewrite all 3 to production standard | Phase 1 |
| AGENTS.md stuck at v3.0.0 | New sync-registry workflow auto-updates it | Phase 2 + 5 |
| install-state.json stuck at v2.2.0 | Same sync-registry workflow | Phase 2 + 5 |
| .mcp.json does not match runtime | New rule + manual sync | Phase 3 |
| Root directory pollution | New output-organization rule + docs/ structure | Phase 3 |
| dump/ folder unsophisticated name | Rename to archived/, update all references | Phase 4 |
| Agent deletes references without warning | New destructive-safety rule + authorization gate | Phase 4 |
| Agent never self-updates its own registry | New sync-registry workflow called by every pipeline | Phase 5 |
| Scanner does not detect stale registries | Update scanner to flag registry drift | Phase 6 |
| Encoding corruption in workflow files | Fix all BOM and em-dash issues | Phase 7 |

---

## PHASE 1 — Rewrite the 3 Specialist Personas (URGENT — /ship is broken until this is done)

PASTE THIS INTO CLAUDE CODE:

```
TASK: Completely rewrite all three specialist persona files in .claude/agents/.
The current files are 6-10 line stubs. They need to be 80-120 lines each with a
full framework, output template, severity system, and composition rules.
Read each existing file first, then replace it entirely.

FILE 1: .claude/agents/code-reviewer.md  (REPLACE ENTIRELY)
---
name: code-reviewer
description: Senior staff engineer performing structured five-axis code review. Use when reviewing any code change before merge, or as part of /ship parallel fan-out.
---

# Persona: Code Reviewer

**Identity:** You are a Staff Engineer with 10+ years of production experience.
You review code to prevent bugs, technical debt, and security issues from reaching production.
You are specific, actionable, and acknowledge good work alongside problems.

**Activation:** Invoked by /review (single pass) or /ship (parallel fan-out).

---

## Review Framework — Five Axes

Evaluate EVERY change across ALL five axes before outputting anything.

### Axis 1: Correctness
- Does the code do what the spec or task description says?
- Are edge cases handled: null, empty, boundary values, concurrent access?
- Are error paths complete — no // TODO: handle error skeletons?
- Do tests verify the actual behavior, not just that the function runs?

### Axis 2: Readability
- Can a new team member understand this without explanation?
- Are names descriptive and consistent with the existing codebase?
- Is control flow straightforward — no deeply nested conditions?
- Are related pieces of code grouped together?

### Axis 3: Architecture
- Does this follow the existing patterns in the codebase?
- If a new pattern is introduced, is it justified?
- Are module boundaries maintained — no circular imports, no god objects?
- Is the abstraction level appropriate?

### Axis 4: Security
- Is all user input validated at system boundaries?
- Are secrets out of code, logs, and version control?
- Is auth checked on every protected operation?
- Are database queries parameterized?
- Do any new dependencies have known CVEs?

### Axis 5: Performance
- Are there N+1 query patterns?
- Are there unbounded loops on user-controlled input?
- Are synchronous operations blocking that should be async?
- Is pagination missing from list endpoints?

---

## Severity Definitions

| Level | Meaning | Action |
|---|---|---|
| Critical | Will cause data loss, security vulnerability, or broken functionality | Must fix before merge |
| Important | Should fix before merge: missing test, wrong abstraction, incomplete error handling | Should fix before merge |
| Suggestion | Consider for improvement: naming, style, optional optimization | At discretion |

---

## Output Template

```
## Code Review
**Verdict:** APPROVE | REQUEST CHANGES
**Overview:** [1-2 sentences on the change and quality]

### Critical Issues
[If none: "None identified."]
- [LOCATION]: [Problem] -> [Specific fix]

### Important Issues
[If none: "None identified."]
- [LOCATION]: [Problem] -> [Specific fix]

### Suggestions
- [LOCATION]: [What to consider]

### What is Done Well
- [At least one genuine positive — always include this]

### Verification Story
- Tests reviewed: [YES / NO]
- Build verified: [YES / NO]
- Security axis: [CLEAN / ISSUES FOUND]
```

## Composition Rules
1. You are invoked by /review or /ship. You do NOT invoke other personas.
2. Read tests FIRST — they reveal intent and coverage.
3. Read the spec or task description before reviewing code.
4. Every Critical or Important finding MUST include a specific fix recommendation.
5. Never approve code with Critical findings.
6. Always include at least one genuine positive.


FILE 2: .claude/agents/security-auditor.md  (REPLACE ENTIRELY)
---
name: security-auditor
description: Security engineer performing OWASP-baseline vulnerability detection. Use for security-focused review or as part of /ship parallel fan-out.
---

# Persona: Security Auditor

**Identity:** You are a Security Engineer specializing in application security.
You focus on practical, exploitable vulnerabilities — not theoretical risks.
You provide proof-of-concept for critical findings so developers understand real impact.

**Activation:** Invoked by /ship (parallel fan-out).

---

## Audit Scope — Five Categories

### Category 1: Input Handling
- All user input validated at system boundaries?
- SQL injection: raw query construction, ORM misuse?
- Command injection: shell calls with user-supplied strings?
- XSS: unescaped user content in HTML output?
- Path traversal: user-supplied file paths without sanitization?

### Category 2: Authentication and Authorization
- Passwords hashed with bcrypt/scrypt/argon2 — never MD5/SHA1?
- Session cookies: httpOnly, secure, sameSite flags set?
- Auth checks on every protected endpoint?
- IDOR vulnerabilities: can User A access User B data?
- Rate limiting on auth endpoints?

### Category 3: Data Protection
- Secrets in environment variables, never in code?
- Sensitive fields excluded from logs?
- Data encrypted in transit and at rest?

### Category 4: Infrastructure
- Security headers: CSP, HSTS, X-Frame-Options present?
- CORS restricted to known origins — not wildcard?
- Dependencies audited for CVEs?
- Error messages generic — no stack traces exposed to users?

### Category 5: Third-Party Integrations
- API keys stored securely, not in client-side code?
- Webhooks verified with HMAC signature validation?
- OAuth using PKCE and state parameter?

---

## Severity Definitions

| Level | Block Release? | Example |
|---|---|---|
| Critical | YES | SQL injection, hardcoded secret, auth bypass |
| High | YES | Missing input validation, IDOR |
| Medium | Fix this sprint | Missing rate limiting, weak CORS |
| Low | Next sprint | Missing security header |
| Info | Best practice | Dependency upgrade available |

---

## Output Template

```
## Security Audit Report

### Summary
Critical: [N] | High: [N] | Medium: [N] | Low: [N] | Info: [N]

### Findings
**[SEVERITY] — [Title]**
Location: [file:line]
Description: [What the vulnerability is]
Impact: [What an attacker could do]
Proof of Concept: [For Critical/High — how to reproduce]
Recommendation: [Exact fix]

### Positive Observations
- [Security practices already in place]
```

## Composition Rules
1. You are invoked by /ship. You do NOT invoke other personas.
2. Focus on EXPLOITABLE vulnerabilities, not theoretical risks.
3. Provide proof-of-concept for Critical and High findings.
4. Never suggest disabling security controls as a fix.
5. Check OWASP Top 10 as minimum baseline on every audit.


FILE 3: .claude/agents/test-engineer.md  (REPLACE ENTIRELY)
---
name: test-engineer
description: QA engineer analyzing test coverage gaps and writing tests for untested behavior. Use for test strategy, coverage analysis, or as part of /ship parallel fan-out.
---

# Persona: Test Engineer

**Identity:** You are an experienced QA Engineer.
Your job is to prove code fails correctly when it should, handles edge cases gracefully,
and does not regress when other code changes around it.

**Activation:** Invoked by /ship (parallel fan-out). Can also be invoked directly.

---

## Test Level Selection Matrix

| Situation | Level |
|---|---|
| Pure function, no I/O | Unit test |
| Crosses a boundary (DB, network, filesystem) | Integration test |
| Critical user-facing workflow | E2E test |
| Performance regression risk | Benchmark test |

Always choose the LOWEST level that captures the behavior.

---

## Coverage Matrix — For Every Changed Function

| Test Case | Description |
|---|---|
| Happy path | Valid input produces expected output |
| Empty/null input | Empty string, empty array, null, undefined, zero |
| Boundary values | Min, max, exactly at limit, one over limit |
| Error paths | Invalid input, upstream failure, timeout |
| Concurrency | Rapid repeated calls, out-of-order async responses |

---

## Bug Proof Pattern
When asked to test a known bug:
1. Write a test that DEMONSTRATES the bug — it must FAIL with current code
2. Confirm it fails and report the failure message
3. State: "Test ready. Will pass once fix is implemented."
4. Do NOT implement the fix — that belongs to the coder.

---

## Output Template

```
## Test Coverage Analysis

### Current State
Tests reviewed: [N tests, which files]
Coverage gaps: [N gaps]

### Recommended Tests
**[Priority] — [Test Name]**
What it verifies: [behavior]
Why it matters: [what bug or regression this prevents]
Test location: [which file]
Sketch:
  it('should [behavior] when [condition]', () => {
    // arrange / act / assert
  });

### Test Quality Assessment
- Test independence: [shared mutable state? YES (problem) / NO (good)]
- Mock placement: [at system boundaries? YES (good) / NO (problem)]
- Test names as specs: [read like specifications? YES / NO]
```

## Composition Rules
1. You are invoked by /ship. You do NOT invoke other personas.
2. Test BEHAVIOR, not implementation details.
3. Each test verifies ONE concept.
4. Tests must be independent — no shared mutable state.
5. Mock at system boundaries, not between internal functions.
6. Every test name should read like a specification.

VERIFICATION: After writing all three files confirm each has:
- YAML frontmatter with name and description
- Identity section
- Structured framework
- Output Template
- Composition Rules stating it does not invoke other personas
- Minimum 60 lines
```


---

## PHASE 2 — Update AGENTS.md and install-state.json

PASTE THIS INTO CLAUDE CODE:

```
TASK: Update the two core registry files to reflect current actual state.

STEP 1: Write a script that counts actual files in each directory:
- .agent/rules/ files
- .agent/skills/ files
- .agent/workflows/ files
- .agent/.agents/skills/ directories
- .agent/instincts/ files
- .claude/commands/ files
- .claude/agents/ files
Print all counts with names.

STEP 2: Update .agent/antigravity-agent-install-state.json:
{
  "version": "4.1.0",
  "release_date": "[today]",
  "installed_rules": [actual filenames from script],
  "installed_foundational_skills": [actual filenames],
  "installed_workflows": [actual filenames],
  "installed_skills": [actual agent directory names],
  "installed_instincts": [actual filenames],
  "installed_commands": [actual command filenames],
  "installed_personas": ["code-reviewer", "security-auditor", "test-engineer"],
  "mcp_servers": ["21st-dev-magic", "StitchMCP", "figma-remote", "mongodb", "playwright", "supabase"],
  "component_counts": {
    "rules": [N],
    "foundational_skills": [N],
    "workflows": [N],
    "agent_personas": [N],
    "instincts": 5,
    "commands": [N],
    "specialist_personas": 3
  },
  "last_updated": "[ISO datetime]",
  "changelog": {
    "4.1.0": "MAJOR: Complete v4.1 upgrade. CLAUDE.md, 3 specialist personas, 5 instincts, 9 new workflows, 9 new skills, 5 new rules, 14 commands, MCP config, sync-registry self-maintenance, output-organization rule, destructive-safety rule, archived/ system.",
    "2.2.0": "Added git-commit-author agent, auto-commit workflow.",
    "2.1.0": "Synchronized versions, applied numeric sequencing."
  }
}

STEP 3: Rewrite .agent/AGENTS.md as version 4.1.0 with ALL components listed:
Header: Antigravity Agent v4.1.0
Sections:
A) SDD Lifecycle Commands: /spec /plan /impl /review /ship
B) Single-Agent Slash Commands: all 19+ agents with numbers
C) Workflow Commands: all 22 workflows
D) Knowledge Engine: /ag-refresh /ag-ask /sync-registry
E) Specialist Personas: code-reviewer, security-auditor, test-engineer
F) Foundational Skills: all skills 01-22
G) Instincts: all 5 with their patterns
H) Accurate architecture tree
```


---

## PHASE 3A — Output Organization: The docs/ System

PASTE THIS INTO CLAUDE CODE:

```
TASK: Create Rule 20 and update all workflows to output to docs/ subdirectories.

PART A: Create .agent/rules/20-output-organization.md

---
rule: 20-output-organization
priority: HIGH
---
# Rule 20: Output Organization — No Root Pollution

## The Law
All agent-generated output documents go into typed subdirectories under docs/,
never the project root.

## Why This Exists
After 10 sessions the project root becomes a junk drawer of MARKET_EVALUATION.md,
SCAN_REPORT.md, MASTER_PLAN.md, and WEEKLY_REVIEW files. The root is for entry
points only: README.md, CLAUDE.md, package.json, LICENSE.md, CHANGELOG.md.

## The docs/ Structure
docs/
├── market-evaluations/   -> MARKET_EVALUATION_{NN}.md
├── master-plans/         -> MASTER_PLAN_{NN}.md
├── scan-reports/         -> SCAN_REPORT_{NN}.md
├── specs/                -> SPEC_{feature-name}_{NN}.md
├── research/             -> RESEARCH_{topic}_{NN}.md
├── audit-reports/        -> AUDIT_REPORT_{NN}.md
├── release-notes/        -> RELEASE_NOTES_v{version}.md
├── weekly-reviews/       -> WEEKLY_REVIEW_{YYYY-MM-DD}.md
└── ai/
    ├── requirements/
    ├── design/
    ├── planning/
    └── implementation/

## Numbering Protocol
Before writing any output file:
1. Check if subdirectory exists. Create it if not.
2. Count existing files matching the pattern.
3. Use next number zero-padded to 2 digits: 00, 01, 02...
4. Never overwrite existing output — always increment.

## Root File Exceptions (ONLY these belong at root)
README.md, CLAUDE.md, DEPLOY.md, LICENSE.md, CHANGELOG.md,
PROJECT_METADATA.md, .mcp.json, all dotfiles,
source entry points: package.json, pyproject.toml, Cargo.toml, go.mod

## Migration of Existing Root Files
When /scanner or /onboard detects root-level output files:
1. Flag as Root Pollution anomaly
2. Offer to move them to docs/ subdirectories
3. Rename with sequence numbers during move

## Enforcement
- /scanner flags root output files as anomaly
- /cross-agent-validator checks workflow outputs landed in docs/

PART B: Update these workflow output paths:
01-scanner.md: -> docs/scan-reports/SCAN_REPORT_{NN}.md
04-multi-plan-synthesis.md: -> docs/master-plans/MASTER_PLAN_{NN}.md
11-release-project.md: market eval -> docs/market-evaluations/MARKET_EVALUATION_{NN}.md
13-spec-discovery.md: -> docs/specs/SPEC_{feature}_{NN}.md
20-parallel-research.md: -> docs/research/RESEARCH_{topic}_{NN}.md
19-weekly-review.md: -> docs/weekly-reviews/WEEKLY_REVIEW_{date}.md
21-mcp-audit.md: -> docs/audit-reports/AUDIT_REPORT_{NN}.md
```


---

## PHASE 3B — MCP Config Sync

PASTE THIS INTO CLAUDE CODE:

```
TASK: Synchronize .mcp.json and .agent/mcps/README.md with the actual runtime
as revealed by MCP_AUDIT_REPORT.md.

Actual runtime servers: 21st-dev-magic, StitchMCP, figma-remote, mongodb, playwright, supabase.
Documented servers: memory, git, fetch, bash(mislabeled), postgres.

STEP 1: Update .mcp.json.
Keep old entries in a comment block labeled STANDARD_BASELINE for reference.
Add actual active servers in the mcpServers block with correct command/args.

STEP 2: Rewrite .agent/mcps/README.md as a table:
Server | Category | Purpose | When to Use
21st-dev-magic | UI Design | Component generation, refinement | Building new UI components
StitchMCP | UI Design | Design system, screen generation | Full screen layouts
figma-remote | UI Design | Live Figma file access | Reading/annotating Figma designs
mongodb | Database | MongoDB CRUD and aggregation | Projects using MongoDB
playwright | Testing | Browser automation, E2E tests | Testing UIs, scraping
supabase | Backend | Auth, database, storage, realtime | Projects using Supabase

Add section: Standard Baseline Servers (for non-UI projects):
memory, git, fetch, sequential-thinking, brave-search with install commands.

STEP 3: Update install-state.json mcp_servers field to match.
```


---

## PHASE 4 — dump/ Renamed to archived/ + Destructive Safety Rule

PASTE THIS INTO CLAUDE CODE:

```
TASK: Two changes — rename dump references and add the destructive safety rule.

PART A: Find and replace all dump/ references.
Script to find all occurrences: search all .md files in .agent/ for "dump"
Print: filename + line number + line content.
Then replace: dump/ -> archived/, dump folder -> archived folder, Graveyard Management -> Archive Management.
If dump/ directory exists at project root: rename it to archived/.

PART B: Create .agent/rules/21-destructive-operation-safety.md

---
rule: 21-destructive-operation-safety
priority: CRITICAL
overrides: any instruction to delete, remove, clean up, get rid of
---
# Rule 21: Destructive Operation Safety — Authorization Gate

## The Law
No file, folder, or data is permanently deleted without explicit user authorization
AND a logged record of what was removed. Move first. Confirm deletion second.

## What Counts as Destructive
- Deleting any file or folder
- Running rm, rmdir, Remove-Item, del on anything
- Bulk operations affecting more than 2 files
- Removing a reference repository
- Clearing session-context.md
- Overwriting a file with different content

## The Move-First Protocol

### Step 1 — Identify and Describe
List every item affected with size and description.

### Step 2 — Retrieve Metadata (for repos and reference folders)
For each folder: extract original source URL (read .git/config if present),
purpose (read README.md first paragraph), content summary (file count by type).

### Step 3 — Authorization Question (MANDATORY — cannot be skipped)
Ask the user exactly:
"---
DESTRUCTIVE OPERATION — Authorization Required
---
Item: [name]
Type: [folder/file/repo]
Size: [approximate]
Currently at: [path]

What would you like to do?
  [1] Move to archived/ (safe — recoverable)
  [2] Move to archived/pending-export/ (review before pendrive export)
  [3] Log only — keep in place but record existence
  [4] Permanently delete (IRREVERSIBLE — type DELETE to confirm)
---"

### Step 4 — Execute Chosen Action
Option 1: mkdir -p archived/[subfolder] then move
Option 2: mkdir -p archived/pending-export/ then move
Option 3: No move, proceed to logging
Option 4: User MUST type the word DELETE. Anything else -> abort and default to Option 1.

### Step 5 — Log to DELETION REGISTRY (always, for all options)
Append to archived/deleted/DELETION_REGISTRY.md:
---
## Entry [NN] — [date]
**Item:** [name]
**Original path:** [full path]
**Action taken:** [Moved to archived/ | pending-export | Logged only | Deleted]
**Source URL:** [git remote URL if applicable]
**Purpose:** [what this was and why it existed]
**Content summary:** [N files, key contents]
**Reason for removal:** [what the user said]
**To recover:** [reclone command or archived/[path]]
---

## Prohibited Behaviors
1. NEVER run rm -rf without the authorization question
2. NEVER delete more than 2 files in one operation without authorization
3. NEVER interpret remove, clean up, get rid of as immediate deletion
4. NEVER skip the DELETION_REGISTRY entry
5. NEVER delete .git/, .agent/, node_modules/, zip/ — always protected

PART C: Create archived/ folder structure.
mkdir -p archived/references
mkdir -p archived/old-versions
mkdir -p archived/deleted
mkdir -p archived/pending-export

Create archived/deleted/DELETION_REGISTRY.md:
# Deletion Registry — Antigravity Agent
This file logs every item deleted, moved, or archived.
Never delete this file.

## Registry
[No entries yet — initialized {today}]
```


---

## PHASE 5 — The Self-Maintenance System

PASTE THIS INTO CLAUDE CODE:

```
TASK: Create skill 22, workflow 22, command, and integrate into all pipelines.

PART A: Create .agent/skills/22-registry-synchronizer.md

# Skill: Registry Synchronizer

## Purpose
Maintain perfect synchronization between the live .agent/ filesystem and the
four registry documents that describe it.

## The Linked-File Map

TRIGGER                              -> AFFECTED REGISTRIES
New file in .agent/rules/            -> AGENTS.md rules section, install-state.json installed_rules
New file in .agent/skills/           -> AGENTS.md skills section, install-state.json installed_foundational_skills
New file in .agent/workflows/        -> AGENTS.md workflows section, install-state.json installed_workflows
New dir in .agent/.agents/skills/    -> AGENTS.md agents section, install-state.json installed_skills
New file in .agent/instincts/        -> AGENTS.md instincts section, install-state.json installed_instincts
New file in .claude/commands/        -> AGENTS.md commands section, CLAUDE.md command registry
New file in .claude/agents/          -> AGENTS.md personas section, /ship command description
Server added to .mcp.json            -> .agent/mcps/README.md, install-state.json mcp_servers
Version bump in PROJECT_METADATA.md  -> install-state.json version, CLAUDE.md identity block

## Drift Detection (script-based — never reads files raw)
Write a shell or Python script that:
1. Counts actual files in each .agent/ directory
2. Reads expected counts from install-state.json component_counts
3. Compares them
4. Outputs: DRIFT DETECTED or IN SYNC for each component type
5. If drift: lists the specific files that are new or missing

## Sync Protocol
When drift is detected:
1. AGENTS.md: regenerate affected sections from actual filesystem
2. install-state.json: update affected lists and component_counts, update last_updated
3. CLAUDE.md: update only if commands or personas changed
4. Never change version field during sync — version bumps are intentional

## Quality Gate
Before declaring sync complete:
- Component counts in install-state.json match actual filesystem
- AGENTS.md sections list all actual files
- No file exists in .agent/ undocumented in AGENTS.md
- No file listed in AGENTS.md that does not exist in .agent/


PART B: Create .agent/workflows/22-sync-registry.md

---
description: "Step 22 — Synchronize all registry files with the actual .agent/ filesystem state."
order: 22
---
# Workflow: Sync Registry

**Objective:** Keep AGENTS.md, install-state.json, and CLAUDE.md perfectly
synchronized with the actual .agent/ filesystem.

## Trigger Conditions
- Automatically as LAST STEP of any workflow that creates new .agent/ files
- Manually via /sync-registry
- Automatically when scanner detects drift
- Automatically before /release-project packaging step

## Execution Sequence

### Step 1 — Drift Detection (script-based)
Run script comparing filesystem vs install-state.json:
Output: [component]: [disk count] actual / [registry count] registered -> [IN SYNC / DRIFT]
Print full drift report before any changes.

### Step 2 — AGENTS.md Regeneration (only if drift detected)
For each drifted component:
1. Read actual files in the directory
2. Extract name and description from each file's first 3 lines
3. Regenerate the affected AGENTS.md section
4. Preserve all other sections — surgical update only
5. Update version number at top

### Step 3 — install-state.json Update
Update drifted lists with actual filenames.
Update component_counts with accurate numbers.
Update last_updated timestamp.
DO NOT change the version field.

### Step 4 — CLAUDE.md Command Registry Sync (only if commands or personas changed)
Read all command files, extract description from YAML frontmatter.
Regenerate Section 4 (Slash Command Registry) of CLAUDE.md.
Preserve all other sections.

### Step 5 — Verification
Re-run drift detection script.
Expected: ALL components show IN SYNC.
If any still show drift: repeat Steps 2-4.

### Step 6 — Sync Report
Output:
"REGISTRY SYNC COMPLETE — [date]
Components synced: [list]
AGENTS.md: UPDATED / UNCHANGED
install-state.json: UPDATED / UNCHANGED
CLAUDE.md: UPDATED / UNCHANGED
Drift resolved: [N] components"


PART C: Create .claude/commands/sync-registry.md

---
description: Synchronize AGENTS.md and install-state.json with actual filesystem state
---
Run workflow 22-sync-registry.md.
Detect drift between .agent/ filesystem and all registry documents.
Update AGENTS.md, install-state.json, and CLAUDE.md if needed.
Always run after adding new skills, workflows, rules, agents, or commands.


PART D: Add /sync-registry as final step to these workflows:
In 11-release-project.md: add Step 10 — Registry Sync before packaging.
In 16-feature-development.md: add as final step after /auto-commit.
In 10-cross-agent-validator.md: add registry drift check to Step 3 artifact verification.
If drift > 5 components: flag as YELLOW health.
```


---

## PHASE 6 — Scanner Upgrades

PASTE THIS INTO CLAUDE CODE:

```
TASK: Add two new detection capabilities to .agent/workflows/01-scanner.md.

READ 01-scanner.md first. Then add after Step 6 Anomaly Detection:

### Step 6b — Registry Drift Detection
Run a script (not raw file reads) that checks:
- Count .agent/rules/*.md vs install-state.json installed_rules count
- Count .agent/skills/*.md vs installed_foundational_skills count
- Count .agent/workflows/*.md vs installed_workflows count
- Count .agent/.agents/skills/ directories vs installed_skills count
- Compare install-state.json version with AGENTS.md header version

Report:
  REGISTRY STATUS: IN SYNC / DRIFT DETECTED
  If drift: "[component]: [N] on disk, [M] in registry — run /sync-registry"
  If version mismatch: "VERSION MISMATCH — run /sync-registry"

### Step 6c — Root Pollution Detection
Check project root for output files that belong in docs/:
Patterns to flag: *EVALUATION*.md, *MASTER_PLAN*.md, *SCAN_REPORT*.md,
*RESEARCH_*.md, *AUDIT_REPORT*.md, WEEKLY_REVIEW_*.md
Exclude: README.md, CLAUDE.md, DEPLOY.md, LICENSE.md, CHANGELOG.md, PROJECT_METADATA.md

Report:
  ROOT POLLUTION: CLEAN / [N] files found
  If found: list them and ask "Run /migrate-docs to move to docs/?"

UPDATE the Output Format section — add two new fields:
  Registry Status: [IN SYNC / DRIFT DETECTED — details]
  Root Pollution: [CLEAN / N output files at root]

UPDATE Recommended Next Step logic:
  If registry drift AND root pollution -> "Run /sync-registry then move files to docs/"
  If only registry drift -> "Run /sync-registry"
  If only root pollution -> "Move files to docs/ or run /migrate-docs"
```


---

## PHASE 7 — Encoding Fixes + CHANGELOG

PASTE THIS INTO CLAUDE CODE:

```
TASK: Fix encoding issues, remove stale content, create CHANGELOG.md.

STEP 1: Detect BOM markers in workflow files using PowerShell:
Get-ChildItem ".agent\workflows\*.md" | ForEach-Object {
  $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
  if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "BOM: $($_.Name)"
  }
}

STEP 2: For each BOM-affected file: strip the BOM, rewrite as UTF-8 without BOM.

STEP 3: Fix em-dash corruption across all workflow files.
Replace in all .agent/workflows/*.md files:
  "â€"" -> "—"
  "â€™" -> "'"

STEP 4: Clean skill 13 content.
In .agent/skills/13-knowledge-capture.md:
Remove the "Advanced Operations Matrix" section at the bottom entirely.
It contains Python database/numpy content unrelated to knowledge capture.
Delete everything after the "## Next Steps" heading.

STEP 5: Resolve Agent 21 numbering violation.
Rule 00 says agents must be numbered 01-19. Agent 21 (mcp-auditor) breaks this.
Ask the user:
"Agent 21 (mcp-auditor) breaks the 01-19 numbering convention in Rule 00.
Options:
  [A] Renumber mcp-auditor as agent 20 — update AGENTS.md, install-state.json, workflow 21 references
  [B] Expand Rule 00 to allow an Infrastructure Agents space (21+) and document the exception
Which do you prefer?"
Wait for the user's answer before making changes.

STEP 6: Create CHANGELOG.md at repo root.

# Changelog — Antigravity Agent

All notable changes documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [4.1.0] — [today's date]
### Added
- CLAUDE.md master bootstrap
- 3 production specialist personas (code-reviewer, security-auditor, test-engineer)
- 5 behavioral instincts in .agent/instincts/
- 9 new foundational skills (13-21)
- 9 new workflows (13-21)
- 5 new governance rules (15-19)
- 14 real slash commands in .claude/commands/
- .mcp.json MCP server configuration
- Rule 20: Output organization (docs/ folder system with sequence numbering)
- Rule 21: Destructive operation safety and authorization gate
- Skill 22: Registry synchronizer
- Workflow 22: Sync-registry (self-maintenance automation)
- archived/ folder replacing dump/ with deletion registry
- CHANGELOG.md (this file)
### Changed
- AGENTS.md updated to v4.1.0 with complete component registry
- install-state.json updated to v4.1.0
- dump/ renamed to archived/ throughout all system files
- Scanner upgraded with drift detection and root pollution detection
- All workflow files: encoding fixed
- 01-scanner.md: registry drift and root pollution detection added
- 10-cross-agent-validator.md: registry sync check added
### Fixed
- Encoding corruption in workflow files
- Rogue Advanced Operations Matrix removed from skill 13
- Specialist personas rewritten from stubs to production-grade frameworks
```

---

## Result: What the Agent Does On Its Own After v4.1.0

The self-maintenance chain that runs automatically:

1. You create a new workflow file
2. The pipeline calls /sync-registry as its final step
3. 22-sync-registry detects the new file via drift detection script
4. AGENTS.md updated — new workflow listed correctly
5. install-state.json updated — component count accurate
6. CLAUDE.md command registry updated if it was a command
7. Next session: /scanner reports IN SYNC
8. You never need to manually update any registry again

The safety chain for destructive operations:

1. You say "remove the references folder" or "delete X"
2. Rule 21 fires — authorization gate activates
3. Agent extracts metadata: source URL, purpose, content summary
4. Agent asks: Move to archived/ / pending-export / log only / DELETE?
5. Whatever you choose: logged permanently in DELETION_REGISTRY.md
6. The word DELETE must be typed explicitly for permanent deletion
7. Never again will a single ambiguous command destroy an entire folder

The output organization chain:

1. You run /market-evaluator
2. Rule 20 fires — agent checks docs/market-evaluations/ for existing files
3. Finds MARKET_EVALUATION_00.md already exists
4. Creates MARKET_EVALUATION_01.md
5. Root stays clean
6. All evaluations in one place, sequentially numbered

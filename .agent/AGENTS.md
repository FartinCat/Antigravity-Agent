# Antigravity Agent Ecosystem (v4.7.0)

A portable AI operating system. Copy the `.agent/` folder into any project directory and the entire skill + workflow ecosystem activates immediately.

---

## 🔧 Slash Commands (Single Agents)

| # | Command | Agent | Phase | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **`/deep-scan`** | 01-deep-scan | P3 | Comprehensive situational awareness agent. Maps... |
| **02** | **`/failure-predictor`** | 02-failure-predictor | P3 | Pre-execution failure prediction agent. Runs be... |
| **03** | **`/ask`** | 03-ask | P3 | Quick, precise answers to doubts with medium co... |
| **04** | **`/planner`** | 04-planner | P3 | Strategic breakdown of complex requirements int... |
| **05** | **`/synthesizer`** | 05-synthesizer | P3 | Ensemble Plan Evaluation and Master Synthesis a... |
| **06** | **`/tdd-guide`** | 06-tdd-guide | P3 | Strict Test-Driven Development agent. Enforces ... |
| **07** | **`/python-agent`** | 07-python-agent | P3 | Python-specific language agent. Encodes Python ... |
| **08** | **`/rust-agent`** | 08-rust-agent | P3 | Rust-specific language agent. Encodes Rust rule... |
| **09** | **`/jsts-agent`** | 09-jsts-agent | P3 | JavaScript/TypeScript-specific language agent. ... |
| **10** | **`/c-agent`** | 10-c-agent | P3 | C-specific language agent. Encodes C rules, ins... |
| **11** | **`/go-agent`** | 11-go-agent | P3 | Go-specific language agent. Encodes Go rules, i... |
| **12** | **`/antibug`** | 12-antibug | P3 | Advanced bug detection agent. Works in tandem w... |
| **13** | **`/web-aesthetics`** | 13-web-aesthetics | P3 | Ensures any generated vanilla CSS/JS web app fe... |
| **14** | **`/scientific-writing`** | 14-scientific-writing | P3 | Specialized rules for writing physics dissertat... |
| **15** | **`/latex-bib-manager`** | 15-latex-bib-manager | P3 | Automatically manages LaTeX bibliographies, enf... |
| **16** | **`/readme-architect`** | 16-readme-architect | P3 | Generates a highly structured, comprehensive, a... |
| **17** | **`/market-evaluator`** | 17-market-evaluator | P3 | Evaluates the codebase and features against use... |
| **18** | **`/commercial-license`** | 18-commercial-license | P3 | Generates a custom LICENSE.md enforcing commerc... |
| **19** | **`/git-commit-author`** | 19-git-commit-author | P3 | Analyzes git diff output and generates atomic, ... |
| **20** | **`/code-reviewer`** | 20-code-reviewer | P3 | Senior code reviewer that evaluates changes acr... |
| **21** | **`/security-auditor`** | 21-security-auditor | P3 | Security engineer focused on vulnerability dete... |
| **22** | **`/test-engineer`** | 22-test-engineer | P3 | QA engineer specialized in test strategy, test ... |
| **23** | **`/mcp-auditor`** | 23-mcp-auditor | P3 | **Role**: Infrastructure Discovery & Capability... |

---

## ⚡ Workflows (+ Button — In Sequence)

Workflows are listed below in **logical ascending order** corresponding to a standard software lifecycle.

- **`01-scanner.md`**: Build situational awareness and map directories.
- **`02-onboard-project.md`**: Analyze legacy code and suggest initial strategy.
- **`03-mcp-audit.md`**: Audit & map integrated MCP tool capabilities.
- **`04-scaffold-assets.md`**: Initialize project structure and taxonomy.
- **`05-spec-discovery.md`**: Functional and technical spec extraction.
- **`06-parallel-research.md`**: **Objective**: Execute simultaneous research across multiple technical paths, then synthesize findings into a unified comparison matrix. Use when evaluating competing technologies, frameworks, libraries, or architectural patterns.
- **`07-multi-plan-synthesis.md`**: Merge competing AI strategies into one plan.
- **`08-knowledge-capture.md`**: Distill project insights into persistent KIs.
- **`09-new-requirement.md`**: Integrate new features into an existing plan.
- **`10-feature-development.md`**: **Objective**: Incrementally build a single feature from specification through implementation to verification. This is the inner loop of development — one feature at a time, fully tested before moving to the next.
- **`11-build-website.md`**: **Objective**: End-to-end pipeline for building a production-quality website or web application from specification to deployment-ready state. Enforces premium aesthetics, SEO best practices, and responsive design.
- **`12-build-app.md`**: **Objective**: End-to-end pipeline for building a production-ready software application from specification through implementation to deployment readiness. Enforces architectural discipline, test coverage, and clean code practices.
- **`13-tdd.md`**: Disciplined Red-Green-Refactor orchestration.
- **`14-debug-session.md`**: Intensive diagnostic and repair protocol.
- **`15-fix-bugs.md`**: Build-detected bug hunting and resolution.
- **`16-performance.md`**: Profiling and bottleneck elimination.
- **`17-quality-gate.md`**: Compliance check against design/requirements.
- **`18-cross-agent-validator.md`**: Audit previous steps for hallucinations/errors.
- **`19-write-report.md`**: **Objective**: Generate a structured technical or academic report with proper formatting, citations, logical flow, and professional typography. Use for status reports, technical summaries, research writeups, post-mortems, and documentation deliverables.
- **`20-weekly-review.md`**: **Objective**: Conduct a structured strategic audit of project health, progress, and trajectory. This is the retrospective heartbeat — run weekly to catch drift, celebrate wins, and course-correct before problems compound.
- **`21-release-project.md`**: God Mode: License, README, Packaging.
- **`22-readme-architect.md`**: Dynamically updates the README.md to accurately reflect all active agents, workflows, and skills.
- **`23-sync-registry.md`**: Synchronize all registry files with the actual .agent/ filesystem state.
- **`24-auto-commit.md`**: Atomic, semantic commit generation loop.

---

## Architecture

```
.agent/
├── instincts/ (Probabilistic Behaviors)
│   ├── 01-minimal-footprint.md
│   ├── 02-verification-before-confidence.md
│   ├── 03-user-intent-preservation.md
│   ├── 04-graceful-degradation.md
│   ├── 05-commercial-quality-standard.md
├── rules/ (Governance)
│   ├── 00-workflow-orchestration.md
│   ├── 01-core.md
│   ├── 02-integrity.md
│   ├── ... (23 rules total)
├── skills/ (Foundational Logic)
│   ├── 01-research-loop.md
│   ├── 02-language-routing.md
│   ├── 03-task-decomposition.md
│   ├── ... (22 skills total)
└── workflows/ (Pipelines)
    ├── 01-scanner.md
    ├── 02-onboard-project.md
    ├── 03-mcp-audit.md
    ├── 04-scaffold-assets.md
    ├── 05-spec-discovery.md
    ├── 06-parallel-research.md
    ├── 07-multi-plan-synthesis.md
    ├── 08-knowledge-capture.md
    ├── 09-new-requirement.md
    ├── 10-feature-development.md
    ├── 11-build-website.md
    ├── 12-build-app.md
    ├── 13-tdd.md
    ├── 14-debug-session.md
    ├── 15-fix-bugs.md
    ├── 16-performance.md
    ├── 17-quality-gate.md
    ├── 18-cross-agent-validator.md
    ├── 19-write-report.md
    ├── 20-weekly-review.md
    ├── 21-release-project.md
    ├── 22-readme-architect.md
    ├── 23-sync-registry.md
    ├── 24-auto-commit.md
```

# Antigravity Agent — v3.0.0

A portable AI operating system. Copy the `.agent/` folder into any project directory and the entire skill + workflow ecosystem activates immediately.

---

## 🔧 Slash Commands (Single Agents)

| # | Command | Agent | Phase | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **`/scanner`** | 01-deep-scan | P1 | Project-aware repo mapping. |
| **02** | **`/failure-predictor`** | 02-failure-predictor | P1 | Pre-execution risk analysis. |
| **03** | **`/ask`** | 03-ask | P1 | Precision query agent. |
| **04** | **`/planner`** | 04-planner | P2 | Strategic breakdown and roadmap. |
| **05** | **`/synthesizer`** | 05-synthesizer | P2 | Merge multiple AI plans. |
| **06** | **`/tdd-guide`** | 06-tdd-guide | P3 | Strict Red-Green-Refactor development. |
| **07** | **`/python`** | 07-python-agent | P3 | Python specialist. |
| **08** | **`/rust`** | 08-rust-agent | P3 | Rust specialist. |
| **09** | **`/jsts`** | 09-jsts-agent | P3 | JS/TS specialist. |
| **10** | **`/c-lang`** | 10-c-agent | P3 | C specialist. |
| **11** | **`/go`** | 11-go-agent | P3 | Go specialist. |
| **12** | **`/antibug`** | 12-antibug | P4 | Deep logic auditing. |
| **13** | **`/web-aesthetics`** | 13-web-aesthetics | P4 | Premium UI enforcement. |
| **14** | **`/scientific-writing`** | 14-scientific-writing | P4 | Academic tone and LaTeX. |
| **15** | **`/latex-bib-manager`** | 15-latex-bib-manager | P4 | Citation sequencing. |
| **16** | **`/readme-architect`** | 16-readme-architect | P5 | Premium README generation. |
| **17** | **`/market-evaluator`** | 17-market-evaluator | P5 | Codebase market value assessment. |
| **18** | **`/commercial-license`** | 18-commercial-license | P5 | Commercial license generation. |
| **19** | **`/commit-author`** | 19-git-commit-author | P5 | Atomic Conventional Commits. |

---

## ⚡ Workflows (+ Button — In Sequence)

| # | Workflow | Purpose | Key Agents |
| :-- | :--- | :--- | :--- |
| **01** | `/scanner` | Map the project. Run first. | `01-deep-scan` |
| **02** | `/onboard-project` | First-contact project analysis. | `01-deep-scan` → Specialists |
| **03** | `/scaffold-assets` | Initialize assets and metadata. | — |
| **04** | `/multi-plan-synthesis` | Merge plans into MASTER_PLAN.md. | `05-synthesizer` |
| **05a** | `/build-website` | End-to-end web app pipeline. | `04-planner` → `13-web-aesthetics` |
| **05b** | `/build-app` | End-to-end software app pipeline. | `04-planner` → `06-tdd-guide` |
| **06** | `/tdd` | Focused TDD cycle. | `06-tdd-guide` → `12-antibug` |
| **07** | `/fix-bugs` | Full bug hunting and patching. | `12-antibug` → `06-tdd-guide` |
| **08** | `/performance` | Measure → optimize → verify. | Specialists → `06-tdd-guide` |
| **09** | `/write-report` | Academic/technical report pipeline. | `14-scientific-writing` |
| **10** | `/cross-agent-validator` | Self-audit: verify all agents. | — |
| **11** | `/release-project` | Cleanup → license → README. | `17-market-evaluator` → `16-readme-architect` |
| **12** | `/auto-commit` | Generate git commit commands. | `19-git-commit-author` |

---

## Architecture

```
.agent/
├── rules/ (Governance & Instincts)
│   ├── 00-workflow-orchestration.md
│   ├── 01-core.md
│   ├── 02-integrity.md
│   ├── 03-instincts.md
│   ├── 04-verification-gates.md
│   ├── 05-context-integrity.md
│   ├── 06-context-memory.md
│   ├── 07-metadata-awareness.md
│   ├── 08-asset-awareness.md
│   ├── 09-dump-awareness.md
│   ├── 10-semantic-versioning.md
│   ├── 11-git-awareness.md
│   ├── 12-silent-ingest.md
│   ├── 13-self-improvement.md
│   └── 14-release-packaging.md
├── skills/ (Foundational Logic)
│   ├── 01-research-loop.md
│   ├── 02-language-routing.md
│   ├── 03-task-decomposition.md
│   ├── 04-architectural-design.md
│   ├── 05-code-synthesis.md
│   ├── 06-refactor.md
│   ├── 07-cognitive-load-inspector.md
│   ├── 08-side-effect-tracker.md
│   ├── 09-state-machine-inspector.md
│   ├── 10-confidence-scoring.md
│   ├── 11-memory-evolution.md
│   └── 12-commit-semantics.md
├── .agents/skills/ (UI Agents)
│   ├── 01-deep-scan/
│   ├── 02-failure-predictor/
│   ├── 03-ask/
│   ├── 04-planner/
│   ├── 05-synthesizer/
│   ├── 06-tdd-guide/
│   ├── 07-python-agent/
│   ├── 08-rust-agent/
│   ├── 09-jsts-agent/
│   ├── 10-c-agent/
│   ├── 11-go-agent/
│   ├── 12-antibug/
│   ├── 13-web-aesthetics/
│   ├── 14-scientific-writing/
│   ├── 15-latex-bib-manager/
│   ├── 16-readme-architect/
│   ├── 17-market-evaluator/
│   ├── 18-commercial-license/
│   └── 19-git-commit-author/
└── workflows/ (Pipelines)
    ├── 01-scanner.md
    ├── 02-onboard-project.md
    ├── 03-scaffold-assets.md
    ├── 04-multi-plan-synthesis.md
    ├── 05a-build-website.md
    ├── 05b-build-app.md
    ├── 06-tdd.md
    ├── 07-fix-bugs.md
    ├── 08-performance.md
    ├── 09-write-report.md
    ├── 10-cross-agent-validator.md
    ├── 11-release-project.md
    └── 12-auto-commit.md
```

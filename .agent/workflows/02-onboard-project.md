---
title: "ONBOARD PROJECT"
description: "Workflow 2 - ONBOARD PROJECT"
order: 2
---

# Workflow: Onboard New Project

**Trigger**: First contact with any repository not yet registered in project memory.

## Purpose
Automated first-contact protocol that builds complete project awareness before any code changes.

---

## Step 1: Language Detection
- Scan file extensions, build files, shebangs
- Apply `02-language-routing.md` to identify primary and secondary languages
- Output: Language inventory with confidence scores

## Step 2: Project Type Inference
Based on detected patterns:

| Signals | Inferred Type |
|---|---|
| `package.json` + `src/App.*` | Web Application (SPA) |
| `Cargo.toml` + `src/main.rs` | Rust Binary |
| `Cargo.toml` + `src/lib.rs` | Rust Library |
| `pyproject.toml` + `src/` | Python Package |
| `Dockerfile` + `docker-compose.yml` | Containerized Service |
| `go.mod` + `cmd/` | Go CLI/Service |
| `.agent/` | Antigravity Agent Ecosystem |
| `Makefile` + `*.c` | C Project |

## Step 3: Architecture Mapping
- Identify entry points (main files, index files, route definitions)
- Map the dependency graph (imports, requires, use statements)
- Identify configuration files and their roles
- Detect test infrastructure and coverage

## Step 4: Inspector Dry-Run
- Run all applicable micro-inspectors in **read-only mode**
- Collect warnings without applying fixes
- Generate a health report

## Step 5: Project Memory Initialization
Create or update `.agent/session-context.md` with:
- Detected languages and versions
- Project type and architecture pattern
- Key file locations (entry points, configs, tests)
- Health report summary from inspector dry-run
- Known quirks or anomalies

## Output
```markdown
## Project Onboarding Report
- **Repository**: [name]
- **Languages**: [list with versions]
- **Type**: [inferred project type]
- **Architecture**: [pattern name]
- **Entry Points**: [list]
- **Health Score**: [green/yellow/red]
- **Inspector Warnings**: [count by category]
- **Recommended First Actions**: [list]
```

# Antigravity Agent — Slash Commands

All files in `.claude/commands/` are real slash commands auto-discovered by Claude Code.
Type `/command-name` in the chat to invoke any command.

## Command Registry

| Command | Trigger | Purpose | Phase |
|---|---|---|---|
| `/spec` | `/spec` | Write structured specification before coding | SDD Lifecycle |
| `/plan` | `/plan` | Break work into verifiable tasks with acceptance criteria | SDD Lifecycle |
| `/impl` | `/impl` | Implement next task: RED → GREEN → commit | SDD Lifecycle |
| `/review` | `/review` | Five-axis code review (single pass) | SDD Lifecycle |
| `/ship` | `/ship` | Parallel fan-out: 3 specialists → GO/NO-GO | SDD Lifecycle |
| `/scanner` | `/scanner` | Map entire repository before work begins | Discovery |
| `/planner` | `/planner` | Strategic implementation planning | Strategy |
| `/antibug` | `/antibug` | Root-cause debugging with regression tests | Quality |
| `/tdd-guide` | `/tdd-guide` | Enforce strict TDD Red-Green-Refactor | Quality |
| `/auto-commit` | `/auto-commit` | Atomic Conventional Commits from staged changes | Finalization |
| `/onboard` | `/onboard` | First-contact analysis for new projects | Discovery |
| `/web-aesthetics` | `/web-aesthetics` | Audit and upgrade UI/UX to premium standards | Quality |
| `/ag-refresh` | `/ag-refresh` | Rebuild project knowledge index | Knowledge |
| `/ag-ask` | `/ag-ask [question]` | Query project codebase via knowledge hub | Knowledge |

## Execution Order (Recommended)

The SDD lifecycle is the recommended flow for any non-trivial work:

```
/spec → /plan → /impl → /review → /ship → /auto-commit
```

For new projects:
```
/scanner → /onboard → /spec → /plan → /impl → /ship
```

For bug fixes:
```
/antibug → /tdd-guide → /auto-commit
```

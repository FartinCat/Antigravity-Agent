---
title: "FIX BUGS"
description: "Workflow 7 - FIX BUGS"
order: 7
---

# Workflow: Fix Bugs

**Objective**: Automatically track down and resolve syntax errors, logic flaws, memory leaks, and historical regressions.

## Execution Sequence

1. **Context Read**: Read `.agent/session-context.md` for any notes from previous sessions about known issues.

2. **Scan**: Invoke `/scanner` to map the current project structure. The scanner EXCLUDES `.agent/` â€” the diagnostic focuses only on project code.

3. **Build System Detection**: Identify the project's build tool and run the build:

   | Indicator | Build Command |
   |-----------|---------------|
   | `package.json` with `build` script | `npm run build` or `pnpm build` |
   | `tsconfig.json` (TypeScript only) | `npx tsc --noEmit` |
   | `Cargo.toml` | `cargo build 2>&1` |
   | `pyproject.toml` | `python -m compileall -q .` or `mypy .` |
   | `go.mod` | `go build ./...` |
   | `Makefile` + `*.c` | `make` |

4. **Hunt**: Pass the scanner output to `/antibug`. The antibug agent MUST:
   - Execute Phase 0 (Historical Pattern Analysis from `dump/` â€” NOT from `.agent/`).
   - Run Phases 1â€“4 on project source files only.
   - Never flag `.agent/` files as bugs in the project.

5. **Fix Loop** (One Error at a Time):
   - **Read the file** â€” See error context (10 lines around the error).
   - **Diagnose** â€” Identify root cause (missing import, wrong type, syntax error).
   - **Fix minimally** â€” Apply the smallest change that resolves the error.
   - **Re-run build** â€” Verify the error is gone and no new errors introduced.
   - **Move to next** â€” Continue with remaining errors.

6. **Guardrails** â€” Stop and ask the user if:
   - A fix introduces **more errors than it resolves**.
   - The **same error persists after 3 attempts** (likely a deeper architectural issue).
   - The fix requires **architectural changes** (not just a bug fix).
   - Build errors stem from **missing dependencies** (need `npm install`, `cargo add`, etc.).

7. **Recovery Strategies**:

   | Situation | Action |
   |-----------|--------|
   | Missing module/import | Check if package is installed; suggest install command |
   | Type mismatch | Read both type definitions; fix the narrower type |
   | Circular dependency | Identify cycle with import graph; suggest extraction |
   | Version conflict | Check manifest for version constraints |
   | Build tool misconfiguration | Read config file; compare with working defaults |

8. **Verify**: Run the full test suite via `/tdd-guide` to confirm no regressions.
9. **Version Bump**: Apply `10-semantic-versioning.md` â€” bump the Patch version in root `PROJECT_METADATA.md` (v0.1.X).
10. **Log**: Append a session entry to `.agent/session-context.md` detailing what was fixed.
11. **Validate**: Run `cross-agent-validator` to confirm patches are real and version was bumped.

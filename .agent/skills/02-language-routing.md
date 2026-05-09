---
name: language-routing
description: Skill for language-routing
---

# Language Routing Protocol

This skill detects the programming language(s) of the current task and routes to the correct language-specific agent for specialized handling.

## Detection Methods (in priority order)

1. **File extension**: `.py` → Python, `.rs` → Rust, `.js/.ts` → JS/TS, `.c/.h` → C, `.go` → Go
2. **Shebang lines**: `#!/usr/bin/env python3` → Python
3. **Import patterns**: `import React` → JS/TS, `use std::` → Rust
4. **Build file presence**: `Cargo.toml` → Rust, `package.json` → JS/TS, `pyproject.toml`/`requirements.txt` → Python, `go.mod` → Go, `Makefile` with gcc → C

## Routing Table

| Detected Language | Agent | Skills Loaded |
|---|---|---|
| Python | `15-python-agent` | PY-R rules, PY-INSTINCT instincts, mypy/pytest workflow |
| Rust | `16-rust-agent` | RS-R rules, RS-INSTINCT instincts, cargo clippy/miri workflow |
| JavaScript/TypeScript | `17-jsts-agent` | JSTS-R rules, JSTS-INSTINCT instincts, tsc/eslint workflow |
| C | `18-c-agent` | C-R rules, C-INSTINCT instincts, gcc -Wall/valgrind workflow |
| Go | `19-go-agent` | GO-R rules, GO-INSTINCT instincts, go vet/staticcheck workflow |

## Polyglot Mode

When a repository contains multiple languages:
- Segment by directory/subsystem
- Route each sub-task to the appropriate language agent
- Define handoff contracts between agents at language boundaries (FFI, API schemas, shared configs)

## Version Detection

Language rules depend on runtime/edition specifics:
- Check `pyproject.toml` for Python version
- Check `Cargo.toml` for Rust edition
- Check `tsconfig.json` for TypeScript target
- Check `go.mod` for Go version
- Check `Makefile` or `CMakeLists.txt` for C standard

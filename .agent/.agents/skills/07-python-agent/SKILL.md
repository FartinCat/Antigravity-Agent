---
name: python-agent
description: Python-specific language agent. Encodes Python rules, instincts, and verification workflows for type-safe, idiomatic Python development.
origin: Custom Ensemble (Claude + DeepSeek + Gemini)
---

# Agent: Python Language Specialist

## Rules

### PY-R001: TYPE_HINTS_MANDATORY
All function signatures must include type hints for parameters and return types. Use `from __future__ import annotations` for forward references.

### PY-R002: NO_MUTABLE_DEFAULTS
Never use mutable objects (`[]`, `{}`, `set()`) as default arguments. Use `None` and initialize inside the function body.

### PY-R003: EXPLICIT_EXCEPTIONS
Never use bare `except:` or `except Exception:` without re-raising or logging. Catch the most specific exception type.

### PY-R004: CONTEXT_MANAGERS_FOR_RESOURCES
Files, database connections, locks, and network sockets must use `with` statements or `contextlib.contextmanager`.

### PY-R005: NO_STAR_IMPORTS
`from module import *` is prohibited. Always import specific names.

### PY-R006: ASYNC_BOUNDARY_CLARITY
Sync and async code must have clear boundaries. Never call `asyncio.run()` inside an already-running event loop.

### PY-R007: FROZEN_DATACLASSES
Data-holding classes should use `@dataclass(frozen=True)` unless mutation is explicitly required and justified.

### PY-R008: PATHLIB_OVER_OS_PATH
Use `pathlib.Path` instead of `os.path` for all filesystem operations.

---

## Instincts

### PY-INSTINCT-001: SHARED_MUTABLE_STATE (p=0.82)
A module-level list or dict is imported and mutated by multiple functions.

### PY-INSTINCT-002: GENERATOR_EXHAUSTION (p=0.75)
A generator is iterated multiple times without `itertools.tee()` or conversion to list.

### PY-INSTINCT-003: PANDAS_CHAINED_INDEXING (p=0.88)
`df[col][row]` instead of `df.loc[row, col]`. Causes SettingWithCopyWarning.

### PY-INSTINCT-004: ASYNCIO_BLOCKING_CALL (p=0.91)
`time.sleep()`, `requests.get()`, or file I/O inside an `async def` function without `asyncio.to_thread()`.

### PY-INSTINCT-005: PICKLE_SECURITY (p=0.95)
`pickle.load()` on untrusted data. Flag as critical security risk.

### PY-INSTINCT-006: DICT_KEY_MUTATION (p=0.70)
Iterating over a dict while adding/removing keys.

### PY-INSTINCT-007: SUBPROCESS_INJECTION (p=0.93)
`subprocess.run(shell=True)` with user-provided input. Flag as command injection risk.

---

## Verification Workflow
1. `mypy --strict` — type checking
2. `ruff check` or `flake8` — linting
3. `bandit -r` — security scanning
4. `pytest` — unit tests
5. Circular import check: `python -c "import {module}"` for all entry points
\n## Advanced Operations Matrix\n\n- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.\n- **Simulation & Modeling**: For scientific simulations, employ 
umpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.\n- **Performance Profiling**: Run python -m cProfile or 	imeit to benchmark critical sections.\n- **Precise Explanation**: Include step‑by‑step rationale in markdown code comments and a short summary in plain text.\n- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re‑raise if unrecoverable.\n

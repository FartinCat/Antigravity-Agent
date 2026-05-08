# Side-Effect Tracker

**Purpose**: Detects global state mutation inside functions whose names imply purity.

## Target Patterns

Functions matching these name prefixes are expected to be **pure** (no side effects):
- `get_*`, `is_*`, `has_*`, `can_*`
- `calc_*`, `compute_*`, `derive_*`
- `format_*`, `render_*`, `stringify_*`
- `parse_*`, `validate_*`, `check_*`

## Violation Conditions

A flagged function performs any of these inside its body:
1. **Global state mutation**: Modifies a module-level variable, class-level mutable state, or singleton
2. **I/O operations**: File read/write, network calls, database queries, console output
3. **Input mutation**: Modifies the contents of a passed-in mutable argument (list, dict, object)
4. **Non-deterministic behavior**: Uses `random`, `time.now()`, or `uuid` without documenting it

## Action on Violation

1. **Warning**: Flag the function with `INSTINCT-006: NO_UNDOCUMENTED_SIDE_EFFECTS`
2. **Suggestion**: Either rename the function to reflect its side effects (e.g., `get_and_cache_user`) or refactor to remove the side effect
3. **Documentation**: If the side effect is intentional, require a `# SIDE-EFFECT:` comment explaining what it mutates and why

## Exemptions
- Functions in test files (`test_*.py`, `*.test.ts`)
- Functions explicitly decorated/annotated as having side effects (`@with_side_effects`, `// side-effect: ...`)

## Advanced Operations Matrix

- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.
- **Simulation & Modeling**: For scientific simulations, employ numpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.
- **Performance Profiling**: Run python -m cProfile or timeit to benchmark critical sections.
- **Precise Explanation**: Include step-by-step rationale in markdown code comments and a short summary in plain text.
- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re-raise if unrecoverable.

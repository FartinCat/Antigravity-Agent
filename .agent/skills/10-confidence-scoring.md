# Confidence Scoring System

Every LLM output is assigned a confidence score before acceptance. This score determines which verification gates must be passed.

## Formula

```
base_score = 70

Modifiers (additive):
  +10: Task is purely syntactic (rename, reformat) — low ambiguity
  +10: Output has <20 lines of new code
  +5:  Language agent's linter passes with no warnings
  +5:  Output matches a known pattern in skill store
  -10: Task requires reasoning about >2 files simultaneously
  -10: Task involves async, concurrency, or parallel execution
  -15: Task involves security (auth, crypto, input validation)
  -20: Task involves unsafe code (C unsafe blocks, Rust unsafe, pointer arithmetic)
  -5:  LLM output contains uncertainty language:
       ["should work", "might", "probably", "I think", "seems like", "I believe"]
```

## Thresholds

| Score | Action |
|---|---|
| ≥ 85 | Auto-accept. Run verification from Level 1. |
| 70-84 | Accept. Run verification from Level 1. Flag for spot check. |
| 50-69 | Hold for human review. Present draft with reasoning. |
| < 50 | Do not accept. Decompose the task further and retry. |

## Blast Radius Estimation

Estimate how many files/systems a change touches:
- **Blast radius ≤ 2**: Confidence Level 0 (autonomous)
- **Blast radius 3-5**: Confidence Level 1 (auto + inspector validation)
- **Blast radius > 5**: Confidence Level 2 (human reviews summary)
- **Security-critical**: Confidence Level 4 (human designs and implements)

## Advanced Operations Matrix

- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.
- **Simulation & Modeling**: For scientific simulations, employ numpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.
- **Performance Profiling**: Run python -m cProfile or timeit to benchmark critical sections.
- **Precise Explanation**: Include step-by-step rationale in markdown code comments and a short summary in plain text.
- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re-raise if unrecoverable.

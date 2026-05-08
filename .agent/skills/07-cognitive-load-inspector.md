# Cognitive Load Inspector

**Purpose**: Measures the cognitive complexity of functions and blocks code that exceeds safe thresholds for LLM reasoning.

## Metrics

### 1. Nesting Depth Score
Each level of nesting adds weight:
- Level 1 (top-level if/for/while): +1
- Level 2 (nested): +2
- Level 3 (double nested): +3
- Level 4+ (deep): +4 per additional level

### 2. Variable Mutation Score
- Each variable reassigned inside a loop: +2
- Each variable reassigned conditionally: +1
- Each accumulator pattern (not flagged): +0

### 3. Declaration-Usage Distance
- Variable declared and used within 5 lines: +0
- Variable declared and first used 6-15 lines away: +1
- Variable declared and first used >15 lines away: +3

### 4. Control Flow Breaks
- Each `break`, `continue`, `goto`, early `return` (after the guard clause section): +2
- Each exception thrown in the middle of a function: +2

## Composite Score

```
Cognitive_Complexity = Σ(nesting_depth) + Σ(mutation) + Σ(distance) + Σ(flow_breaks)
```

## Thresholds

| Score | Verdict |
|---|---|
| ≤ 10 | **GREEN** — Safe for any LLM |
| 11-15 | **YELLOW** — Acceptable, but document the logic with inline comments |
| 16-25 | **ORANGE** — Must decompose before sending to a low-tier LLM |
| > 25 | **RED** — Mandatory refactoring. No LLM should attempt to reason about this function as-is |

## Refactoring Strategies for RED functions
1. **Extract Method**: Pull nested logic into named helper functions
2. **Guard Clause**: Convert deep nesting into early returns
3. **Table-Driven Logic**: Replace cascading if/else with a lookup table
4. **State Machine**: Replace complex conditional chains with explicit state transitions
5. **Pipeline**: Replace nested transformations with chained operations (map/filter/reduce)

## Advanced Operations Matrix

- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.
- **Simulation & Modeling**: For scientific simulations, employ numpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.
- **Performance Profiling**: Run python -m cProfile or timeit to benchmark critical sections.
- **Precise Explanation**: Include step-by-step rationale in markdown code comments and a short summary in plain text.
- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re-raise if unrecoverable.

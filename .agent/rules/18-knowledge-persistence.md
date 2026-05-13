---
rule: 18-knowledge-persistence
priority: MEDIUM
---
# Rule 18: Knowledge Persistence

## The Law
Valuable discoveries must be stored — not just completed — before the session ends.

## Why This Exists
Prevents solving the same problem three sessions in a row, repeating research that was done last week, and losing architectural decisions that were made but not documented.

## Mandatory Behaviors
1. Search memory before initiating any non-trivial work.
2. At session end, explicitly evaluate what should persist (conventions, gotchas, decisions, reusable fixes).
3. Write a session summary to **`AETHER.md` Section 18** before closing out.
4. Output code-level knowledge to `docs/ai/`.
5. Use the Memory MCP (if available) for cross-project knowledge persistence.

## Prohibited Behaviors
1. Storing raw logs or transcripts as "memory".
2. Storing one-time task progress or temporary state.
3. Storing speculation without verification.
4. Creating duplicate memories without checking existing stores.

## Enforcement
- Session close routines must explicitly invoke knowledge capture for identified patterns.

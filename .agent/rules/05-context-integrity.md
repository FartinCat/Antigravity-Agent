# Context Integrity Rules

These rules prevent "context drift" — the agent acting on stale or inaccurate information about the project state.

## R4-001: NO_STALE_FILE_SUMMARIES
After any file write, all cached summaries of that file must be invalidated. No agent may act on a pre-write summary after a modification has occurred.

## R4-002: NO_STALE_CALL_GRAPHS
After structural edits (new functions, renamed exports, changed signatures), the call graph must be re-derived before any agent reasons about dependencies.

## R4-003: SKILL_VERSION_CHECK
Before applying a cached skill, verify that:
- The language version matches (Python 3.10 vs 3.12, Rust edition 2021 vs 2024)
- The framework version matches (React 18 vs 19, Django 4 vs 5)
- The project context hasn't changed since the skill was last validated

## R4-004: CONTEXT_WINDOW_AWARENESS
When a task requires reasoning about more than 3 files simultaneously:
1. Do NOT send all files to the LLM in one call
2. Extract information from each file separately
3. Synthesize results using rule-based logic (not LLM)
4. Send only the synthesis to the LLM for the final step

## R4-005: PATCH_QUALITY_REQUIREMENTS
Every patch produced by the agent must include:
- **Reason**: Why this change is needed
- **Scope**: Which symbols/functions are affected
- **Verification evidence**: Which gate was passed
- **Rollback target**: What to revert if the patch causes regressions

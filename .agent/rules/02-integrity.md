# Universal Integrity Rules (Hard Stops)

These are non-negotiable. The agent will halt and alert the user if any rule is violated, regardless of instruction.

## R1-001: NEVER_EDIT_ARTIFACTS
Any file inside a build output directory (`dist/`, `build/`, `target/`, `__pycache__/`, `*.pyc`, `*.class`, `*.o`, `*.so`, `*.dll`) is an artifact. Never edit artifacts. Edit source → rebuild → verify artifact changed.

## R1-002: NEVER_COMMIT_SECRETS
API keys, passwords, private keys, connection strings with credentials. If a secret pattern is detected in a file about to be written, halt and redact.

## R1-003: NEVER_SKIP_VERIFICATION
Each action type has a corresponding verification step. The verification step cannot be skipped, abbreviated, or declared "assumed to pass."

## R1-004: NEVER_ASSUME_STATE
The agent must not assume that a previous action's result is still current unless re-verified within the same sub-task window.

## R1-005: NEVER_FIX_SYMPTOMS
The root cause of a bug must be identified before a fix is applied. A fix that patches a symptom without addressing the root cause is classified as a deferred bug, not a fix.

## R1-006: NO_UNDOCUMENTED_SIDE_EFFECTS
A function whose name/documentation implies purity (`get_`, `compute_`, `parse_`, `format_`) must not modify global state, perform I/O, or mutate input arguments.

## R1-007: ERROR_MESSAGES_MUST_BE_ACTIONABLE
Every `log.error()` or error return must include the error object or a unique error code — never a bare string without context.

## R1-008: INPUT_SIZE_LIMITS
Any endpoint or function accepting externally-sourced data must enforce a maximum size before processing.

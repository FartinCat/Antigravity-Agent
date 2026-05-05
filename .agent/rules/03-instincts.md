# Universal Instincts Layer

Instincts are probabilistic warnings — they fire a flag, not a halt. Unlike rules, a user can override an instinct with justification. Each instinct has a probability score indicating how often the flagged pattern is a real problem.

---

## Structural Instincts

### INSTINCT-001: MISSING_INVERSE_OPERATION (p=0.78)
A function named `save*`, `write*`, `push*`, `insert*`, `create*`, `send*` exists without a corresponding `load*`, `read*`, `pop*`, `get*`, `delete*`, `receive*` function being called on initialization or the relevant event.

### INSTINCT-002: DEEP_NESTING_SMELL (p=0.71)
Code with nesting depth > 4 (`if` inside `for` inside `if` inside `try`...). Suggest extraction into named functions.

### INSTINCT-003: LARGE_FUNCTION (p=0.68)
A function exceeding 60 lines of executable code. Likely has more than one responsibility.

### INSTINCT-004: ASYMMETRIC_RESOURCE_HANDLING (p=0.85)
A resource is opened/acquired (file, socket, lock, DB connection) without a visible close/release path in the same scope or a `finally`/`defer`/`Drop`/RAII pattern. Near-rule level — require explicit justification to pass.

### INSTINCT-005: CONFIG_HARDCODED (p=0.83)
A URL, port number, file path, or API endpoint appears as a string literal in application logic (not in a config file or constant).

---

## LLM-Specific Instincts

### INSTINCT-L001: HALLUCINATED_API (p=0.60)
The LLM is about to call a function/method that does not appear in the project's dependency list or the language's standard library. Verify existence before writing the call.

### INSTINCT-L002: COPY_WITHOUT_ADAPTATION (p=0.55)
A code block is structurally identical to code in another file but with different variable names. Require explicit statement of why this pattern applies here.

### INSTINCT-L003: INCOMPLETE_ERROR_PATH (p=0.90)
The LLM writes the happy path but the error path contains only `// handle error` or `pass`. Require error path completion before proceeding.

### INSTINCT-L004: STALE_CONTEXT_DRIFT (p=0.65)
The current task is more than 5 sub-tasks removed from when the relevant context was loaded. Re-inject the relevant context before continuing.

### INSTINCT-L005: OVERCONFIDENT_COMPLETION (p=0.80)
The agent declares a task "done" without having run a verification step. Mandatory verification before "done" status.

---

## Advanced Instincts

### INSTINCT-006: RACE_WINDOW_TOCTOU (p=0.92)
Checking file existence then opening it, or checking null then dereferencing, with possible interleaving.

### INSTINCT-007: CROSS_FILE_RENAME_DRIFT (p=0.87)
An identifier changed in one file but related docs, tests, configs, imports, or error messages still use the old term.

### INSTINCT-008: SEMANTIC_COMPRESSION_RISK (p=0.72)
A weak model proposes replacing several distinct concepts with one generic abstraction. Flag as likely loss of domain meaning.

### INSTINCT-009: VERIFICATION_WEAKNESS (p=0.76)
Verification uses only build success or only snapshot tests. Flag as underpowered.

### INSTINCT-010: LOCAL_FIX_GLOBAL_PATTERN (p=0.81)
A bug is patched in one site but pattern search shows similar structures elsewhere. Elevate to project-wide inspection.

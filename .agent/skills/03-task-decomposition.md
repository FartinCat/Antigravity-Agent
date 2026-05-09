---
name: task-decomposition
description: Skill for task-decomposition
---

# Task Decomposition Protocol (Low-Tier LLM Compensation)

This skill ensures that every task given to an LLM is small enough to be solved correctly, even by weaker models.

## Cognitive Load Budget

Every sub-task receives a Reasoning Unit (RU) score:
- **RU=1**: Trivial — rename, format, copy/paste
- **RU=2**: Single-function logic with all context inlined
- **RU=3**: Multi-step algorithm within one file
- **RU=4**: Cross-file coordination or stateful reasoning

**Rule**: Low-tier LLMs are capped at RU ≤ 2. Tasks above this are automatically decomposed further.

## Decomposition Rules

### DECOMP-001: ONE_FILE_PER_CALL
A low-tier LLM call must touch at most one file. Multi-file features → sequential calls.

### DECOMP-002: INTERFACE_BEFORE_BODY
Call 1: "Write only the function signature and docstring for X"
Call 2: "Write only the body of X, given this signature: {output of Call 1}"

### DECOMP-003: READ_BEFORE_WRITE
Always a separate call: "Read this file and tell me: what does function Y do?"
Then: "Now modify function Y to also do Z, given your previous description."

### DECOMP-004: FIX_ONE_ERROR_PER_CALL
When a build fails with 5 errors, fix them one at a time. Never present all errors at once.

### DECOMP-005: SUMMARIZE_THEN_ACT
For files over 200 lines: first call = "Summarize what each function does in 2-3 words each." Second call = the actual task, with the summary injected instead of the full file.

## Staged Prompt Construction

Prompts are compiled from validated fragments:
```
Prompt = Role_Block + Context_Island + Invariant_Guard + Action_Step + Output_Schema + Anti_Hallucination_Guard
```

## Adversarial Verification

After a code change, spawn a separate "Devil's Advocate" check:
"Given this diff and the original code, what is the most dangerous thing that could go wrong?"

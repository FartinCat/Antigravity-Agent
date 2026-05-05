# Refactor Logic

This file contains the foundational principles used by the `tdd-guide` agent during Phase 3 (Refactor) and by the `antibug` agent when proposing structural improvements.

## Core Mandate
Refactoring is **not rewriting**. It is the disciplined improvement of existing, tested code without changing its observable behavior. Tests must stay green throughout every refactor step.

## The Refactor Checklist

### 1. Naming
- Every variable, function, and class name must be self-documenting. If a comment is needed to explain what a name means, rename it instead.
- Functions should be named after **what they do**, not **how they do it**.
- Boolean variables and functions should read as assertions: `is_valid`, `has_permission`, `can_proceed`.

### 2. Function Size & Single Responsibility
- A function should do **one thing**. If you can describe it with "and", it does too many things — split it.
- Target: no function longer than 20–30 lines. If it grows beyond this, extract helpers.
- Exception: orchestration functions that explicitly coordinate multiple sub-steps are allowed to be longer, but each sub-step must be a named function call.

### 3. Duplication Elimination (DRY)
- Identify repeated logic patterns (3+ occurrences). Extract into a shared utility function.
- Do not eliminate duplication until it appears at least twice — premature abstraction is worse than duplication.

### 4. Magic Numbers and Strings
- Replace all hardcoded literals with named constants.
  - Bad: `if score > 85:`
  - Good: `PASSING_THRESHOLD = 85` then `if score > PASSING_THRESHOLD:`

### 5. Error Handling Clarity
- Every error path must be explicit, logged, and handled — never silently swallowed.
- Prefer specific exception types over bare `except Exception`.
- Error messages must be actionable: state what happened, why it happened, and what the user or system should do next.

### 6. Dependency Direction
- High-level modules must not depend on low-level implementation details.
- Inject dependencies rather than importing them directly inside functions where possible.

## Banned Refactor Patterns
- Renaming things "to be cleaner" while tests are failing. Refactor only on green.
- Adding new functionality during a refactor step. That is a new Red phase.
- Removing tests because the code "obviously works." Tests are documentation — never delete them.

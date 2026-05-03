---
description: "Orchestrates the bug hunting process: Deep Scan -> Antibug -> Patch Bump."
---

# Workflow: Fix Bugs

**Objective**: Automatically track down and resolve syntax errors, logic flaws, and memory leaks.

## Execution Sequence

1. **Scan**: Invoke `deep-scan` to map the current repository structure and identify recently modified files.
2. **Hunt**: Pass the context to the `/antibug` skill to deeply analyze the logic.
3. **Patch**: Apply the fixes.
4. **Version Bump**: Invoke `semantic-versioning` to bump the Patch version (v0.1.X).

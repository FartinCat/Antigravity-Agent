---
description: "Step 9 — Finalize the project: Clean dump → Market Evaluation → License → README → v1.0.0 release."
order: 10
---

# Workflow: Release Project

**Objective**: Finalize a project for public consumption and monetization. This is the "God Mode" pipeline.

## Execution Sequence

1. **Auto-Cleanup**: Trigger the `dump-awareness` instinct. The AI actively scans the project root for stray reference folders (`frontend1`, `app2`, etc.) and moves them into the `dump/` directory. **The `.agent/` folder is NEVER moved or touched during cleanup.**

2. **Scanner**: Invoke `/scanner` to produce a final state-of-project report confirming cleanup was successful and the project root is clean.

3. **Evaluate**: Invoke the `/market-evaluator` skill. Read root `PROJECT_METADATA.md` and the scanner output to determine codebase complexity and suggest commercial pricing tiers based on missing/present features.

4. **License**: Invoke the `/commercial-license` skill. Generate a custom `LICENSE.md` at the project root prohibiting free commercial use, allowing free access for validated contributors, and requiring institutional verification for academic users.

5. **Document**: Invoke the `/readme-architect` skill to build the final `README.md`.
   - **Step 5a**: Ask the user to provide a banner image path or generate a placeholder SVG banner. Do NOT call `generate_image` — this tool does not exist in the system. Instead, create a clean SVG banner or use a placeholder instruction.
   - **Step 5b**: Build the full `README.md` following the premium structure (Badges, Architecture, Method A/B guides, and Session Memory section).

6. **Version Bump**: Invoke `semantic-versioning` to bump the Major version to `v1.0.0` in root `PROJECT_METADATA.md`.

7. **Log**: Append a release entry to `.agent/session-context.md` with the release version and date.

8. **Validate**: Run `cross-agent-validator` to confirm all release artifacts are present.

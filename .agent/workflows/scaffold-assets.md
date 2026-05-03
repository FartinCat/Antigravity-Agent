---
description: Automatically scaffolds the standardized assets/ directory taxonomy and initializes PROJECT_METADATA.md at the project root.
---

# Workflow: Scaffold Asset Taxonomy

**Objective**: Enforce a standardized resource organization matrix and bootstrap the project metadata state file required by versioning, market-evaluator, and commercial-license agents.

## Execution Sequence

1. **Root Resolution**: Apply the `asset-awareness` injection point rule:
   - If `src/` exists → create `src/assets/` and all sub-directories inside it.
   - If `src/` does not exist → create `assets/` at project root.
   - Broadcast the resolved `ASSETS_ROOT` path to all active agents for the session.

2. **Taxonomy Generation**: Create the following sub-directories inside `ASSETS_ROOT`:
   - `images/`
   - `videos/`
   - `audios/`
   - `texts/`
   - `information/`
   - `icons/`

3. **Root Metadata Bootstrap**: Create `PROJECT_METADATA.md` at the **project root** (not inside assets/) if it does not already exist. Use this template:
   ```markdown
   # Project Metadata
   
   **Project Name**: [TO BE FILLED]
   **Version**: 0.1.0
   **Author**: [TO BE FILLED]
   **Created**: [DATE]
   **Status**: In Development
   
   ## Description
   [Brief description of the project]
   
   ## Tech Stack
   - [e.g., Python 3.11 / React 18 / LaTeX]
   
   ## Feature Checklist
   - [ ] Feature 1
   - [ ] Feature 2
   
   ## Changelog
   - v0.1.0: Project initialized.
   ```

4. **Information Seed**: Copy `PROJECT_METADATA.md` into `ASSETS_ROOT/information/` as well, so `market-evaluator` and `commercial-license` agents can locate it via either path.

5. **Path Resolution Broadcast**: Announce the resolved `ASSETS_ROOT` path internally so all subsequent code synthesis (HTML, React, LaTeX, Python) uses the correct relative paths.

## Manual Invocation
- Via chat: `/scaffold-assets`
- Automatically triggered by `asset-awareness` instinct when structural non-compliance is detected.
- Automatically triggered as Step 1 of `build-website` and `build-app` workflows.

---
title: "SCAFFOLD ASSETS"
description: "Initialize project structure and taxonomy."
order: 3
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

3. **Documentation Bootstrap**: Ensure the following folders exist in the new project root so generated reports always land in the documented location:

   - `docs/scan-reports/`
   - `docs/audit-reports/`
   - `docs/master-plans/`
   - `docs/research/`
   - `docs/market-evaluations/`

4. **Archive Bootstrap**: Ensure the archive hierarchy exists for moved, deleted, and versioned artifacts:

   - `archived/archive-registry/`
   - `archived/current-version/`
   - `archived/old-versions/`
   - `archived/references/`

5. **Root Metadata Bootstrap**: If root **`AETHER.md`** is missing, create a minimal stub that includes **§14 Project Metadata** and **§18 Session Context** using this template (otherwise only fill empty §14 fields in-place):

   ```markdown
   # Aether Agent v0.1.0 — [Project Name]

   ## 14. Project Metadata

   **Project Name**: [TO BE FILLED]
   **Version**: 0.1.0
   **Author**: [TO BE FILLED]
   **Created**: [DATE]
   **Status**: In Development

   ### Description
   [Brief description of the project]

   ### Tech Stack
   - [e.g., Python 3.11 / React 18 / LaTeX]

   ### Feature Checklist
   - [ ] Feature 1
   - [ ] Feature 2

   ## 16. Changelog

   ### [0.1.0] - [DATE]
   - Project initialized.

   ## 18. Session Context

   # Session Context — [DETECTED PROJECT DIRECTORY NAME]
   Initialized: [DATE]
   Project Directory: [DETECTED PROJECT DIRECTORY NAME]
   ```

6. **Single Source of Truth**: **`AETHER.md` at the project root** is the authoritative version + changelog + session file. Do NOT maintain a competing `PROJECT_METADATA.md` or `.agent/session-context.md`. The `market-evaluator` and `commercial-license` agents read from **`AETHER.md` §14**.

7. **Session Context Init**: Trigger the `06-context-memory.md` rule — ensure **`AETHER.md` §18** exists and has the correct `Project Directory:` field for this project.



8. **Path Resolution Broadcast**: Announce the resolved `ASSETS_ROOT` path so all subsequent code synthesis uses the correct relative paths.



## Manual Invocation

- Via chat: `/scaffold-assets`

- Automatically triggered by `asset-awareness` instinct when structural non-compliance is detected.

- Automatically triggered as Step 1 of `build-website` and `build-app` workflows.


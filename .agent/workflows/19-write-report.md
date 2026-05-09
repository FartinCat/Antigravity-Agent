---
title: "WRITE REPORT"
description: "Generate status reports and technical summaries."
order: 9
---

# Workflow: Write Report



**Objective**: Execute a pipeline for generating high-quality academic or technical reports.



## Execution Sequence



1. **Scanner**: Invoke `/scanner` to understand the project state, existing documents, `.bib` files, and figure assets before planning the report.

2. **Outline**: Invoke `/planner` to create a chapter-by-chapter outline based on the scanner output and any existing notes or drafts.

3. **Draft**: Apply `/scientific-writing` skill to ensure objective tone and banned patterns are respected throughout.

4. **Format**: Invoke `/latex-bib-manager` to clean citations, sort bibliographies, and enforce strict float anchors.

5. **Log**: Append a session entry to `.agent/session-context.md` with the report outline and current completion status.

6. **Finalize**: Generate the final PDF or document output. Version bump (Minor) in `PROJECT_METADATA.md`.


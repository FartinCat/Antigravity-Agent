# Workflow: Write Report

**Objective**: Generate a structured technical or academic report with proper formatting, citations, logical flow, and professional typography. Use for status reports, technical summaries, research writeups, post-mortems, and documentation deliverables.

## Trigger Conditions
- User requests a report, summary, or writeup
- User says "write a report on..." or "document the findings"
- Invoked via `/write-report`

## Execution Sequence

### Phase 1 — Report Scoping
1. **Determine Report Type**: Classify as one of:
   - **Status Report**: Progress update with metrics and blockers
   - **Technical Summary**: Deep dive into a system, feature, or architecture
   - **Research Report**: Findings from investigation with citations
   - **Post-Mortem**: Incident analysis with root cause and remediation
   - **Decision Record**: ADR-style record of a technical decision
2. **Identify Audience**: Determine technical depth (executive summary vs. engineer deep-dive).
3. **Gather Sources**: List all files, logs, conversations, and data that will inform the report.
4. **Define Sections**: Create an outline with 4-8 major sections.

**Gate**: Confirm report type, audience, and outline with user before writing.

### Phase 2 — Content Generation
1. **Executive Summary**: Write a 3-5 sentence summary that stands alone. A reader who reads ONLY this paragraph should understand the conclusion.
2. **Body Sections**: Write each section following the outline. Rules:
   - Lead with the conclusion, then support with evidence (inverted pyramid)
   - Use tables for comparative data (never inline lists of > 4 items)
   - Use code blocks for technical examples
   - Use Mermaid diagrams for architecture and flow descriptions
   - Cite sources with `[source](link)` format
3. **Metrics & Data**: Present quantitative findings in tables or bullet lists with units.
4. **Recommendations**: End each major section with 1-2 actionable recommendations.

### Phase 3 — Polish & Review
1. **Heading Hierarchy**: Verify single `#` for title, `##` for major sections, `###` for subsections.
2. **Consistency Check**: Ensure terminology is consistent throughout (no mixing "server/instance/node" for the same concept).
3. **Length Check**: 
   - Status reports: 1-2 pages (500-1000 words)
   - Technical summaries: 3-5 pages (1500-3000 words)
   - Research reports: 5-10 pages (3000-6000 words)
4. **Grammar & Tone**: Professional, active voice, no filler phrases ("it should be noted that...").
5. **Actionability**: Every section must end with a clear next step or conclusion.

**Gate**: Self-review the report against the checklist before presenting.

### Phase 4 — Delivery
1. **Format**: Output as markdown with proper frontmatter (title, date, author, version).
2. **Save**: Write to the appropriate `docs/` subdirectory per Rule 20.
3. **Announce**: Summarize the key findings and recommendations to the user.

## Failure Paths
- **Insufficient Data**: If sources are missing, flag gaps explicitly: "Section X could not be completed due to missing [data]. Recommend [action]."
- **Scope Creep**: If the report grows beyond the target length, split into a summary + appendix structure.
- **Ambiguous Requirements**: If the report type or audience is unclear, default to Technical Summary for engineers.

## Report Template
```markdown
# [Report Title]
**Date**: YYYY-MM-DD | **Author**: Antigravity Agent | **Version**: 1.0

## Executive Summary
[3-5 sentences covering the key finding/conclusion]

## Background
[Context needed to understand the report]

## Findings
### [Finding 1]
[Evidence and analysis]

### [Finding 2]
[Evidence and analysis]

## Recommendations
1. [Action item with priority]
2. [Action item with priority]

## Appendix
[Supporting data, raw logs, extended analysis]
```

## Output Organization (Rule 20)
Save to `docs/reports/REPORT_{NN}.md` (increment NN zero-padded).

---
name: readme-architect
description: Generates a highly structured, comprehensive, and engaging README.md for the project from a layman's perspective.
origin: Custom Ensemble
---

# README Architect

Generate the ultimate project documentation. The README must not be boring. It must be engaging, deeply structural, and easy to understand for absolute beginners.

## Pre-Task Protocol
Before generating anything, execute the **Research Loop**:
1. Run `/scanner` to understand the project structure.
2. Read root `PROJECT_METADATA.md` for name, version, author, and tech stack.
3. Check if `MARKET_EVALUATION.md` exists for commercial positioning information.
4. Read `LICENSE.md` for accurate license terms to include.

## When to Activate

- When a project is nearing completion.
- When running the `/release-project` workflow.
- When requested to "document the project" or "build a readme".

## Required Structure

The generated `README.md` MUST follow this exact premium sequence:

1. **The Centered Header**:
   - Use `<div align="center">`.
   - **Banner**: If a banner image exists in `assets/images/`, reference it. If not, create an elegant SVG banner inline using the project name and a subtitle. Do NOT reference `generate_image` — this tool does not exist. Use SVG or ask the user to provide a banner path.
   - **Title & Subtitle**: Engaging and bold.
   - **Badges**: Include Shields.io badges for Version (from `PROJECT_METADATA.md`), languages (from tech stack), and License.
   - **The Hook**: A relevant quote in a blockquote.

2. **Architecture Section**: Explain the core structure — the high-level logic flow and key design decisions.

3. **Quick Start & Usage Guides**:
   - **Method A**: For Native AI IDEs — slash commands, workflows, `+` button.
   - **Method B**: For Plain Chat (Claude.ai, ChatGPT) — see `HOW-TO-USE.md` for the paste-SKILL.md method.

4. **Agent/Component Reference Table**: A clean table mapping commands/files to their purposes.

5. **Visual Logic**: Include a Mermaid.js diagram to map the core application logic.

6. **Session Memory Section**: Explain how `session-context.md` provides cross-session memory and how the project-directory detection works on migration.

7. **Deployment Guide**: Reference `DEPLOY.md` for instructions on copying `.agent/` to new projects.

8. **Release & Legal**:
   - **License**: Summarize from `LICENSE.md`. Mention commercial fee, contributor access, academic verification requirement.
   - **Data Privacy**: Note that `MARKET_EVALUATION.md` and `PROJECT_METADATA.md` may contain sensitive data and should be reviewed before making public.

## Design Principles
- **Rich Aesthetics**: Use emojis, horizontal rules, and alignment divs.
- **No Placeholders**: Use SVG banners, real badges, and real data from project files.
- **Clarity first**: Bold key terms. Write for someone who has never seen the project before.

## Banned Patterns
- Referencing `generate_image` — this tool does not exist.
- Writing "[IMAGE HERE]" or "[BANNER HERE]" as final output. Either generate an SVG or explicitly ask the user for the banner file path.
- Generic README content that could apply to any project. Every section must reference actual project files and decisions.
\n## Advanced Operations Matrix\n\n- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.\n- **Simulation & Modeling**: For scientific simulations, employ 
umpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.\n- **Performance Profiling**: Run python -m cProfile or 	imeit to benchmark critical sections.\n- **Precise Explanation**: Include step‑by‑step rationale in markdown code comments and a short summary in plain text.\n- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re‑raise if unrecoverable.\n

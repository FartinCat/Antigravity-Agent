---
name: readme-architect
description: Generates a highly structured, comprehensive, and engaging README.md for the project from a layman's perspective.
origin: Custom Ensemble
---

# README Architect

Generate the ultimate project documentation. The README must not be boring. It must be engaging, deeply structural, and easy to understand for absolute beginners.

## When to Activate

- When a project is nearing completion.
- When running the `/release-project` workflow.
- When requested to "document the project" or "build a readme".

## Required Structure

The generated `README.md` MUST follow this exact sequence:

1. **The Hook**: Start with a relevant, funny coding quote or a profound thought from a great researcher (e.g., Nikola Tesla, Alan Turing) formatted as a blockquote. Use emojis strategically to make it visually interesting.
2. **Objective & Links**: Provide a clear, layman's explanation of what the project does. Include placeholder links for GitHub, Vercel, Render, or other deployment platforms.
3. **Deep-Scan Schematic**: Trigger or use the output of `deep-scan` to print a folder tree. **Explain the reason each core file/folder exists**.
4. **Algorithm Tree**: Provide a Mermaid.js flowchart mapping out the core logic or process of the software/report. This makes complex code easy to understand visually.
5. **Acronym Dictionary**: State the full forms of any acronyms or code words used in the project (e.g., API, SSR, TTS).
6. **Pros & Cons Table**: Create an objective table evaluating the project's current state, strengths, and limitations.
7. **Monetization & License Table**: Add a table detailing the commercial and free usage terms, strictly aligning with the output of the `commercial-license` skill (i.e., Pay for Commercial, Free for active Contributors).
8. **Installation Guide**: Clear, step-by-step instructions on how to install and run the project from the GitHub repository.

## Banned Patterns

- Do not use generic boilerplate text.
- Do not skip the visual elements (Mermaid charts, tables, emojis).
- Do not assume the reader knows advanced terminology without checking the Acronym Dictionary.

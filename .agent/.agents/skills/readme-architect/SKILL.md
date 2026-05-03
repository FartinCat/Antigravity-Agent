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

The generated `README.md` MUST follow this exact premium sequence:

1.  **The Centered Header**:
    - Use `<div align="center">`.
    - **Banner**: Instruct the user to generate or provide a premium banner image.
    - **Title & Subtitle**: Engaging and bold.
    - **Badges**: Include Shields.io badges for Version, Languages (Python, Rust, etc.), and License.
    - **The Hook**: A profound quote (e.g., Tesla, Turing) in a blockquote.
2.  **Architecture Section**: Explain the core structure (e.g., the "Dual-Skill" pattern if applicable, or the high-level logic flow).
3.  **Quick Start & Usage Guides**:
    - **Method A**: For Native AI IDEs (Slash commands, Workflows).
    - **Method B**: For Plain Chat (Copy-pasting SKILL.md).
4.  **Agent/Component Reference Table**: A clean table mapping commands/files to their purposes and "brand colors".
5.  **Visual Logic**: Include a Mermaid.js algorithm tree to map the core logic.
6.  **Session Memory Section**: Explicitly explain how to use `session-context.md` or similar for cross-chat persistence.
7.  **Release & Legal**:
    - **Pros & Cons Table**: Objective evaluation.
    - **Monetization & License**: Details on commercial vs free usage. Explicitly mention the **Student Verification** requirement (Institutional email/ID) for academic users.
    - **Data Privacy**: Mention that sensitive files like `MARKET_EVALUATION.md` and `PROJECT_METADATA.md` are protected via `.gitignore`.

## Design Principles
- **Rich Aesthetics**: Use emojis, horizontal rules, and alignment divs.
- **No Placeholders**: If an image is needed, suggest a prompt for `generate_image`.
- **Clarity first**: Use bolding for key terms.

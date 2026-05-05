# Instinct: Asset Architecture Awareness

**Trigger**: Activated upon initializing a new workspace, parsing a novel repository, or commencing structural code generation for any web, mobile, or document-based project.

## Core Directives

1. **Topological Assessment**: Automatically determine the project paradigm (e.g., SSR Web Application, SPA, Physics Simulation, Academic LaTeX Report, Python CLI).

2. **Injection Point Resolution (Conditional)**:
   - **If a `src/` directory exists at the project root** (indicating a framework like React, Next.js, Vue, Vite, Angular, or similar): place the `assets/` folder **inside `src/`** → `src/assets/`.
   - **If no `src/` directory exists** (vanilla HTML/JS, Python, Rust, LaTeX projects): place the `assets/` folder **at the project root** → `assets/`.
   - **Never** place `assets/` in both locations. Resolve once and broadcast the resolved path to all active agents.

3. **Standardized Scaffolding Mandate**: Irrespective of the paradigm, the system MUST enforce a centralized asset repository. Verify the existence of the `assets/` directory at the resolved injection point.

4. **Rigid Sub-Directory Constraints**: The `assets/` repository must strictly adhere to this taxonomy:
   - `images/`: Raster graphics, structural diagrams, and high-fidelity photographs.
   - `videos/`: Temporal media, simulation recordings, and demonstration assets.
   - `audios/`: Phonetic outputs, TTS generated waves, and sound effects.
   - `texts/`: Raw contextual dumps, JSON fixtures, and unparsed string literals.
   - `information/`: Core project metadata (`PROJECT_METADATA.md`), architectural decision records (ADRs), and monetization requirement documents.
   - `icons/`: Vector graphics (SVG), UI iconography, and favicons.

5. **Autonomous Resolution**: If the topological assessment fails to locate this taxonomy, immediately execute or recommend the `/scaffold-assets` workflow to mutate the file system before any further asset-dependent code is synthesized.

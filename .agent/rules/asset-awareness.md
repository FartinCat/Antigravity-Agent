# Instinct: Asset Architecture Awareness

**Trigger**: Activated upon initializing a new workspace, parsing a novel repository, or commencing structural code generation for any web, mobile, or document-based project.

## Core Directives

1. **Topological Assessment**: Automatically determine the project paradigm (e.g., SSR Web Application, SPA, Physics Simulation, Academic LaTeX Report).
2. **Standardized Scaffolding Mandate**: Irrespective of the paradigm, the system MUST enforce a centralized asset repository. Verify the existence of an `assets/` directory at the project root or the primary `src/` boundary.
3. **Rigid Sub-Directory Constraints**: The `assets/` repository must strictly adhere to the following taxonomy to ensure deterministic asset resolution:
    - `images/`: Raster graphics, structural diagrams, and high-fidelity photographs.
    - `videos/`: Temporal media, simulation recordings, and demonstration assets.
    - `audios/`: Phonetic outputs, TTS generated waves, and sound effects.
    - `texts/`: Raw contextual dumps, JSON fixtures, and unparsed string literals.
    - `information/`: Core project metadata, architectural decision records (ADRs), and monetization requirement documents.
    - `icons/`: Vector graphics (SVG), UI iconography, and favicons.
4. **Autonomous Resolution**: If the topological assessment fails to locate this exact taxonomy, immediately execute or recommend the `/scaffold-assets` workflow to mutate the file system before any further asset-dependent code is synthesized.

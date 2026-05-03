---
description: Automatically scaffolds the rigorous, standardized assets/ directory taxonomy required for professional project management.
---

# Workflow: Scaffold Asset Taxonomy

**Objective**: Programmatically enforce a standardized resource organization matrix across all project paradigms to ensure deterministic asset resolution and maintain architectural purity.

## Execution Sequence

1. **Root Resolution**: Dynamically identify the optimal injection point for the asset matrix (preferencing the project root or the primary framework `src/` directory).
2. **Taxonomy Generation**: Execute recursive directory creation for the following rigid structure:
   - `assets/images/`
   - `assets/videos/`
   - `assets/audios/`
   - `assets/texts/`
   - `assets/information/`
   - `assets/icons/`
3. **Metadata Initialization**: Seed the `assets/information/` directory with a standardized `PROJECT_METADATA.md` or `.gitkeep` to establish a persistent state for the `market-evaluator` and `commercial-license` agents to read from.
4. **Path Resolution Update**: Broadcast an internal state update to all active agents, ensuring all synthesized code (HTML, React, LaTeX, Python) uses the newly established relative paths for asset linking.

## Invocation Parameters
- Can be invoked manually via the UI command `/scaffold-assets`.
- Invoked autonomously by the `asset-awareness` instinct when structural non-compliance is detected.

---
name: market-evaluator
description: Evaluates the codebase and features against user requirements to estimate future market value and suggest commercial pricing tiers.
origin: Custom Ensemble
---

# Market Value Evaluator

Analyze the commercial viability, complexity, and feature completeness of the current repository to help the author secure funding and price the software appropriately.

## When to Activate

- Following a `deep-scan` on a mature project.
- Before generating a `commercial-license`.
- When the user asks for a project audit or monetization advice.

## Core Rules

1. **Objective Valuation**: Assess the codebase complexity (lines of code, advanced algorithms, UI polish via `web-aesthetics`). Higher complexity and polish justify higher commercial fees.
2. **Requirement Alignment**: Cross-reference the built product with the original user requirements (found in the `Plan/` folder or `assets/information/`). Identify missing features that could increase market value.
3. **Pricing Strategy**: Suggest tiered pricing models (e.g., Enterprise, Startup, Independent Contractor) based on the utility of the software.
4. **Funding Focus**: Always frame the evaluation from the perspective of securing funding for a student developer. Highlight unique selling points (USPs) that can be pitched to investors or clients.
5. **Data Sensitivity**: The resulting evaluation report contains sensitive commercial strategy. Ensure the generated `MARKET_EVALUATION.md` is added to `.gitignore` to prevent public leakage.

## Evaluation Workflow

1. **Ingest State**: Trigger `deep-scan` to understand the full scope of the project.
2. **Feature Mapping**: List all core functionalities.
3. **Market Comparison**: Compare the functionalities against standard market offerings (e.g., "This simulation tool offers features similar to premium academic software").
4. **Output Report**: Generate a `MARKET_EVALUATION.md` file detailing:
    - Codebase Complexity Score
    - Feature Completeness vs Requirements
    - Suggested Commercial License Fees
    - Pitch Summary for Funding

## Banned Patterns

- Do not suggest making the core product completely free/open-source without a monetization hook.
- Avoid vague evaluations. Provide concrete, justifiable estimates and actionable steps to increase value.

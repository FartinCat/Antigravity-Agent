---
name: commercial-license
description: Generates a custom LICENSE.md enforcing commercial fees and validation-based contributor access.
origin: Custom Ensemble
---

# Commercial License Generator

Generate rigorous, legally sound licensing files that protect the author's financial interests while encouraging validated open-source contribution.

## When to Activate

- When finalizing a repository for public release.
- When requested to "add a license" or "generate terms of use".
- Before deploying a market-evaluated product.

## Core Rules

1. **No Charity**: The license must explicitly prohibit free commercial usage. Any commercial deployment, distribution, or monetization by a third party requires a paid fee.
2. **Contributor Tier**: Individuals who actively contribute to the codebase (via accepted Pull Requests or significant bug fixes) may be granted free personal or commercial use, **strictly upon written validation by the author**.
3. **Personal Use**: Academic or personal usage is free, but redistribution without credit is prohibited.
4. **Clarity**: The terms must be plainly written without excessive legal jargon, so users immediately understand they must pay for commercial use.

## Generation Workflow

1. **Project Identification**: Determine the name of the project and the author's name (from `.agent/information/` or repository metadata).
2. **Drafting Terms**: 
    - Section 1: Personal/Academic Use (Free)
    - Section 2: Contributor Access (Free, pending author validation)
    - Section 3: Commercial Use (Fee required, link to contact/payment)
3. **File Creation**: Generate the `LICENSE.md` file in the root directory.

## Banned Patterns

- Never generate a standard MIT, Apache, or GPL license. These do not fit the strict commercial fee and validation requirements.
- Do not make the contribution validation automatic. It must state "pending explicit validation by the original author."

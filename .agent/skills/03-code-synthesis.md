# Code Synthesis Logic (Advanced)

This skill provides the algorithmic logic for the `04-synthesizer` agent to merge disparate AI perspectives (e.g., plans from Claude, DeepSeek, GPT-4o) into a single authoritative `MASTER_PLAN.md`.

## 1. Weighted Perspective Analysis
Not all AI plans are equal. The synthesizer must apply weights based on known model strengths:
- **Claude 4.6 Sonnet**: Highest weight for **Architecture and UI Aesthetics**.
- **DeepSeek V3 / R1**: Highest weight for **Algorithmic Logic and Optimization**.
- **GPT-4o**: Highest weight for **Third-Party Integrations and Documentation**.
- **Gemini 3.0 Pro**: Highest weight for **Creative Content Generation**.
- **Perplexity 4**: Highest weight for **Research and Analysis**.

**Synthesis Rule**: If Plan A (Claude) and Plan B (DeepSeek) conflict on a database choice, the Synthesizer must evaluate the choice against `02-architectural-design.md` mandates first. If still tied, the model with the higher weight for that specific domain wins.

## 2. Semantic Reconciliation Protocol
When merging plans, the Synthesizer must ensure naming and contract consistency:
- **Contract Mapping**: Ensure that "UserObject" in the Backend plan perfectly matches the "UserEntity" in the Frontend plan.
- **Naming Standardization**: Force all plans into the project's standard casing (e.g., `camelCase` for JS, `snake_case` for Python).
- **API Alignment**: Verify that the endpoints proposed in the Backend plan are exactly what the Frontend plan expects to call.

## 3. Conflict Resolution Decision Tree
1. **Repository Awareness**: Does the current code already have an established pattern? (Precedence: 100%).
2. **Foundational Mandates**: Does the choice violate `02-architectural-design.md` or `07-core.md`? (Precedence: 90%).
3. **Performance Metric**: Which approach has lower complexity (O-notation) or fewer dependencies? (Precedence: 80%).
4. **Majority Rule**: If three plans suggest "Library X" and one suggests "Library Y," follow the majority unless it violates Step 2.

## 4. Integration Regression Checking
Before finalizing the `MASTER_PLAN.md`, the agent must simulate the integration:
- **Dependency Hell Check**: Detect if Plan A's libraries are incompatible with Plan B's (e.g., mismatched React versions).
- **Environmental Drift**: Ensure all plans assume the same OS (WSL/Windows) and environment variables.
- **Side-Effect Analysis**: Flag if Plan A's data cleanup script might accidentally wipe data required by Plan B's analytical service.

## 5. Master Output Structure
The final `MASTER_PLAN.md` must be more than a list; it must be a **DAG (Directed Acyclic Graph)** of tasks:
- **Prerequisites**: Clear list of what must be installed before Step 1.
- **Critical Path**: Identification of the "Bottleneck" features that must be built first.
- **Verification Plan**: A specific test case for every phase to ensure the synthesis holds together during execution.

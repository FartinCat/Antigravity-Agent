# Instinct: Silent Ingest

**Trigger**: When the user provides bulk text, conversation history, or explicitly says "understand and keep quiet."

## Rules
1. **Minimize Output**: Acknowledge receipt with a brief message or a single emoji (e.g., "Understood. Context absorbed. 🧠").
2. **Deep Comparison**: Immediately analyze the provided text against the current directory structure and existing codebases.
3. **Internal Indexing**: Silently map out dependencies, variables, and logic flow described in the text for future reference.
4. **Hold Action**: Do not initiate code changes or ask clarifying questions unless the text is critically incomplete or the user prompts for the "Next Step."
5. **Observation Mode**: Stay in "observation mode" until the user asks for synthesis or implementation.

# 🔍 Scanner Workflow

This workflow is designed to give you a comprehensive overview of the repository's current state, recent changes, and how to use key components effectively. It minimizes confusion by providing direct, precise context.

## 📋 Execution Sequence

### Phase 1: Deep Awareness
Use the **Deep-Scan Agent** to map the entire repository. This ensures the system has the latest file tree and structural context.
- **Agent**: `/deep-scan`
- **Task**: "Perform a full repository scan and provide a summarized file tree. Identify the core components of the project."

### Phase 2: Change Analysis
Identify what has changed recently. This helps in understanding the project's current trajectory.
- **Agent**: `/ask`
- **Task**: "Analyze the recently modified files and summarize the changes. Check the `PROJECT_METADATA.md` and `.agent/session-context.md` for recent updates."

### Phase 3: Effective Usage Guide
Provide specific instructions on how to use system-level files that might be confusing.
- **Agent**: `/ask`
- **Task**: "Explain how to use `session-context.md` for session persistence. Also, clarify the role of `PROJECT_METADATA.md` and how to update it."

### Phase 4: Doubt Resolution
Address any remaining doubts the user might have about the codebase.
- **Agent**: `/ask`
- **Task**: "Based on the scan and change analysis, what are the most important things I should know before I start coding? Answer concisely."

---

## 💾 Session Context Tip
Always remember to update `.agent/session-context.md` after a major change. This file acts as the "long-term memory" for your agents. When starting a new chat, paste its contents to resume perfectly.

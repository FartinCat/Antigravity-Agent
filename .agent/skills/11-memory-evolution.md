# Memory Evolution Protocol

This skill defines the three-tier memory system and the evolution logic that promotes patterns from session memory → project memory → global memory.

## Memory Tiers

### Tier 1: Session Memory (Ephemeral)
- Stored in: `.agent/session-context.md`
- Lifecycle: Written at session close, distilled into Tier 2 at end of session
- Contains: Tasks attempted, succeeded, failed, with root causes

### Tier 2: Project Memory (Per-Repository)
- Stored in: `.agent/project_memory/{repo_name}.md` (future)
- Currently approximated by: session-context.md history entries
- Contains: Architecture decisions, known quirks, recurring bugs, team conventions

### Tier 3: Global Memory (Universal)
- Stored in: `.agent/global_memory.md` (future)
- Contains: Anti-patterns and best practices that apply across all projects in all languages

## Evolution Protocol (End of Session)

### Step 1: Failure Harvest
For each failed task this session:
1. Extract root cause
2. Check if a matching anti-pattern exists in memory
3. If YES: increment times_triggered, raise confidence
4. If NO: create new anti-pattern entry at confidence 0.70

### Step 2: Success Reinforcement
For each succeeded task:
1. Identify which skills were applied
2. For each applied skill: increment times_validated, adjust confidence toward 0.99

### Step 3: Skill Decay (Every 50 sessions)
- Skills with confidence < 0.40 after 10+ applications → archive
- Skills never triggered in 50+ sessions → move to watch list
- Skills with confidence > 0.95 and 20+ validations → promote to higher tier

### Step 4: Human Feedback Integration
When a human overrides an agent action:
1. Capture the diff of the human correction
2. Generalize the fix pattern
3. Create a candidate skill with confidence = 0.85
4. Associate it with the triggered instincts that preceded the mistake

## Skill Distillation (Macro-Skills)
Every 50 sessions, check for skill pairs frequently applied together:
- Draft a Macro-Skill combining both
- Test against historical failures
- If effective: promote; if not: discard

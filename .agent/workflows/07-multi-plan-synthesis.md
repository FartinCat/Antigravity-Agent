---

title: "MULTI PLAN SYNTHESIS"

description: "Merge competing AI strategies into one plan."

order: 4

---



# Workflow: Multi-Plan Synthesis







**Objective**: Convert multiple external AI perspectives into a single, optimized, conflict-free implementation file.







## Steps







1. **Detection**: Check for the existence of a `Plan/` folder in the project root directory. If it does not exist, halt and instruct the user to create it and populate it with plan files (e.g., `planbychatgpt.txt`, `planbyclaude.txt`, `planbygrok.txt`). The `Plan/` folder must be at project root, NOT inside `.agent/`.







2. **Scanner**: Invoke `/scanner` to capture the current true state of the project before comparing plans. The scanner output (excluding `.agent/`) becomes the ground truth for reconciliation.







3. **Ingestion**: Read all files inside `Plan/`. Log how many files were found and their names.







4. **Synthesis (Synthesizer Agent)**:



   - Compare strategies from each file.



   - Resolve contradictions by checking actual project resources from the scanner output.



   - Select the most robust, performance-oriented, and bug-free approach for each component.



   - Log every conflict found and the resolution ruling.







5. **Output**: Create `MASTER_PLAN.md` at the project root with the full structured plan, conflict log, and phase breakdown.







6. **Validation**: Run a final check to ensure the plan covers all user requirements and adheres to `01-core.md` instincts.







7. **Session Log**: Append a session entry to `.agent/session-context.md` confirming synthesis complete and recording which plans were merged.







## Primary Agent



- `.agent/.agents/skills/04-synthesizer`







## Dependent Skills



- `.agent/.agents/skills/01-deep-scan` (invoked via /scanner — must run before synthesis)



- `.agent/skills/05-code-synthesis.md` (conflict resolution logic)





## Output Organization (Rule 20)
1. Check if `docs/master-plans` exists, create if not.
2. Count existing files.
3. Output report to `docs/master-plans/MASTER_PLAN_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.


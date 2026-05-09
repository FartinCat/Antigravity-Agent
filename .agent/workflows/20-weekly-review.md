---

title: "WEEKLY REVIEW"

description: "Strategic audit of project progress/health."

order: 20

---



# Workflow: Weekly Review



Trigger: /weekly-review, or "do my weekly review"



Steps:

1. Read session-context.md for week's activity log

2. Search memory for notes from the week

3. Generate: accomplished / left undone / lessons learned

4. Plan: top 3 priorities for next week

5. Archive: copy this week's session-context.md to .agent/archive/week-{date}.md

6. Reset session-context.md with next week's focus areas



Output: WEEKLY_REVIEW_{date}.md in project root





## Output Organization (Rule 20)
1. Check if `docs/weekly-reviews` exists, create if not.
2. Count existing files.
3. Output report to `docs/weekly-reviews/WEEKLY_REVIEW_{date}.md` (increment NN zero-padded).
4. NEVER output to project root.


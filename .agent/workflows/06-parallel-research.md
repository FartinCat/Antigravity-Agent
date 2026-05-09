---

title: "PARALLEL RESEARCH"

description: "Simultaneous research on multiple technical paths."

order: 06

---



# Workflow: Parallel Research



Trigger: /research [topic], or "research X for me"



Steps:

1. Decompose topic into 3-5 research angles

2. For each angle: fetch MCP → extract findings (script, not raw HTML)

3. Identify: key facts, competing viewpoints, expert consensus, open questions

4. Synthesize: executive summary (3 paragraphs) + detailed breakdown per angle

5. Note confidence levels and areas of uncertainty

6. Store findings in memory if they'll be reused



Output: RESEARCH_{topic}_{date}.md with citations





## Output Organization (Rule 20)
1. Check if `docs/research` exists, create if not.
2. Count existing files.
3. Output report to `docs/research/RESEARCH_{topic}_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.


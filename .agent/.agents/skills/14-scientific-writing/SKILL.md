---
name: scientific-writing
description: Specialized rules for writing physics dissertations, academic reports, and LaTeX formatting. Ensures a rigorous, objective, and consistent scientific tone.
origin: Custom Ensemble
---

# Scientific Writing & LaTeX Formatting

Write rigorous, objective, and well-structured academic content, specifically tailored for Physics dissertations and scientific reports.

## When to Activate

- Drafting or revising chapters of a dissertation (e.g., Literature Review, Methodology).
- Formatting complex tables and figures in LaTeX.
- Synthesizing research data into formal text.
- Standardizing citations and bibliography formatting.
- Ensuring consistent scientific tone across multiple documents.

## Core Rules

1. **Objective Tone**: Always use the third person ("The experiment demonstrated..." not "We showed..."). Maintain an objective and detached voice.
2. **Precision**: Use specific, quantifiable data over qualitative descriptors. Avoid subjective adjectives (e.g., use "a 50nm increase" instead of "a huge increase").
3. **LaTeX Integrity**: When providing code, ensure exact LaTeX syntax. Always use appropriate math modes (`$...$`, `\begin{equation}`) for variables.
4. **Active over Passive**: Prefer active voice when describing methodology, unless passive voice is strictly required to emphasize the object of the experiment.
5. **Contextual Flow**: Each paragraph must begin with a clear topic sentence and transition logically to the next. Lead with the physical principle or result, then explain.

## Voice Capture Workflow

When continuing a dissertation or report:
1. **Analyze Existing Content**: Read prior sections (e.g., the Bismuth Oxytelluride report) to capture sentence length, vocabulary complexity, and formatting habits.
2. **Notation Matching**: Identify the specific nomenclature used (e.g., whether to use $Bi_2O_2Te$ or spelling it out).
3. **Citation Style**: Confirm the numbering and format of citations (e.g., sequential numerical `[1]`, `[2]`).

## Banned Patterns

Delete and rewrite any of these:
- Overly flowery or dramatic language (e.g., "In a groundbreaking discovery...").
- Filler transitions such as "It is interesting to note that..." or "Basically".
- Imprecise language like "very," "quite," "a lot."
- First-person pronouns ("I", "we", "our") unless specifically asked to write a personal reflection.
- "In this paper we will..." (use "This paper presents..." instead).

## LaTeX Implementation Patterns

### Figures
```latex
% GOOD: Floating figure with clear placement rules and caption
\begin{figure}[H] % or [htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/crystal_structure.png}
    \caption{Crystal structure of Bi$_2$O$_2$Te showing layered orientation.}
    \label{fig:crystal_structure}
\end{figure}
```

### Tables
```latex
% GOOD: Using booktabs for professional academic tables without vertical lines
\begin{table}[htbp]
    \centering
    \caption{Comparison of Synthesis Methods}
    \label{tab:synthesis}
    \begin{tabular}{llc}
        \toprule
        Method & Precursor & Temperature ($^\circ$C) \\
        \midrule
        Hydrothermal & Bi(NO$_3$)$_3$ & 180 \\
        Solid State & Bi$_2$O$_3$ & 500 \\
        \bottomrule
    \end{tabular}
\end{table}
```

## Scientific Writing Checklist

Before finalizing any section:
- [ ] Tone is strictly objective and formal.
- [ ] No banned filler words or subjective adjectives are present.
- [ ] All variables and equations are correctly enclosed in LaTeX math mode.
- [ ] Figures and tables have descriptive captions and are referenced in the text.
- [ ] Citations follow a strictly sequential numerical order if compiling the final draft.
- [ ] Paragraphs flow logically and focus on concrete physical principles or data.
\n## Advanced Operations Matrix\n\n- **Database Interaction**: Use appropriate client libraries (e.g., sqlite3 for SQLite, psycopg2 for PostgreSQL, mysql-connector-python for MySQL) with parameterized queries to prevent injection.\n- **Simulation & Modeling**: For scientific simulations, employ 
umpy, scipy, or pandas for data handling, and matplotlib or plotly for visualizations.\n- **Performance Profiling**: Run python -m cProfile or 	imeit to benchmark critical sections.\n- **Precise Explanation**: Include step‑by‑step rationale in markdown code comments and a short summary in plain text.\n- **Error Handling**: Wrap external calls in try/except blocks, log errors with context, and re‑raise if unrecoverable.\n

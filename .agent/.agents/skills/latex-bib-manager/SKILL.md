---
name: latex-bib-manager
description: Automatically manages LaTeX bibliographies, enforces strictly sequential citation numbering ([1], [2]...), cleans .bib entries, and stabilizes figure floats.
origin: Custom Ensemble
---

# LaTeX Bibliography & Float Management

Maintain strict, error-free formatting for academic LaTeX documents, ensuring that citations compile sequentially and floats (figures/tables) remain anchored where expected.

## When to Activate

- Compiling a final or draft dissertation PDF.
- Fixing "citation out of order" errors.
- Adding a large batch of references to a `.bib` file.
- Resolving floating figures that appear on the wrong page (e.g., Chapter 1 figures appearing in Chapter 2).

## Core Rules

1. **Sequential Citations**: Citations in the text *must* appear in strictly ascending numerical order (e.g., the first cited source is [1], the second is [2], regardless of alphabetical author ordering).
2. **BibTeX Cleanup**: Ensure all `.bib` entries have complete fields (author, title, journal, year, volume, pages, doi). Remove unused or duplicate entries.
3. **Float Anchoring**: Use the `[H]` float specifier (from the `float` package) when a figure absolutely must not move, or enforce `\clearpage` at the end of chapters to flush pending floats.
4. **Git Ignore**: Never commit `.aux`, `.log`, `.toc`, `.bbl`, or `.blg` files. Ensure they are in `.gitignore`.

## Workflow Checklist

1. **Check Compiler**: Confirm whether the project uses `pdflatex`, `bibtex`, or `biber`/`biblatex`.
2. **Sort Citations**: If using `biblatex`, ensure the style is set to `numeric-comp` or similar sorting configuration (`sorting=none` ensures they appear in order of citation). If using standard `bibtex`, ensure the `.bst` style supports sequential numbering (e.g., `unsrt`).
3. **Clean .bib**: Scan the bibliography file and standardize capitalization (protecting proper nouns with `{Brackets}`).
4. **Fix Overflows**: If a table or figure overflows the page width, suggest using `tabularx` or resizing the `\includegraphics`.

## Banned Patterns

- Do not use alphabetical citation sorting (`plain.bst`) if sequential is requested.
- Do not use `\begin{center}` inside a `figure` environment; use `\centering`.
- Do not let floats cross chapter boundaries.

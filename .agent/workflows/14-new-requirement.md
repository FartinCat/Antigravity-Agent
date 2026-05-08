---
title: "NEW REQUIREMENT"
description: "Workflow 14 - NEW REQUIREMENT"
order: 14
---

# Workflow: New Requirement

Guide me through adding a new feature, from requirements documentation to implementation readiness.

1. **Capture Requirement** â€” If not already provided, ask for: feature name (kebab-case, e.g., `user-authentication`), what problem it solves and who will use it, and key user stories.
2. **Use Memory for Context** â€” Before asking repetitive clarification questions, search memory for related decisions or conventions via `npx ai-devkit@latest memory search --query "<feature/topic>"` and reuse relevant context.
3. **Create Feature Documentation Structure** â€” Copy each template's content (preserving YAML frontmatter and section headings) into feature-specific files:
   - `docs/ai/requirements/README.md` â†’ `docs/ai/requirements/feature-{name}.md`
   - `docs/ai/design/README.md` â†’ `docs/ai/design/feature-{name}.md`
   - `docs/ai/planning/README.md` â†’ `docs/ai/planning/feature-{name}.md`
   - `docs/ai/implementation/README.md` â†’ `docs/ai/implementation/feature-{name}.md`
   - `docs/ai/testing/README.md` â†’ `docs/ai/testing/feature-{name}.md`
4. **Requirements Phase** â€” Fill out `docs/ai/requirements/feature-{name}.md`: problem statement, goals/non-goals, user stories, success criteria, constraints, open questions.
5. **Design Phase** â€” Fill out `docs/ai/design/feature-{name}.md`: architecture changes, data models, API/interfaces, components, design decisions, security and performance considerations.
6. **Planning Phase** â€” Fill out `docs/ai/planning/feature-{name}.md`: task breakdown with subtasks, dependencies, effort estimates, implementation order, risks.
7. **Store Reusable Knowledge** â€” When important conventions or decisions are finalized, store them via `npx ai-devkit@latest memory store --title "<title>" --content "<knowledge>" --tags "<tags>"`.
8. **Next Command Guidance** â€” Run `/review-requirements` first, then `/review-design`. If both pass, continue with `/execute-plan`.

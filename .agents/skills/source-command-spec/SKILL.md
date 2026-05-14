---
name: "source-command-spec"
description: "Start spec-driven development — write a structured specification before writing any code"
---

# source-command-spec

Use this skill when the user asks to run the migrated source command `spec`.

## Command Template

Invoke the Antigravity spec-driven-development workflow.

Surface assumptions IMMEDIATELY before writing spec content:
"ASSUMPTIONS I'M MAKING: [list] → Correct me now or I'll proceed with these."

Then write a spec document covering six core areas:

1. **Objective** — what, why, who, success criteria
2. **Commands** — full executable commands with flags (build, test, lint, dev)
3. **Project Structure** — directory layout with descriptions
4. **Code Style** — one real code snippet showing style beats paragraphs describing it
5. **Testing Strategy** — framework, test locations, coverage expectations
6. **Boundaries** — Always do / Ask first / Never do

Save as `SPEC.md` in project root. Confirm with user before proceeding to `/plan`.

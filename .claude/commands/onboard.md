---
description: First-contact project analysis — run this on any new project
---

Invoke workflow `02-onboard.md`.

Steps:
1. Run `/scanner` first — full repository mapping
2. Health checks: tests passing? Build working? CI configured?
3. Stack detection: languages, frameworks, package managers
4. Identify: entry points, test directories, config files, potential issues
5. Create `SCAN_REPORT.md`
6. Update **`AETHER.md` Section 18** with project context

**Rule:** Always run `/scanner` before `/onboard`. Always onboard before building.

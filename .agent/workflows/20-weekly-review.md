# Workflow: Weekly Review

**Objective**: Conduct a structured strategic audit of project health, progress, and trajectory. This is the retrospective heartbeat — run weekly to catch drift, celebrate wins, and course-correct before problems compound.

## Trigger Conditions
- End of work week or sprint
- User says "weekly review" or "how are we doing?"
- Invoked via `/weekly-review`

## Execution Sequence

### Phase 1 — Data Collection (Automated)
1. **Git Activity**: Run `git log --oneline --since="7 days ago"` to capture all commits.
2. **File Churn**: Run `git diff --stat HEAD~20` (or equivalent) to identify hotspots.
3. **Open Issues**: Count TODO/FIXME/HACK comments in the codebase: `grep -rn "TODO\|FIXME\|HACK" --include="*.md" --include="*.py" --include="*.js" --include="*.ts" .`
4. **Test Health**: Run the test suite and capture pass/fail/skip counts.
5. **Registry Health**: Run `python .agent/scripts/sync_registry.py --no-bump` and capture the health status.
6. **Session Context**: Read `.agent/session-context.md` for the week's session entries.

### Phase 2 — Analysis
1. **Velocity Assessment**: How many tasks/features were completed vs. planned?
2. **Quality Assessment**:
   - Test coverage trend (improving/declining/stable)
   - Bug count trend (new bugs introduced vs. bugs fixed)
   - Technical debt trend (TODO count change from last review)
3. **Architecture Assessment**:
   - Are files growing too large? (flag any file > 500 lines)
   - Are there circular dependencies forming?
   - Is the module structure still clean?
4. **Risk Identification**:
   - Stalled work (files modified but not committed for > 3 days)
   - Scope creep signals (new files created outside the plan)
   - Dependency concerns (outdated packages, security advisories)

### Phase 3 — Scoring
Rate each dimension on a 1-5 scale:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Velocity | ?/5 | [commits this week vs. target] |
| Quality | ?/5 | [test pass rate, bug trend] |
| Architecture | ?/5 | [file sizes, modularity] |
| Documentation | ?/5 | [README accuracy, comment density] |
| Momentum | ?/5 | [consistent daily commits vs. burst patterns] |

**Overall Health**: Average of all dimensions → RED (< 2.5) / YELLOW (2.5-3.5) / GREEN (> 3.5)

### Phase 4 — Recommendations
1. **Top 3 Wins**: What went well this week? Celebrate explicitly.
2. **Top 3 Concerns**: What needs attention before next week?
3. **Action Items**: 1-3 specific tasks for next week, each with:
   - Owner (agent or user)
   - Priority (P0/P1/P2)
   - Estimated effort (hours)
4. **Decision Queue**: Any decisions that have been deferred and need resolution.

## Failure Paths
- **No Git History**: If the project has no commits this week, flag as "Stalled — no measurable progress" and recommend a planning session.
- **No Tests**: If no test suite exists, recommend setting one up as the P0 action item.
- **First Review**: If this is the first weekly review, skip trend analysis and establish the baseline.

## Output Format
```markdown
# Weekly Review — [Date Range]

## Health Dashboard
| Dimension | Score | Trend |
|-----------|-------|-------|
| Velocity | ⭐⭐⭐⭐ | ↑ |
| Quality | ⭐⭐⭐ | → |
| Architecture | ⭐⭐⭐⭐ | → |
| Documentation | ⭐⭐ | ↓ |
| Momentum | ⭐⭐⭐⭐⭐ | ↑ |
| **Overall** | **GREEN** | |

## Wins
1. [win]
2. [win]
3. [win]

## Concerns
1. [concern + recommended action]
2. [concern + recommended action]

## Next Week Action Items
- [ ] P0: [task] — [owner] — [effort]
- [ ] P1: [task] — [owner] — [effort]
- [ ] P2: [task] — [owner] — [effort]

## Registry Health
[output from sync_registry.py --no-bump]
```

## Output Organization (Rule 20)
Save to `docs/reviews/WEEKLY_REVIEW_{YYYY-MM-DD}.md`.

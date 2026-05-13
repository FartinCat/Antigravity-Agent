# Workflow: Parallel Research

**Objective**: Execute simultaneous research across multiple technical paths, then synthesize findings into a unified comparison matrix. Use when evaluating competing technologies, frameworks, libraries, or architectural patterns.

## Trigger Conditions
- User asks to compare technologies or approaches
- User says "research options for..."
- Planning phase reveals multiple viable paths
- Invoked via `/parallel-research`

## Execution Sequence

### Phase 1 — Research Scoping
1. **Define Research Axes**: Identify 2-5 distinct paths to investigate (e.g., "React vs Vue vs Svelte").
2. **Define Evaluation Criteria**: Establish 4-6 comparison dimensions relevant to the project:
   - Performance characteristics (bundle size, runtime speed, memory)
   - Developer experience (learning curve, documentation quality, tooling)
   - Ecosystem maturity (community size, plugin availability, corporate backing)
   - Project fit (compatibility with existing stack, migration cost)
3. **Set Boundaries**: Each research path gets a fixed scope — no rabbit holes.

**Gate**: Confirm research paths and criteria with user before proceeding.

### Phase 2 — Parallel Investigation
For EACH research path, execute simultaneously:

1. **Primary Source Review**: Read official documentation, changelog, and getting-started guides.
2. **Benchmark Discovery**: Find existing benchmarks, performance comparisons, and case studies.
3. **Ecosystem Scan**: Check package manager stats (npm downloads, GitHub stars/issues ratio, release cadence).
4. **Risk Assessment**: Identify dealbreakers — license issues, abandonment signals, breaking change history.
5. **Code Sample**: Write a minimal proof-of-concept (< 50 lines) demonstrating the core use case.

### Phase 3 — Synthesis
1. **Build Comparison Matrix**: Create a markdown table with all paths as columns and criteria as rows.
2. **Score Each Path**: Rate 1-5 on each criterion with brief justification.
3. **Calculate Weighted Totals**: Apply project-specific weights to criteria.
4. **Identify Clear Winner**: If scores are within 10%, flag as "toss-up" and recommend based on team familiarity.

### Phase 4 — Recommendation
1. **Primary Recommendation**: State the winning path with confidence level (High/Medium/Low).
2. **Runner-Up**: Explain when the second choice would be better.
3. **Migration Path**: If switching from an existing solution, outline the migration steps.
4. **Risk Disclosure**: List any concerns that could invalidate the recommendation.

## Failure Paths
- **Insufficient Data**: If a path lacks benchmarks, mark as "Unverified" and note the gap.
- **Tie**: If paths are equivalent, recommend based on ecosystem momentum and team experience.
- **Dealbreaker Found**: If a path has a license or compatibility issue, eliminate it early and note why.

## Output Format
```markdown
# Parallel Research Report: [Topic]

## Research Paths
1. [Path A] — [one-line summary]
2. [Path B] — [one-line summary]

## Comparison Matrix
| Criterion (weight) | Path A | Path B | Path C |
|---|---|---|---|
| Performance (30%) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| DX (25%) | ... | ... | ... |

## Recommendation
**Winner**: [Path X] — Confidence: [High/Medium/Low]
**Rationale**: [2-3 sentences]

## Risks & Caveats
- [risk 1]
- [risk 2]
```

## Output Organization (Rule 20)
Save report to `docs/research/PARALLEL_RESEARCH_{NN}.md` (increment NN zero-padded).

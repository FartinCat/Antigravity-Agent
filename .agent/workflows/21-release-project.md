---

title: "RELEASE PROJECT"

description: "God Mode: License, README, Packaging."

order: 21

---



# Workflow: Release Project



**Objective**: Finalize a project for public consumption and monetization. This is the "God Mode" pipeline.



## Execution Sequence



1. **Auto-Cleanup**: Trigger the `09-archive-management.md` rule. The AI actively scans the project root for stray reference folders (`frontend1`, `app2`, etc.) and moves them into the `archived/` directory. **The `.agent/`, `.git/`, and `zip/` folders are NEVER moved.**



2. **Scanner**: Invoke `/scanner` to produce a final state-of-project report confirming cleanup was successful and the project root is clean.



3. **Evaluate**: Invoke `/market-evaluator` (Agent 17). Read root `PROJECT_METADATA.md` and the scanner output to determine codebase complexity and suggest commercial pricing tiers.



4. **License**: Invoke `/commercial-license` (Agent 18). Generate a custom `LICENSE.md` prohibiting free commercial use.



5. **Document**: Invoke `/readme-architect` (Agent 16) to build the final premium `README.md`.



6. **Version Bump**: Invoke `10-semantic-versioning.md` to finalize the release version (read current version from `PROJECT_METADATA.md` and bump accordingly) in root `PROJECT_METADATA.md`.



7. **Packaging**: Trigger `14-release-packaging.md`. Migrate any existing zip files to `archived/old-versions/`, and generate a new versioned ZIP archive of the `.agent/` folder and key documentation in the `archived/current-version/` directory.



8. **Log**: Append a release entry to `.agent/session-context.md` with the release version and date.



9. **Validate**: Run `/cross-agent-validator` to confirm all release artifacts (License, Readme, Market Eval, Zip) are present.





## Output Organization (Rule 20)
1. Check if `docs/market-evaluations` exists, create if not.
2. Count existing files.
3. Output report to `docs/market-evaluations/MARKET_EVALUATION_{NN}.md` (increment NN zero-padded).
4. NEVER output to project root.



### Step 10 — Registry Sync
Run `/sync-registry` before packaging to ensure perfect synchronization.


---

title: "AUTO COMMIT"

description: "Atomic, semantic commit generation loop."

order: 24

---



# Workflow: Auto-Commit Pipeline



**Objective**: Produce a structured list of atomic `git add` + `git commit` commands, presented in **separate, individual** copyable bash blocks for granular control.



## Execution Sequence



1. **State Capture**: Run `git status` and `git diff --stat`.

2. **Artifact Check**: Identify and exclude build artifacts.

3. **Diff Analysis**: Analyze each modified file's intent.

4. **Semantic Grouping**: Apply `12-commit-semantics.md` for atomic chunking.

5. **Continuous Auto-Versioning**: ENFORCE Rule `22-continuous-versioning.md`. If files were modified, bump version in **`AETHER.md`** (identity §1 + §14 Project Metadata) per patch/minor rules from the diff intent.

6. **Registry Sync**: Run `python .agent/scripts/sync_registry.py` to ripple the new version to `README.md`, `LICENSE.md`, `install-state.json`, and **`AETHER.md` §13**. 

7. **Message Generation**: Agent `19-git-commit-author` drafts messages per `11-git-awareness.md`.

8. **Output**: **CRITICAL: Present EACH commit inside its OWN separate triple-backtick bash block.** This allows the user to copy and run each commit individually.



## Output Format

**1/N — [Category]**
```bash
git add [files]
git commit -m "[prefix]: [message]"
```

**[Additional Commits...]**
```bash
git add [files]
git commit -m "[prefix]: [message]"
```

**N/N — Version bump (always last)**
```bash
git add AETHER.md .agent/aether-agent-install-state.json
git commit -m "chore(version): bump to v[X.Y.Z]"
```



## Primary Agent

- `.agent/.agents/skills/19-git-commit-author`




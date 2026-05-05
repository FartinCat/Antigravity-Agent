# Core Architectural Instincts

These are the unbreakable, fundamental directives that dictate the agent's baseline operational state. They supersede all other instructions.

1. **Deterministic Clarity**: Code synthesis must prioritize deterministic outcomes and high maintainability. Reject "clever" or obfuscated solutions. Opt for explicit, strictly-typed, and highly documented architectures.

2. **Zero-Trust Security**: Treat all inputs as hostile. Never synthesize code that exposes secrets, lacks parameter validation, or bypasses authentication layers.

3. **Strategic Pre-computation (Planning)**: Execute architectural planning before mutating any file. Ambiguity must be resolved via the `/planner` agent or `/multi-plan-synthesis` workflow before writing logic. (Note: The correct names are `/planner` for the single-agent planning skill and `/multi-plan-synthesis` for the full ensemble workflow. There is no `/plan` command.)

4. **Test-Driven Mandate**: Code is not complete without proof of correctness. Default to the `/tdd` workflow (Red-Green-Refactor via `/tdd-guide` agent) for all logic generation.

5. **Atomic Operations**: Deconstruct monolithic tasks into atomic, verifiable sub-tasks. Ensure each mutation leaves the system in a compiling, functional state.

6. **Agent Infrastructure Isolation**: The `.agent/` folder is the operating system of this project's AI toolchain. It is NEVER treated as project source code. It is excluded from all scans, diagnostics, tree reports, and anomaly detection. The only `.agent/` file ever read during a session is `session-context.md` for memory continuity.

7. **Session Memory**: Always check `.agent/session-context.md` at the start of every session. Always verify the `Project Directory:` field matches the current project folder before trusting the stored history.

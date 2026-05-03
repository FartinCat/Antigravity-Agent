# Core Architectural Instincts

These are the unbreakable, fundamental directives that dictate the agent's baseline operational state. They supercede all other instructions.

1. **Deterministic Clarity**: Code synthesis must prioritize deterministic outcomes and high maintainability. Reject "clever" or obfuscated solutions. Opt for explicit, strictly-typed, and highly documented architectures.
2. **Zero-Trust Security**: Treat all inputs as hostile. Never synthesize code that exposes secrets, lacks parameter validation, or bypasses authentication layers.
3. **Strategic Pre-computation (Planning)**: Execute architectural planning before mutating any file. Ambiguity must be resolved via the `/plan` or `/multi-plan-synthesis` workflows before writing logic.
4. **Test-Driven Mandate**: Code is not complete without proof of correctness. Default to the `/tdd` cycle (Red-Green-Refactor) for logic generation.
5. **Atomic Operations**: Deconstruct monolithic tasks into atomic, verifiable sub-tasks. Ensure each mutation leaves the system in a compiling, functional state.

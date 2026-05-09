Edited antigravity-agent-install-state.json
Edited AGENTS.md
Viewed CHANGELOG.md:1-33
Listed directory Antigravity%20Agent
Listed directory .agent
Listed directory workflows

The current directory is the **Antigravity Agent Ecosystem (v4.0.0)**, a portable Agentic Operating System (AOS). It is a production-ready infrastructure designed to be injected into any codebase to provide high-level autonomous orchestration.

### 📂 Directory Structure

The core of the system resides in the `.agent/` directory, which follows a rigid hierarchical structure:

*   **`.agent/`**: The "Central Nervous System" of the AOS.
    *   **`workflows/`**: 22 sequence-ordered pipelines (01–22) that handle the entire software lifecycle from scanning to automated release.
    *   **`instincts/`**: 5 probabilistic behavioral rules that guide agent actions implicitly (e.g., minimal footprint, verification-first).
    *   **`rules/`**: 15 governance rules (00–14) that enforce deterministic behavior and security.
    *   **`skills/`**: 21 foundational logic modules for complex reasoning (TDD, State Machines, Cognitive Load monitoring).
    *   **`mcps/`**: Documentation for 6 integrated MCP toolsets (21st-dev, Stitch, Figma, MongoDB, Playwright, Supabase).
    *   **`.agents/skills/`**: 22 specialized personas (agents) with specific YAML-defined capabilities.
*   **`.claude/`**: Platform-specific configuration and agent triggers.
*   **`.gemini/`**: System logs, scratch scripts, and internal memory buffers.
*   **`Root/`**: Registry and documentation files including `README.md`, `AGENTS.md`, and the `CHANGELOG.md`.

### ⚡ Current Capabilities

The ecosystem is now fully synchronized to **v4.0.0** with the following active capabilities:

1.  **Full Lifecycle Orchestration**: Automates projects across 5 phases:
    *   **P1 Awareness**: `/scanner`, `/onboard-project`, `/mcp-audit`.
    *   **P2 Strategy**: `/spec-discovery` (Rigid 6-pillar framework), `/multi-plan-synthesis`.
    *   **P3 Execution**: `/build-app`, `/feature-development`, `/tdd`.
    *   **P4 Quality**: `/debug-session`, `/fix-bugs`, `/quality-gate`.
    *   **P5 Finalization**: `/release-project`, `/auto-commit`.
2.  **Specialist Personas**: 22 deep-logic agents, including enterprise-grade **Code Reviewers**, **Security Auditors**, and **Test Engineers** with strict reporting templates.
3.  **MCP Integration**: Native support for external tools allowing for automated UI generation, DB management, browser testing, and design-to-code flows.
4.  **Governance Layer**: Rule 00 and 15 internal foundational skills ensure the agent never hallucinates, always verifies state before acting, and maintains a minimal footprint on your codebase.
5.  **Self-Mapping**: The ecosystem is self-aware; it can audit its own tools (`/mcp-audit`) and maintain its own versioning state across all registries.
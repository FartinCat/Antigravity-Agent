# Workflow: Build App

**Objective**: End-to-end pipeline for building a production-ready software application from specification through implementation to deployment readiness. Enforces architectural discipline, test coverage, and clean code practices.

## Trigger Conditions
- User wants to build a software application (CLI, API, desktop, mobile)
- User says "build an app for..." or "create a [type] application"
- Invoked via `/build-app`

## Execution Sequence

### Phase 1 — Architecture & Design
1. **Gather Requirements**: Identify:
   - Application type (CLI, REST API, desktop GUI, mobile, full-stack)
   - Core functionality (3-5 primary features)
   - Data model (entities, relationships, storage requirements)
   - External integrations (APIs, databases, auth providers)
   - Target platform and deployment environment
2. **Technology Selection**: Choose stack based on requirements:
   - **CLI Tool**: Python (argparse/click) or Node.js (commander)
   - **REST API**: Python (FastAPI/Flask) or Node.js (Express/Fastify)
   - **Desktop**: Electron, Tauri, or native framework
   - **Full-Stack**: Next.js, or separate frontend + API
3. **Architecture Decision**: Apply `04-architectural-design.md`:
   - Define module boundaries (hexagonal architecture preferred)
   - Identify ports and adapters
   - Plan the dependency injection strategy
   - Document data flow between modules
4. **Project Structure**: Define the directory layout before writing any code.

**Gate**: Confirm architecture, tech stack, and project structure with user.

### Phase 2 — Foundation
1. **Project Init**: Initialize with appropriate tooling:
   - Package manager setup (`npm init`, `pip init`, `cargo init`)
   - Linter and formatter configuration
   - Git initialization with `.gitignore`
2. **Core Abstractions**: Build the foundational layer first:
   - Configuration management (env vars, config files)
   - Logging framework
   - Error handling patterns (custom error types)
   - Database connection / data layer
3. **Entry Point**: Create the main entry point with graceful startup/shutdown.
4. **Test Infrastructure**: Set up test framework before writing any feature code:
   - Unit test runner configured
   - Integration test directory created
   - CI pipeline defined (if applicable)

### Phase 3 — Feature Development (Iterative)
For EACH feature, follow the `/feature-development` workflow (10-feature-development.md):

1. **Spec**: Define acceptance criteria for the feature.
2. **Test First**: Write failing tests for the feature (TDD when applicable).
3. **Implement**: Build the feature incrementally (< 50 lines per block).
4. **Verify**: Run tests, fix failures, confirm acceptance criteria.
5. **Commit**: Atomic commit per feature using `12-commit-semantics.md`.

Repeat for each feature in priority order. Features are built sequentially — never start feature N+1 before feature N passes all tests.

### Phase 4 — Integration & Hardening
1. **Integration Testing**: Test feature interactions:
   - API endpoint chain testing (create → read → update → delete)
   - Error propagation across module boundaries
   - Edge cases: empty inputs, max-length inputs, concurrent access
2. **Security Review**: Apply `15-security-engineering.md`:
   - Input validation on all entry points
   - Authentication/authorization checks
   - Secrets management (no hardcoded credentials)
   - Dependency vulnerability scan
3. **Performance Baseline**: Measure and document:
   - Response times for critical paths
   - Memory usage under load
   - Startup time
4. **Documentation**: Write:
   - README with installation and usage instructions
   - API documentation (if applicable)
   - Configuration reference

### Phase 5 — Verification
1. **Full Test Suite**: Run all unit + integration tests. Target: 0 failures.
2. **Linter Clean**: Zero warnings from linter/formatter.
3. **Build Verification**: `npm run build` or equivalent succeeds without warnings.
4. **Manual Smoke Test**: Run the application and verify the 3 most critical user flows.
5. **Security Scan**: Run `npm audit` or equivalent — no critical/high vulnerabilities.

**Gate**: All tests pass, build succeeds, no critical security issues. If any fail, return to Phase 4.

### Phase 6 — Delivery
1. **Production Build**: Generate optimized production artifacts.
2. **Deployment Guide**: Write step-by-step deployment instructions.
3. **Environment Config**: Document all required environment variables.
4. **Log**: Record the application build in **`AETHER.md` §18**.

## Failure Paths
- **Architecture Disagreement**: Return to Phase 1 and iterate on the design.
- **Test Failures Persist**: After 3 fix attempts on the same test, invoke `/antibug` for root-cause analysis.
- **Dependency Conflict**: If packages conflict, document the conflict, try resolution, and if unresolvable, suggest an alternative package.
- **Scope Overflow**: If features exceed the session capacity, deliver what's complete, document remaining work in the task list, and hand off cleanly.

## Quality Standards
- ✅ Every public function has a docstring/JSDoc comment
- ✅ No function exceeds 50 lines (decompose if longer)
- ✅ No file exceeds 300 lines (split into modules if longer)
- ✅ All error messages are user-friendly (no raw stack traces in production)
- ✅ Configuration is externalized (no hardcoded values)
- ❌ NO `console.log` debugging left in production code
- ❌ NO commented-out code blocks

## Output Organization (Rule 20)
Application code lives in the project directory. Log creation to **`AETHER.md` §18**.

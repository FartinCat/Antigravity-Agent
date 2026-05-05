---
name: jsts-agent
description: JavaScript/TypeScript-specific language agent. Encodes JS/TS rules, instincts, and verification workflows for modern, type-safe web development.
origin: Custom Ensemble (Claude + DeepSeek + Gemini)
---

# Agent: JavaScript/TypeScript Language Specialist

## Rules

### JSTS-R001: STRICT_MODE
All JavaScript files must use `'use strict'` or be ESM modules (which are strict by default). TypeScript `strict: true` in tsconfig is mandatory.

### JSTS-R002: NO_FLOATING_PROMISES
Every `async` function call must be `await`ed, `.then()`ed, or explicitly voided with `void promise`. Unhandled promise rejections are bugs.

### JSTS-R003: ESM_CJS_CONSISTENCY
A project must use one module system. Mixing `require()` and `import` in the same codebase requires explicit justification and boundary documentation.

### JSTS-R004: ENV_SPLIT
Environment-specific configuration (API URLs, feature flags, secrets) must be loaded from environment variables or config files, never hardcoded.

### JSTS-R005: DEPENDENCY_AUDIT
Before adding a new npm dependency, verify:
- Last publish date (>12 months = stale risk)
- Weekly downloads (threshold: >10,000)
- Known vulnerabilities (`npm audit`)
- Bundle size impact

### JSTS-R006: NO_DEFAULT_EXPORTS
Prefer named exports over default exports. Default exports lose refactoring safety and IDE support.

### JSTS-R007: PROMISE_ALLSETTLED_OVER_ALL
When multiple independent async operations are run in parallel, prefer `Promise.allSettled()` over `Promise.all()` to avoid losing results from successful operations when one fails.

---

## Instincts

### JSTS-INSTINCT-001: ASYNC_FOREACH (p=0.92)
`array.forEach(async (item) => ...)` — does not await iterations. Use `for...of` with `await` or `Promise.all(array.map(...))`.

### JSTS-INSTINCT-002: CLOSURE_IN_LOOP (p=0.78)
`var` variable captured in a closure inside a loop — all iterations share the same variable. Use `let` or `const`.

### JSTS-INSTINCT-003: PROTOTYPE_POLLUTION (p=0.90)
Deep merge or `Object.assign()` from untrusted input without property filtering — prototype pollution risk.

### JSTS-INSTINCT-004: REACT_STALE_CLOSURE (p=0.85)
React `useEffect` or `useCallback` with missing dependency array entries — stale closure bug.

### JSTS-INSTINCT-005: V8_DEOPTIMIZATION (p=0.55)
Patterns that cause V8 deoptimization: megamorphic property access, `delete` on objects, `arguments` in hot paths.

### JSTS-INSTINCT-006: EVENT_LISTENER_LEAK (p=0.80)
`addEventListener()` without corresponding `removeEventListener()` in cleanup — memory leak in SPAs and component lifecycles.

---

## Verification Workflow
1. `tsc --noEmit` — type checking (TypeScript) or `node --check` (JavaScript)
2. `eslint .` — linting
3. `npm audit` — dependency vulnerabilities
4. `jest` or `vitest` — unit tests
5. Bundle size check: `npx bundlephobia-cli` for new dependencies

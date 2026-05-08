---
rule: 16-sdd-lifecycle
priority: HIGH
---
# Rule 16: Spec-Driven Development Lifecycle

## The Law
Never write code for a feature that lacks a written specification.

## Why This Exists
Prevents building features based on assumptions, endless rework due to misunderstood requirements, and creating features with impossible-to-test acceptance criteria.

## Mandatory Behaviors
1. Run `/spec` before initiating any feature work.
2. `SPEC.md` must contain all 6 core areas before any coding begins.
3. User must explicitly confirm the spec before proceeding to `/plan`.
4. Plan must be confirmed before proceeding to `/impl`.
5. Update `SPEC.md` immediately when scope changes — never let the spec go stale.

## Prohibited Behaviors
1. Saying "The spec is obvious, I'll just implement."
2. Writing code first, then writing a spec to match it.
3. Treating acceptance criteria as optional suggestions.
4. Implementing features that are not explicitly documented in the spec without proposing a spec amendment first.

## Enforcement
- Check for `SPEC.md` before `/impl`. If missing, halt and redirect to `/spec`.

# Instinct: Minimal Footprint

## The Pattern
Make the smallest change that solves the problem.

## When It Fires
- About to refactor code that wasn't broken.
- About to rewrite more than was asked.
- About to add dependencies when the standard library works.

## Correct Behavior
"I'm only changing lines 14-22 in auth.py. Everything else stays as is."

## Failure Mode
- Refactoring 3 files while fixing a 1-line bug.
- Adding an external library when a 10-line function would suffice.
- Restructuring project directories unnecessarily.

## Override Protocol
"User said 'clean up while you're in there'" — explicitly confirm the scope of cleanup before proceeding.

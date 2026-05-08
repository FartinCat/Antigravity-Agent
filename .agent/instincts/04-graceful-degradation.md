# Instinct: Graceful Degradation

## The Pattern
Keep working when one part fails. Report clearly. Never hide failures.

## When It Fires
- An MCP tool fails or times out.
- A test fails.
- A build breaks.
- An API returns unexpected data.

## Correct Behavior
"The fetch MCP failed. I'll fall back to file-based research and note the limitation."
"The build failed on line 42. Here is the error, I'll invoke /antibug."

## Failure Mode
- Silently skipping a failing test to show a green build.
- Hiding a build error to present the task as "done".
- Claiming success when a background step actually failed.

## Override Protocol
N/A — always report failures.

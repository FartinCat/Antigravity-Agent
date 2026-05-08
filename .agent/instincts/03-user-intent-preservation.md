# Instinct: User Intent Preservation

## The Pattern
Serve what the user MEANS, not just what they say.

## When It Fires
- Request is highly ambiguous.
- Literal interpretation would produce a wrong or destructive result.
- Before any destructive operation (rm, drop, prune).

## Correct Behavior
"You said 'delete the old tests' — I want to confirm you mean the files in `tests/legacy/`, not `tests/unit/`."

## Failure Mode
- Silently deleting the wrong directory because it technically matched the pattern.
- Implementing a completely different feature than described because the terminology was slightly off.
- Blindly executing a broken command provided by the user.

## Override Protocol
N/A — always confirm before destructive ops or if intent is unclear.

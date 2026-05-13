#!/usr/bin/env python3
"""
detect_root.py — Dynamic root detection for Aether Agent
=============================================================================
Rules:
  - Never uses __file__-relative paths or hardcoded absolute paths
  - Never persists the root to disk (session-local variable only)
  - Works in VS Code, Cursor, Windsurf, Claude Code, Gemini, plain terminal, CI
  - Respects AETHER_ROOT env var for explicit overrides (e.g. CI pipelines)
  - Walks UP from cwd, not down — safe even inside massive monorepos

Usage:
  from detect_root import detect_root, root_relative, get_root

  root = detect_root()               # first call — detects and caches
  agents = root_relative(".agents")  # path helpers
  root2 = detect_root()              # subsequent calls — returns cached value
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

# --------------------------------------------------------------------------- #
# Markers that identify an agent root. Listed in priority order.
# Create a .agent-root file in any directory to pin it as the root.
# --------------------------------------------------------------------------- #
ROOT_MARKERS = [
    ".agent-root",       # Explicit pin file — highest priority
    ".aether-root",      # Explicit pin file alternative
    "AETHER.md",         # Unified Aether state file (strong signal)
    ".agents",           # Agent infrastructure directory
    ".agent",            # Agent infrastructure directory (legacy/alternative)
    ".claude",           # Claude-specific commands directory
    ".git",              # Git repo root — reliable fallback
    "package.json",      # Node.js project root
    "pyproject.toml",    # Python project root
    "Cargo.toml",        # Rust project root
    "go.mod",            # Go project root
    "CLAUDE.md",         # IDE stub — weaker than AETHER.md
]

MAX_WALK_DEPTH = 6  # Never walk more than 6 levels up
_SESSION_ROOT: Optional[Path] = None  # Never written to disk


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def detect_root(start: Optional[str] = None, interactive: bool = True) -> Path:
    """
    Detect and cache the agent root directory for this session.

    Resolution order:
      1. Return cached value (already detected this session)
      2. Check AETHER_ROOT / AGENT_ROOT environment variables
      3. Walk up from `start` (defaults to cwd) looking for root markers
      4. Ask user interactively if `interactive=True`
      5. Raise RuntimeError with actionable message
    """
    global _SESSION_ROOT

    if _SESSION_ROOT is not None:
        return _SESSION_ROOT

    for env_key in ("AETHER_ROOT", "AGENT_ROOT", "AOS_ROOT"):
        env_val = os.environ.get(env_key)
        if env_val:
            candidate = Path(env_val).resolve()
            if candidate.exists():
                _SESSION_ROOT = candidate
                _log(f"📍 Agent root (from ${env_key}): {_SESSION_ROOT}")
                return _SESSION_ROOT
            else:
                _log(f"⚠️  ${env_key} set to '{env_val}' but path does not exist — ignoring")

    start_path = Path(start).resolve() if start else Path.cwd().resolve()
    found_root, found_marker, found_depth = _walk_up(start_path)

    if found_root is not None:
        _SESSION_ROOT = found_root
        depth_note = "" if found_depth == 0 else f" (walked {found_depth} level{'s' if found_depth > 1 else ''} up)"
        _log(f"📍 Agent root{depth_note}: {_SESSION_ROOT}  [via {found_marker}]")
        return _SESSION_ROOT

    if interactive and _is_interactive():
        _SESSION_ROOT = _ask_user(start_path)
        return _SESSION_ROOT

    raise RuntimeError(
        f"\n❌ Cannot detect agent root from: {start_path}\n"
        f"   Searched up {MAX_WALK_DEPTH} directory levels for: {', '.join(ROOT_MARKERS)}\n\n"
        f"   Fix options:\n"
        f"   A) Create a .agent-root file in your project root:  touch /your/project/.agent-root\n"
        f"   B) Set an environment variable:                     export AETHER_ROOT=/your/project\n"
        f"   C) Run from inside the project directory:           cd /your/project && ./agentic-os start\n"
    )


def get_root() -> Path:
    if _SESSION_ROOT is None:
        raise RuntimeError("Agent root not initialized. Call detect_root() before get_root().")
    return _SESSION_ROOT


def root_relative(*parts: str) -> Path:
    return get_root().joinpath(*parts)


def reset_root() -> None:
    global _SESSION_ROOT
    _SESSION_ROOT = None


def verify_root(root: Optional[Path] = None) -> dict:
    r = root or get_root()
    components = {
        "root":               str(r),
        "agents_dir":         (r / ".agents").is_dir() or (r / ".agent").is_dir(),
        "claude_dir":         (r / ".claude").is_dir(),
        "git_repo":           (r / ".git").is_dir(),
        "aether_md":          (r / "AETHER.md").is_file(),
        "claude_md":          (r / "CLAUDE.md").is_file(),
        "legacy_project_metadata": (r / "PROJECT_METADATA.md").is_file(),
        "agent_pin":          (r / ".agent-root").is_file(),
    }
    components["is_valid_agent_root"] = (
        components["agents_dir"] or components["claude_dir"]
    )
    return components


# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #

def _walk_up(start: Path) -> tuple[Optional[Path], Optional[str], int]:
    current = start
    for depth in range(MAX_WALK_DEPTH + 1):
        for marker in ROOT_MARKERS:
            candidate = current / marker
            if candidate.exists():
                return current, marker, depth
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None, None, -1


def _is_interactive() -> bool:
    ci_vars = ("CI", "CONTINUOUS_INTEGRATION", "GITHUB_ACTIONS", "GITLAB_CI",
               "TRAVIS", "CIRCLECI", "JENKINS_URL", "CODEBUILD_BUILD_ID")
    if any(os.environ.get(v) for v in ci_vars):
        return False
    return sys.stdin.isatty()


def _ask_user(start: Path) -> Path:
    print(f"\n⚠️  Could not detect agent root from: {start}", file=sys.stderr)
    print(f"   Searched for: {', '.join(ROOT_MARKERS)}", file=sys.stderr)
    print(f"   Tip: create a .agent-root file in your project root to pin it.\n",
          file=sys.stderr)

    try:
        answer = input("Where is the agent's root directory? [Enter = cwd]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n❌ Aborted.", file=sys.stderr)
        sys.exit(1)

    candidate = Path(answer).resolve() if answer else Path.cwd().resolve()

    if not candidate.exists():
        print(f"\n❌ Directory does not exist: {candidate}", file=sys.stderr)
        sys.exit(1)

    if not candidate.is_dir():
        print(f"\n❌ Not a directory: {candidate}", file=sys.stderr)
        sys.exit(1)

    return candidate


def _log(message: str) -> None:
    print(message, file=sys.stderr)


# --------------------------------------------------------------------------- #
# Patch sync_registry.py to use this module instead of __file__ hacks
# --------------------------------------------------------------------------- #

def patch_sync_registry() -> Path:
    return detect_root(interactive=False)


if __name__ == "__main__":
    import argparse
    import sys
    # Fix for Windows console encoding
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
    parser = argparse.ArgumentParser(description="Detect and verify the Aether Agent root directory.")
    parser.add_argument("--start",  help="Directory to start detection from (default: cwd)")
    parser.add_argument("--verify", action="store_true", help="Show component checklist")
    parser.add_argument("--json",   action="store_true", help="Output as JSON")
    parser.add_argument("--pin",    action="store_true", help="Create .agent-root in cwd")
    parser.add_argument("--reset",  action="store_true", help="Clear cached root (testing)")
    args = parser.parse_args()

    if args.reset:
        reset_root()

    if args.pin:
        pin_path = Path.cwd() / ".agent-root"
        pin_path.write_text("# Aether Agent root pin\n")
        print(f"✅ Created {pin_path}")
        sys.exit(0)

    try:
        root = detect_root(start=args.start)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if args.verify:
        info = verify_root(root)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"\nRoot: {root}\n\nComponent check:")
            for key, present in {k: v for k, v in info.items() if k != "root"}.items():
                print(f"  {'✅' if present else '❌'}  {key.replace('_', ' ')}")
            print(f"\n{'✅ Valid agent root' if info['is_valid_agent_root'] else '⚠️  Not a recognized agent root'}")
    else:
        print(root if not args.json else json.dumps({"root": str(root)}))

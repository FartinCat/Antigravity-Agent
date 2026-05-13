#!/usr/bin/env bash
# entrypoint.sh — Aether Agent CLI Entrypoint

# Parse arguments
INTERACTIVE=true
for i in "$@"; do
    case $i in
        --root=*)
        export AETHER_ROOT="${i#*=}"
        shift
        ;;
        --root)
        export AETHER_ROOT="$2"
        shift
        shift
        ;;
        --non-interactive)
        INTERACTIVE=false
        shift
        ;;
    esac
done

# Resolve the root dynamically via bootstrap.js
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is required to run Aether Agent."
    exit 1
fi

# Locate the agent relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="$SCRIPT_DIR/.agent/scripts/bootstrap.js"

if [ ! -f "$BOOTSTRAP_SCRIPT" ]; then
    echo "❌ Error: Could not find bootstrap script at $BOOTSTRAP_SCRIPT"
    exit 1
fi

# Detect root
DETECTED_ROOT=$(node "$BOOTSTRAP_SCRIPT")
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Aether Agent OS initialized at: $DETECTED_ROOT"
echo ""
echo "Commands available:"
echo "  ./agentic-os start     - Start the agent loop"
echo "  ./agentic-os sync      - Synchronize registry and versions"
echo "  ./agentic-os readme    - Regenerate README"
echo ""

# Handle subcommands
case "$1" in
    start)
        echo "🚀 Starting Aether Agent..."
        # Launch main logic (placeholder for whatever runs the agent interactively)
        # For now, it just confirms detection worked
        ;;
    sync)
        echo "🔄 Synchronizing registry..."
        python3 "$SCRIPT_DIR/.agent/scripts/sync_registry.py"
        ;;
    readme)
        echo "📝 Regenerating README..."
        python3 "$SCRIPT_DIR/.agent/scripts/readme_architect.py"
        ;;
    *)
        echo "Agent ready. Run './agentic-os start' to begin."
        ;;
esac

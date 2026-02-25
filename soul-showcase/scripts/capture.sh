#!/bin/bash
# capture.sh -- Record a command's output as a terminal GIF
# Usage: capture.sh <output.gif> <command...>
#
# Example: capture.sh board.gif python -m soul_planner board
#
# Requires: asciinema, agg

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: capture.sh <output.gif> <command...>" >&2
    exit 1
fi

GIF_PATH="$1"
shift
COMMAND="$*"

# Check dependencies
if ! command -v asciinema &>/dev/null; then
    echo "ERROR: asciinema not installed. Run: sudo apt install asciinema" >&2
    exit 1
fi
if ! command -v agg &>/dev/null; then
    echo "ERROR: agg not installed. Run: ~/soul/soul-showcase/scripts/install-deps.sh" >&2
    exit 1
fi

CAST_FILE=$(mktemp /tmp/showcase-XXXXXX.cast)
trap "rm -f $CAST_FILE" EXIT

# Record the command (non-interactive, 2 second idle limit)
asciinema rec \
    --command "$COMMAND" \
    --idle-time-limit 2 \
    --quiet \
    "$CAST_FILE"

# Convert to GIF
# --cols 100 --rows 30 for consistent sizing
# --font-size 16 for readability
agg \
    --cols 100 \
    --rows 30 \
    --font-size 16 \
    "$CAST_FILE" \
    "$GIF_PATH"

echo "Captured: $GIF_PATH ($(du -h "$GIF_PATH" | cut -f1))"

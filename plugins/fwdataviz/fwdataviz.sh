#!/bin/bash
# Fixed-width Data Visualizer — macOS native plugin stub for NotepadMac
# Full implementation needs NSTableView/NSOutlineView panel UI

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  detect-fixed-width)
    python3 -c "
import sys
lines = sys.stdin.read().split('\n')
if not lines:
    print('No data')
    sys.exit(0)
# Detect fixed-width columns by analyzing line lengths
widths = [len(line) for line in lines if line]
avg_width = sum(widths) / len(widths) if widths else 0
is_fixed = all(w == widths[0] for w in widths) if len(widths) > 1 else False
print(f'Lines: {len(lines)}, Avg width: {avg_width:.0f}, Fixed-width: {is_fixed}')
"
    ;;
  extract-fields)
    echo "Field extraction requires native NSTableView UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

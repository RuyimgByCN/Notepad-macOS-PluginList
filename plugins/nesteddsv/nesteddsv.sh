#!/bin/bash
# NestedDSV — macOS native plugin stub for NotepadMac
# Full visualization needs NSOutlineView panel UI

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  detect-dsv)
    python3 -c "
import sys, csv, io

text = sys.stdin.read()
first_lines = text.split('\n')[:5]

# Try to detect delimiter
delimiters = [',', ';', '\t', '|', ':']
for delim in delimiters:
    counts = [line.count(delim) for line in first_lines if line]
    if counts and min(counts) > 0 and all(c == counts[0] for c in counts):
        print(f'Delimiter: {repr(delim)}, Fields per line: {counts[0] + 1}')
        sys.exit(0)

print('Could not detect DSV format', file=sys.stderr)
"
    ;;
  extract-dsv-fields)
    echo "Field extraction requires native NSOutlineView UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

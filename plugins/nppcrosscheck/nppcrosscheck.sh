#!/bin/bash
# NppCrossCheck — macOS native plugin for NotepadMac
# Compare two lists separated by blank lines

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  cross-check|find-intersection|find-difference|find-union)
    python3 -c "
import sys

text = sys.stdin.read()
parts = text.split('\n\n')
if len(parts) < 2:
    # Try splitting on multiple blank lines
    import re
    parts = re.split(r'\n{2,}', text)

if len(parts) < 2:
    print('Error: Need two lists separated by blank lines', file=sys.stderr)
    sys.exit(1)

list_a = set(line.strip() for line in parts[0].strip().split('\n') if line.strip())
list_b = set(line.strip() for line in parts[1].strip().split('\n') if line.strip())

import os
cmd = os.environ.get('NPP_CROSS_CMD', '$COMMAND')

result = []
if cmd == 'cross-check':
    result.append('=== Intersection (A ∩ B) ===')
    for item in sorted(list_a & list_b):
        result.append(item)
    result.append('')
    result.append('=== In A but not B (A - B) ===')
    for item in sorted(list_a - list_b):
        result.append(item)
    result.append('')
    result.append('=== In B but not A (B - A) ===')
    for item in sorted(list_b - list_a):
        result.append(item)
elif cmd == 'find-intersection':
    for item in sorted(list_a & list_b):
        result.append(item)
elif cmd == 'find-difference':
    for item in sorted(list_a - list_b):
        result.append(item)
elif cmd == 'find-union':
    for item in sorted(list_a | list_b):
        result.append(item)

print('\n'.join(result))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

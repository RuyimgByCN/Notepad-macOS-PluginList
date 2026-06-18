#!/bin/bash
# Task List — macOS native plugin for NotepadMac
# Scan TODO/FIXME/NOTE items from document

COMMAND="$1"
if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  scan-todos|scan-fixmes|scan-all-tasks)
    python3 -c "
import sys, re, os

cmd = '$COMMAND'
text = sys.stdin.read()

patterns = {
    'scan-todos': [r'\bTODO\b'],
    'scan-fixmes': [r'\bFIXME\b', r'\bFIX\b'],
    'scan-all-tasks': [r'\bTODO\b', r'\bFIXME\b', r'\bNOTE\b', r'\bHACK\b', r'\bXXX\b', r'\bBUG\b'],
}

results = []
for i, line in enumerate(text.split('\n'), 1):
    for pat in patterns.get(cmd, patterns['scan-all-tasks']):
        if re.search(pat, line, re.IGNORECASE):
            results.append(f'Line {i}: {line.strip()}')

if results:
    print('\n'.join(results))
else:
    print('No task markers found')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

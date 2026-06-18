#!/bin/bash
# NppTextViz — macOS native plugin for NotepadMac
# Hide/show lines matching pattern (for log analysis)

COMMAND="$1"
if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi
# NPP_HIDE_PATTERN environment variable for the pattern
PATTERN="${NPP_HIDE_PATTERN:-}"

case "$COMMAND" in
  hide-matching-lines)
    if [ -z "$PATTERN" ]; then
        echo "Error: NPP_HIDE_PATTERN not set" >&2
        exit 1
    fi
    python3 -c "
import sys, re
pattern = '$PATTERN'
text = sys.stdin.read()
for line in text.split('\n'):
    if not re.search(pattern, line):
        print(line)
"
    ;;
  show-all-lines)
    # Just output everything (undo hiding)
    cat
    ;;
  hide-non-matching)
    if [ -z "$PATTERN" ]; then
        echo "Error: NPP_HIDE_PATTERN not set" >&2
        exit 1
    fi
    python3 -c "
import sys, re
pattern = '$PATTERN'
text = sys.stdin.read()
for line in text.split('\n'):
    if re.search(pattern, line):
        print(line)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# DoxyIt — macOS native plugin for NotepadMac
# Converted from upstream DoxyIt (v0.4.4, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  generate-comment)
    python3 -c "
import sys
lines = sys.stdin.read().rstrip('\n').splitlines()
out = ['/**']
for ln in lines:
    out.append(' * ' + ln)
out.append(' */')
print('\n'.join(out))
    "
    ;;
  convert-javadoc)
    python3 -c "
import sys
lines = sys.stdin.read().rstrip('\n').splitlines()
out = ['/**']
for ln in lines:
    out.append(' * ' + ln)
out += [' *', ' * @return description', ' */']
print('\n'.join(out))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

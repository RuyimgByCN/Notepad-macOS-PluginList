#!/bin/bash
# pycalc — macOS native plugin for NotepadMac
# Converted from upstream pycalc (v1.0.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  calc)
    python3 -c "
import sys
expr = sys.stdin.read().strip()
try:
    print(eval(expr, {'__builtins__': {}}, __import__('math').__dict__))
except Exception as e:
    print('Error:', e, file=sys.stderr); sys.exit(1)
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

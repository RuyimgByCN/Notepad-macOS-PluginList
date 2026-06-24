#!/bin/bash
# PyNPP — macOS native plugin for NotepadMac
# Converted from upstream PyNPP (v1.2, x86)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  run-python)
    python3 -c "
import sys, io
code = sys.stdin.read()
buf = io.StringIO()
old = sys.stdout; sys.stdout = buf
try:
    exec(code, {'__name__': '__main__'})
except Exception as e:
    sys.stdout = old; print('Error:', e, file=sys.stderr); sys.exit(1)
sys.stdout = old; sys.stdout.write(buf.getvalue())
    "
    ;;
  python-version)
    python3 --version
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

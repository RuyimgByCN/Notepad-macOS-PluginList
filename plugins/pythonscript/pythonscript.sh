#!/bin/bash
# PythonScript — macOS native plugin for NotepadMac
# Converted from upstream PythonScript (v2.1.0.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  exec-python)
    python3 -c "
import sys, io
code = sys.stdin.read()
buf = io.StringIO()
try:
    exec(code, {'__name__': '__main__'}, {'__stdout__': buf})
except Exception as e:
    print('Error:', e, file=sys.stderr); sys.exit(1)
sys.stdout.write(buf.getvalue())
    "
    ;;
  eval-python)
    python3 -c "
import sys
try:
    print(eval(sys.stdin.read(), {'__builtins__': __builtins__}))
except Exception as e:
    print('Error:', e, file=sys.stderr); sys.exit(1)
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

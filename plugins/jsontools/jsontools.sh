#!/bin/bash
# JSON Tools — macOS native plugin for NotepadMac
# Converted from upstream JsonTools (v8.5, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  format-json)
    python3 -c "
import sys, json
print(json.dumps(json.loads(sys.stdin.read()), indent=2, ensure_ascii=False))
    "
    ;;
  minify-json)
    python3 -c "
import sys, json
print(json.dumps(json.loads(sys.stdin.read()), separators=(',', ':'), ensure_ascii=False))
    "
    ;;
  validate-json)
    python3 -c "
import sys, json
try:
    json.loads(sys.stdin.read()); print('JSON is valid.')
except Exception as e:
    print('JSON error:', e, file=sys.stderr); sys.exit(1)
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

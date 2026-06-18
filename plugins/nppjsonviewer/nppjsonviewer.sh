#!/bin/bash
# JSON Viewer — macOS native plugin for NotepadMac
# JSON formatting, minification, and validation

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  format-json)
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f'JSON Error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  minify-json)
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, separators=(',', ':'), ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f'JSON Error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  validate-json)
    python3 -c "
import sys, json
try:
    json.load(sys.stdin)
    print('JSON is valid')
except json.JSONDecodeError as e:
    print(f'JSON Error at line {e.lineno}, column {e.colno}: {e.msg}')
    sys.exit(1)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

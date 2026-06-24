#!/bin/bash
# XBrackets Lite — macOS native plugin for NotepadMac
# Converted from upstream XBrackets (v1.3.1, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  wrap-paren)
    python3 -c "
import sys
s = sys.stdin.read(); print('(' + s + ')')
    "
    ;;
  wrap-bracket)
    python3 -c "
import sys
s = sys.stdin.read(); print('[' + s + ']')
    "
    ;;
  wrap-brace)
    python3 -c "
import sys
s = sys.stdin.read(); print('{' + s + '}')
    "
    ;;
  wrap-quote)
    python3 -c "
import sys
s = sys.stdin.read(); print('"' + s + '"')
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# URL Encode/Decode — macOS native plugin for NotepadMac
# URL encoding and decoding using Python urllib

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  url-encode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.quote(sys.stdin.read(), safe=''))
"
    ;;
  url-decode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.unquote(sys.stdin.read()))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

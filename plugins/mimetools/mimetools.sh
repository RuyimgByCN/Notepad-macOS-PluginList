#!/bin/bash
# Mime tools — macOS native plugin for NotepadMac
# Base64, Quoted-printable, URL encode/decode

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  base64-encode)
    python3 -c "
import sys, base64
text = sys.stdin.buffer.read()
print(base64.b64encode(text).decode('ascii'))
"
    ;;
  base64-decode)
    python3 -c "
import sys, base64
text = sys.stdin.read().strip()
try:
    print(base64.b64decode(text).decode('utf-8', errors='replace'))
except Exception as e:
    print(f'Decode error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  qp-encode)
    python3 -c "
import sys, quopri
text = sys.stdin.buffer.read()
print(quopri.encodestring(text).decode('ascii'))
"
    ;;
  qp-decode)
    python3 -c "
import sys, quopri
text = sys.stdin.read()
print(quopri.decodestring(text.encode('ascii')).decode('utf-8', errors='replace'))
"
    ;;
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

#!/bin/bash
# HTML Tag — macOS native plugin for NotepadMac
# HTML entity and JS character encoding/decoding

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  encode-html-entities)
    python3 -c "
import sys, html
text = sys.stdin.read()
print(html.escape(text, quote=True))
"
    ;;
  decode-html-entities)
    python3 -c "
import sys, html
text = sys.stdin.read()
print(html.unescape(text))
"
    ;;
  encode-js-chars)
    python3 -c "
import sys
text = sys.stdin.read()
result = []
for ch in text:
    cp = ord(ch)
    if cp > 127:
        result.append(f'\\u{cp:04X}')
    else:
        result.append(ch)
print(''.join(result))
"
    ;;
  decode-js-chars)
    python3 -c "
import sys, re
text = sys.stdin.read()
def replace_js(m):
    return chr(int(m.group(1), 16))
print(re.sub(r'\\u([0-9a-fA-F]{4})', replace_js, text))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

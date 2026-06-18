#!/bin/bash
# Emoji Description — macOS native plugin for NotepadMac
# Shows Unicode code point, UTF-8 bytes, HTML entity for selected text

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  char-info)
    python3 -c "
import sys, html

text = sys.stdin.read()
results = []
for ch in text:
    cp = ord(ch)
    utf8 = ch.encode('utf-8')
    hex_bytes = ' '.join(f'{b:02X}' for b in utf8)
    html_ent = html.escape(ch)
    try:
        html_num_ent = f'&#x{cp:X};'
    except:
        html_num_ent = ''
    name = ''
    try:
        import unicodedata
        name = unicodedata.name(ch, '')
    except:
        pass
    results.append(f'{ch}  U+{cp:04X}  Dec:{cp}  UTF-8:[{hex_bytes}]  HTML:{html_num_ent}  Name:{name}')

print('\n'.join(results) if results else 'No characters selected')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

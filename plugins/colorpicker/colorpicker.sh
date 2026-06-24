#!/bin/bash
# Don Rowlett Color Picker — macOS native plugin for NotepadMac
# Converted from upstream ColorPicker (v2.3, x86)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  hex-to-rgb)
    python3 -c "
import sys, re
s = sys.stdin.read().strip().lstrip('#')
if len(s) == 3: s = ''.join(c*2 for c in s)
r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
print(f'rgb({r}, {g}, {b})')
    "
    ;;
  rgb-to-hex)
    python3 -c "
import sys, re
m = re.search(r'(\d+)\D+(\d+)\D+(\d+)', sys.stdin.read())
if not m: print('Input: rgb(r, g, b)', file=sys.stderr); sys.exit(1)
r, g, b = map(int, m.groups())
print('#{:02x}{:02x}{:02x}'.format(r, g, b))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

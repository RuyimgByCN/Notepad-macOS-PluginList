#!/bin/bash
# Npp Converter — macOS native plugin for NotepadMac
# ASCII ↔ Hex conversion

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  ascii-to-hex)
    python3 -c "
import sys
text = sys.stdin.read()
hex_str = ' '.join(f'{ord(c):02X}' for c in text)
print(hex_str)
"
    ;;
  hex-to-ascii)
    python3 -c "
import sys
hex_str = sys.stdin.read().strip()
# Remove spaces and colons
hex_str = hex_str.replace(' ', '').replace(':', '')
try:
    result = bytes.fromhex(hex_str).decode('utf-8', errors='replace')
    print(result)
except ValueError as e:
    print(f'Hex decode error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

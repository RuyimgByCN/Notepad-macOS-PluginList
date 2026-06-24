#!/bin/bash
# AutoCodepage — macOS native plugin for NotepadMac
# Converted from upstream AutoCodepage (v1.2.7, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  detect-encoding)
    python3 -c "
import sys
raw = sys.stdin.buffer.read()
enc = 'ascii'
if raw.startswith(b'\xef\xbb\xbf'): enc = 'utf-8-sig'
elif raw.startswith(b'\xff\xfe'): enc = 'utf-16-le'
elif raw.startswith(b'\xfe\xff'): enc = 'utf-16-be'
else:
    try: raw.decode('ascii'); enc = 'ascii'
    except UnicodeDecodeError:
        try: raw.decode('utf-8'); enc = 'utf-8'
        except UnicodeDecodeError: enc = 'latin-1 (fallback)'
print(f'Bytes: {len(raw)}, detected encoding: {enc}')
    "
    ;;
  byte-stats)
    python3 -c "
import sys, collections
raw = sys.stdin.buffer.read()
c = collections.Counter(raw)
print(f'Total bytes: {len(raw)}')
print(f'Non-ASCII bytes: {sum(v for b, v in c.items() if b > 127)}')
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

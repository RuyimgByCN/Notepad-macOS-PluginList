#!/bin/bash
# NppHash — macOS native plugin for NotepadMac
# Converted from upstream NppHasher (v1.0, x86)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  md5)
    python3 -c "
import sys, hashlib
print(hashlib.md5(sys.stdin.buffer.read()).hexdigest())
    "
    ;;
  sha256)
    python3 -c "
import sys, hashlib
print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())
    "
    ;;
  base64-encode)
    python3 -c "
import sys, base64
print(base64.b64encode(sys.stdin.buffer.read()).decode())
    "
    ;;
  base64-decode)
    python3 -c "
import sys, base64
print(base64.b64decode(sys.stdin.read()).decode(errors='replace'))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

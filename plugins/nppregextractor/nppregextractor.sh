#!/bin/bash
# NppRegExTractor — macOS native plugin for NotepadMac
# Converted from upstream NppRegExTractorPlugin (v2.1.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  extract-emails)
    python3 -c "
import sys, re
print('\n'.join(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', sys.stdin.read())))
    "
    ;;
  extract-urls)
    python3 -c "
import sys, re
print('\n'.join(re.findall(r'https?://[^\s)\]\"\']+', sys.stdin.read())))
    "
    ;;
  extract-ips)
    python3 -c "
import sys, re
print('\n'.join(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', sys.stdin.read())))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# Preview HTML — macOS native plugin for NotepadMac
# Converted from upstream PreviewHTML (v1.4.5.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  validate-html)
    python3 -c "
import sys, re
data = sys.stdin.read()
opens = re.findall(r'<([a-zA-Z0-9]+)[^>]*>', data)
closes = re.findall(r'</([a-zA-Z0-9]+)>', data)
print(f'Opening tags: {len(opens)}, closing tags: {len(closes)}')
    "
    ;;
  preview)
    echo "HTML preview requires native WKWebView — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

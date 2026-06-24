#!/bin/bash
# Tidy2 — macOS native plugin for NotepadMac
# Converted from upstream Tidy2 (v0.2, x86)

COMMAND="$1"

if ! command -v tidy > /dev/null 2>&1; then
    echo "Error: tidy is required. Install: brew install tidy-html5" >&2
    exit 1
fi

case "$COMMAND" in
  tidy-html)
    tidy -q -utf8 --tidy-mark n 2>/dev/null
    ;;
  tidy-xml)
    tidy -q -xml -utf8 --tidy-mark n 2>/dev/null
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

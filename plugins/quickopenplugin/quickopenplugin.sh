#!/bin/bash
# QuickOpenPlugin — macOS native plugin for NotepadMac
# Converted from upstream QuickOpenPlugin (v1.1, x86)

COMMAND="$1"

case "$COMMAND" in
  open-selected)
    open "$(cat)" 2>/dev/null || echo "Selected text is not a valid path" >&2
    ;;
  quick-open)
    echo "Fuzzy quick-open panel requires native UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

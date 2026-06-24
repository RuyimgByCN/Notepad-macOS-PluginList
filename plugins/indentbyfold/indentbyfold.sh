#!/bin/bash
# Indent By Fold — macOS native plugin for NotepadMac
# Converted from upstream IndentByFold (v0.7.3, x64)

COMMAND="$1"

case "$COMMAND" in
  reindent)
    echo "Fold-based indent requires editor fold-point API — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

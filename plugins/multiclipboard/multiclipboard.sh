#!/bin/bash
# MultiClipboard — macOS native plugin for NotepadMac
# Converted from upstream MultiClipboard (v2.1.0.0, x86)

COMMAND="$1"

case "$COMMAND" in
  show-history)
    echo "Clipboard history requires native panel UI — pending implementation" >&2
    ;;
  paste-buffer)
    echo "Multi-buffer paste requires native UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

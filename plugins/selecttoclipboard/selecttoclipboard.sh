#!/bin/bash
# Select to Clipboard — macOS native plugin for NotepadMac
# Copy selected text to clipboard using macOS pbcopy

COMMAND="$1"

case "$COMMAND" in
  copy-selection)
    pbcopy
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

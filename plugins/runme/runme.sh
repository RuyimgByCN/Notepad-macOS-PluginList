#!/bin/bash
# RunMe — macOS native plugin for NotepadMac
# Execute current file or open containing folder

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  run-file)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    open "$FILE"
    ;;
  run-in-terminal)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    # Open Terminal.app and run the file
    osascript -e "tell application \"Terminal\" to do script \"cd '$(dirname "$FILE")' && './$(basename "$FILE")'\""
    ;;
  open-containing-folder)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    open "$(dirname "$FILE")"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

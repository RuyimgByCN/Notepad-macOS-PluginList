#!/bin/bash
# HEX-Editor — macOS native plugin stub for NotepadMac
# Full hex editing needs native panel UI (Scintilla hex mode or custom NSView)

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  hex-dump)
    if [ -n "$FILE" ]; then
        xxd "$FILE" 2>&1 | head -256
    else
        INPUT=$(cat)
        echo "$INPUT" | xxd 2>&1 | head -256
    fi
    ;;
  hex-view-selection)
    INPUT=$(cat)
    echo "$INPUT" | xxd 2>&1
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

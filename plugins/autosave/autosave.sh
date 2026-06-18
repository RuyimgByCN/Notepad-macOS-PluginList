#!/bin/bash
# AutoSave — macOS native plugin stub for NotepadMac
# Full implementation needs Swift Timer + NSDocument.save() + FSEvent monitoring
# This stub provides basic save-all functionality

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  save-all-now)
    if [ -n "$FILE" ]; then
        # Save the current file (host will handle all-file save)
        echo "SAVE_CURRENT"
    fi
    ;;
  toggle-autosave)
    echo "AutoSave toggle requires native Swift implementation (Timer + NSDocument)" >&2
    echo "This is a stub — full functionality pending native code." >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

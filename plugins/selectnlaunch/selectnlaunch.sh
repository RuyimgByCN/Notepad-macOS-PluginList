#!/bin/bash
# Select N' Launch — macOS native plugin for NotepadMac
# Save selection as temp file and open with associated program

COMMAND="$1"
# NPP_FILE_EXT environment variable for desired extension
FILE_EXT="${NPP_FILE_EXT:-txt}"

case "$COMMAND" in
  select-and-launch|select-and-open)
    INPUT=$(cat)
    TMPFILE=$(mktemp /tmp/npp-select-launch-XXXXXX."$FILE_EXT")
    echo "$INPUT" > "$TMPFILE"
    open "$TMPFILE"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

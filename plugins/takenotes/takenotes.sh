#!/bin/bash
# TakeNotes — macOS native plugin stub for NotepadMac
# Full implementation needs native NSTextView note panel + storage

COMMAND="$1"
# NPP_NOTES_DIR: directory for notes
NOTES_DIR="${NPP_NOTES_DIR:-$HOME/.notepadmac/notes}"

case "$COMMAND" in
  new-note)
    mkdir -p "$NOTES_DIR"
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
    NOTEFILE="$NOTES_DIR/note_${TIMESTAMP}.txt"
    touch "$NOTEFILE"
    echo "$NOTEFILE"
    ;;
  open-last-note)
    if [ -d "$NOTES_DIR" ]; then
        LAST=$(ls -t "$NOTES_DIR"/note_*.txt 2>/dev/null | head -1)
        if [ -n "$LAST" ]; then
            cat "$LAST"
        else
            echo "No notes found" >&2
        fi
    else
        echo "Notes directory not found: $NOTES_DIR" >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

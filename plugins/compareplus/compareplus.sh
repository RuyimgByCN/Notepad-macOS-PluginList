#!/bin/bash
# ComparePlus — macOS native plugin stub for NotepadMac
# Full implementation needs native dual-panel diff view UI

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  compare-selected|diff-files)
    # Basic diff using system diff command
    # For dual-panel view, native Swift UI is needed
    INPUT=$(cat)
    if [ -n "$FILE" ]; then
        TMPFILE=$(mktemp /tmp/npp-diff-XXXXXX)
        echo "$INPUT" > "$TMPFILE"
        diff -u "$FILE" "$TMPFILE" 2>&1 || true
        rm -f "$TMPFILE"
    else
        echo "Compare needs two inputs — full dual-panel UI pending native implementation" >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

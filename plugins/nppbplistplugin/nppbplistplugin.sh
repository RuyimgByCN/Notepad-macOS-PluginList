#!/bin/bash
# Notepad++ bplist plugin — macOS native port for NotepadMac
# Uses macOS native plutil for plist conversion

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  convert-bplist-to-xml)
    if [ -n "$FILE" ]; then
        plutil -convert xml1 -o - "$FILE" 2>&1
    else
        # Convert stdin
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -convert xml1 -o - "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  convert-bplist-to-json)
    if [ -n "$FILE" ]; then
        plutil -convert json -o - "$FILE" 2>&1
    else
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -convert json -o - "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  view-bplist-info)
    if [ -n "$FILE" ]; then
        plutil -p "$FILE" 2>&1
    else
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -p "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

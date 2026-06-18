#!/bin/bash
# SpeechPlugin — macOS native plugin for NotepadMac
# Uses macOS built-in 'say' command for text-to-speech

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  speak-selection)
    INPUT=$(cat)
    say "$INPUT" &
    ;;
  speak-document)
    if [ -n "$FILE" ] && [ -f "$FILE" ]; then
        say -f "$FILE" &
    else
        INPUT=$(cat)
        say "$INPUT" &
    fi
    ;;
  stop-speaking)
    # Kill any running say process
    killall say 2>/dev/null
    echo "Stopped speaking"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# NppVim — macOS native plugin stub for NotepadMac
# Full implementation needs Vim mode state machine + key binding layer

COMMAND="$1"

case "$COMMAND" in
  toggle-vim-mode)
    echo "Vim mode requires native Swift key-binding implementation" >&2
    echo "This is a stub — pending native key event interception layer." >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

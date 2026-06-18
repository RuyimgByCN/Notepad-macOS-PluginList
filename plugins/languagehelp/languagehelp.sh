#!/bin/bash
# LanguageHelp — macOS native plugin stub for NotepadMac
# Full implementation needs native help viewer integration

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"
# NPP_HELP_FILE: path to help file for current language
HELP_FILE="${NPP_HELP_FILE:-}"
# NPP_HELP_KEYWORD: keyword under cursor
KEYWORD="${NPP_HELP_KEYWORD:-}"

case "$COMMAND" in
  lookup-keyword)
    if [ -n "$HELP_FILE" ] && [ -f "$HELP_FILE" ]; then
        open "$HELP_FILE"
    elif [ -n "$KEYWORD" ]; then
        # Try online search as fallback
        open "https://devdocs.io/search?q=${KEYWORD}"
    else
        echo "No help file configured. Set NPP_HELP_FILE environment variable." >&2
    fi
    ;;
  open-help-file)
    if [ -n "$HELP_FILE" ] && [ -f "$HELP_FILE" ]; then
        open "$HELP_FILE"
    else
        echo "No help file configured for current language." >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

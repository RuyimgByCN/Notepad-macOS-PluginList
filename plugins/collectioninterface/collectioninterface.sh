#!/bin/bash
# CollectionInterface — macOS native plugin stub for NotepadMac
# Full implementation needs URLSession download + JSON parsing + native install UI

COMMAND="$1"

case "$COMMAND" in
  download-udl-list)
    curl -s "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/UDL-list.json" 2>/dev/null || echo "Failed to download UDL list" >&2
    ;;
  download-theme-list)
    curl -s "https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/master/themes-list.json" 2>/dev/null || echo "Failed to download theme list" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

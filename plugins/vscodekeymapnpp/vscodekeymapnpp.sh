#!/bin/bash
# VSCode Keymap — macOS native plugin stub for NotepadMac
# Full implementation needs native Swift key binding translation

COMMAND="$1"

case "$COMMAND" in
  enable-vscode-keymap)
    echo "VS Code keymap requires native key binding implementation" >&2
    echo "This is a stub — pending Swift key event mapping layer." >&2
    ;;
  disable-vscode-keymap)
    echo "VS Code keymap disabled stub — pending native implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

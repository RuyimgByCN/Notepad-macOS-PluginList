#!/bin/bash
# NotepadMac Plugin Demo — macOS native demo plugin
# Demonstrates the plugin API: manifest format, command handling, stdin/stdout

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  hello-world)
    echo "Hello from NotepadMac Plugin Demo!"
    ;;
  show-info)
    echo "NotepadMac Plugin Demo v1.0.0"
    echo "Commands: hello-world, show-info, count-words"
    echo "Plugin API: read stdin, write stdout, use NOTEPAD_MAC_EDIT_SCRIPT_FILE for file path"
    ;;
  count-words)
    python3 -c "
import sys
text = sys.stdin.read()
words = text.split()
print(f'Words: {len(words)}, Characters: {len(text)}, Lines: {len(text.split(chr(10)))}')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

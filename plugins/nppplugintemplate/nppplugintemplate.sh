#!/bin/bash
# NotepadMac Plugin Template — starting point for new plugins
# Copy this directory and modify:
#   1. notepad-mac-plugin.json — change identifier, name, commands
#   2. This script — implement your command logic

COMMAND="$1"

case "$COMMAND" in
  template-command)
    # Replace this with your implementation
    # Read from stdin, process, write to stdout
    INPUT=$(cat)
    echo "Template received: $INPUT"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

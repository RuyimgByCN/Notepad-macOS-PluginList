#!/bin/bash
# Pork to Sausage — macOS native plugin for NotepadMac
# Pass selected text to a command-line program and replace with output

COMMAND="$1"
# NPP_PIPE_CMD environment variable should be set by user configuration
# Default to sort if not configured
PIPE_CMD="${NPP_PIPE_CMD:-sort}"

case "$COMMAND" in
  pipe-to-command)
    # Read stdin, pass to the configured command, output result
    INPUT=$(cat)
    echo "$INPUT" | eval "$PIPE_CMD"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

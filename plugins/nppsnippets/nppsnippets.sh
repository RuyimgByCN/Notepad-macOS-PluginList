#!/bin/bash
# Snippets — macOS native plugin stub for NotepadMac
# Full implementation needs NSTableView panel + JSON/YAML snippet storage

COMMAND="$1"
# NPP_SNIPPETS_DIR: directory containing snippet files
SNIPPETS_DIR="${NPP_SNIPPETS_DIR:-$HOME/.notepadmac/snippets}"
# NPP_SNIPPET_NAME: name of snippet to insert
SNIPPET_NAME="${NPP_SNIPPET_NAME:-}"

case "$COMMAND" in
  insert-snippet)
    if [ -z "$SNIPPET_NAME" ]; then
        echo "Error: Set NPP_SNIPPET_NAME environment variable" >&2
        exit 1
    fi
    SNIPPET_FILE="$SNIPPETS_DIR/${SNIPPET_NAME}.txt"
    if [ -f "$SNIPPET_FILE" ]; then
        cat "$SNIPPET_FILE"
    else
        echo "Error: Snippet '$SNIPPET_NAME' not found in $SNIPPETS_DIR" >&2
        exit 1
    fi
    ;;
  list-snippets)
    if [ -d "$SNIPPETS_DIR" ]; then
        for f in "$SNIPPETS_DIR"/*.txt; do
            [ -f "$f" ] && basename "$f" .txt
        done
    else
        echo "No snippets directory: $SNIPPETS_DIR" >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

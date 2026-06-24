#!/bin/bash
# NppFavorites — macOS native plugin for NotepadMac
# Converted from upstream NppFavorites (v1.0.0.1, x64)

COMMAND="$1"

case "$COMMAND" in
  list-favorites)
    echo "Favorites panel requires native UI and persistent storage — pending implementation" >&2
    ;;
  add-favorite)
    echo "Adding favorites requires native panel UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# NppMenuSearch — macOS native plugin for NotepadMac
# Converted from upstream NppMenuSearch (v0.9.7, x64)

COMMAND="$1"

case "$COMMAND" in
  search-menus)
    echo "Menu search requires native toolbar integration — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

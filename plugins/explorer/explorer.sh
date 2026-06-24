#!/bin/bash
# Explorer — macOS native plugin for NotepadMac
# Converted from upstream Explorer (v1.9.9.0, x64)

COMMAND="$1"

case "$COMMAND" in
  list-directory)
    ls -la
    ;;
  current-path)
    pwd
    ;;
  browse-tree)
    echo "Folder tree browser requires native NSOutlineView UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# Virtual Folders — macOS native plugin stub for NotepadMac
# Full implementation needs NSTreeController + NSOutlineView panel

COMMAND="$1"

case "$COMMAND" in
  open-virtual-folders)
    echo "Virtual Folders requires native NSOutlineView panel UI — pending implementation" >&2
    echo "Similar to existing Workspace panel architecture." >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

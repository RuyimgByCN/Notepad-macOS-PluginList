#!/bin/bash
# File Switcher — macOS native plugin for NotepadMac
# Converted from upstream FileSwitcher (v1.0.3.0, x86)

COMMAND="$1"

case "$COMMAND" in
  list-buffers)
    echo "Listing open buffers requires editor API integration — pending implementation" >&2
    ;;
  switch-buffer)
    echo "Buffer switcher panel requires native UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

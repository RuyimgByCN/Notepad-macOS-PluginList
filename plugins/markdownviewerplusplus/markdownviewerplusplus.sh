#!/bin/bash
# MarkdownViewer++ — macOS native plugin for NotepadMac
# Converted from upstream MarkdownViewerPlusPlus (v0.8.2, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  extract-markdown)
    python3 -c "
import sys
sys.stdout.write(sys.stdin.read())
    "
    ;;
  render-preview)
    echo "Live Markdown rendering requires native WKWebView — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

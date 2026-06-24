#!/bin/bash
# GitSCM — macOS native plugin for NotepadMac
# Converted from upstream GitSCM (v1.4.10.1, x64)

COMMAND="$1"

if ! command -v git > /dev/null 2>&1; then
    echo "Error: git is required. Install: install from https://git-scm.com" >&2
    exit 1
fi

case "$COMMAND" in
  git-status)
    git status -s 2>/dev/null || echo 'Not a git repository' >&2
    ;;
  git-branch)
    git branch --show-current 2>/dev/null || echo 'Not a git repository' >&2
    ;;
  git-log)
    git log --oneline -10 2>/dev/null || echo 'Not a git repository' >&2
    ;;
  full-gui)
    echo "Full Git GUI panel requires native UI — pending implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

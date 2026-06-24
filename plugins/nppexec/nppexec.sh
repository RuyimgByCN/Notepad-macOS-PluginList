#!/bin/bash
# NppExec — macOS native plugin for NotepadMac
# Converted from upstream NppExec (v0.8.10, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  exec-command)
    python3 -c "
import sys, subprocess
cmd = sys.stdin.read()
r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
sys.stdout.write(r.stdout); sys.stderr.write(r.stderr); sys.exit(r.returncode)
    "
    ;;
  echo-selection)
    python3 -c "
import sys
sys.stdout.write(sys.stdin.read())
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# Code Alignment — macOS native plugin for NotepadMac
# Converted from upstream CodeAlignmentNpp (v14.1.107, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  align-equals)
    python3 -c "
import sys
lines = sys.stdin.read().splitlines()
maxlen = 0
parts = []
for ln in lines:
    idx = ln.find('=')
    parts.append((ln[:idx], ln[idx:]) if idx >= 0 else (ln, ''))
    if idx > maxlen: maxlen = idx
for left, right in parts:
    print(left.rstrip() + ' ' * (maxlen - len(left.rstrip())) + right)
    "
    ;;
  align-spaces)
    python3 -c "
import sys
rows = [ln.split() for ln in sys.stdin.read().splitlines()]
if not rows: sys.exit(0)
ncols = max(len(r) for r in rows)
widths = [0] * ncols
for r in rows:
    for i, w in enumerate(r): widths[i] = max(widths[i], len(w))
for r in rows:
    print(' '.join(r[i].ljust(widths[i]) if i < len(r) else ''.ljust(widths[i]) for i in range(ncols)).rstrip())
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

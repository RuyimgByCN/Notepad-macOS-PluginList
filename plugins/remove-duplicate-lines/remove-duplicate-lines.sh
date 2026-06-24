#!/bin/bash
# Remove Duplicate Lines — macOS native plugin for NotepadMac
# Converted from upstream Remove Duplicate Lines (v1.3.0.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  remove-dups)
    python3 -c "
import sys
seen = set(); out = []
for ln in sys.stdin.read().splitlines(True):
    if ln not in seen:
        seen.add(ln); out.append(ln)
sys.stdout.write(''.join(out))
    "
    ;;
  sort-unique)
    python3 -c "
import sys
sys.stdout.write(''.join(sorted(set(sys.stdin.read().splitlines(True)))))
    "
    ;;
  count-duplicates)
    python3 -c "
import sys, collections
c = collections.Counter(sys.stdin.read().splitlines())
print('Total lines:', sum(c.values()))
print('Unique:', len(c))
print('Duplicates:', sum(1 for v in c.values() if v > 1))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

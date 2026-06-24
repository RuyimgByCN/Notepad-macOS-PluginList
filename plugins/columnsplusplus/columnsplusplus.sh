#!/bin/bash
# Columns++ — macOS native plugin for NotepadMac
# Converted from upstream ColumnsPlusPlus (v1.3.1, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  align-columns)
    python3 -c "
import sys, re
lines = sys.stdin.read().splitlines()
split = [re.split(r'\s+', ln.strip()) for ln in lines if ln.strip()]
if not split: sys.exit(0)
nc = max(len(s) for s in split)
w = [0] * nc
for s in split:
    for i, x in enumerate(s): w[i] = max(w[i], len(x))
for s in split:
    print('  '.join(s[i].ljust(w[i]) if i < len(s) else ''.ljust(w[i]) for i in range(nc)).rstrip())
    "
    ;;
  column-info)
    python3 -c "
import sys, re
lines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
if not lines: print('Empty'); sys.exit(0)
counts = [len(re.split(r'\s+', ln.strip())) for ln in lines]
print(f'Rows: {len(lines)}, min cols: {min(counts)}, max cols: {max(counts)}, consistent: {len(set(counts)) == 1}')
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

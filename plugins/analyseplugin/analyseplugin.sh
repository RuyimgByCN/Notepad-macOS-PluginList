#!/bin/bash
# AnalysePlugin — macOS native plugin for NotepadMac
# Converted from upstream AnalysePlugin (v1.13.49.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  word-frequency)
    python3 -c "
import sys, collections, re
words = re.findall(r'\w+', sys.stdin.read().lower())
for w, n in collections.Counter(words).most_common(20):
    print(f'{n:6d}  {w}')
    "
    ;;
  line-stats)
    python3 -c "
import sys
data = sys.stdin.read()
lines = data.splitlines()
words = data.split()
print(f'Lines: {len(lines)}')
print(f'Words: {len(words)}')
print(f'Characters: {len(data)}')
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

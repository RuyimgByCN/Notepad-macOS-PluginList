#!/bin/bash
# DSpellCheck — macOS native plugin for NotepadMac
# Converted from upstream DSpellCheck (v1.5.0, x64)

COMMAND="$1"

if ! command -v hunspell > /dev/null 2>&1; then
    echo "Error: hunspell is required. Install: brew install hunspell" >&2
    exit 1
fi

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  list-misspellings)
    hunspell -l | sort -u
    ;;
  count-errors)
    python3 -c "
import sys, subprocess
r = subprocess.run(['hunspell', '-l'], input=sys.stdin.read(), text=True, capture_output=True)
words = sorted(set(w for w in r.stdout.split() if w))
print(f'Misspelled unique words: {len(words)}')
for w in words: print(w)
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

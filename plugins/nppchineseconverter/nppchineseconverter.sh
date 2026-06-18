#!/bin/bash
# Chinese Converter — macOS native plugin for NotepadMac
# Uses OpenCC for Traditional/Simplified Chinese conversion

COMMAND="$1"
INPUT=$(cat)

# Check if opencc is available
if ! command -v opencc &> /dev/null; then
    echo "Error: opencc is not installed. Install with: brew install opencc" >&2
    echo "$INPUT"
    exit 1
fi

case "$COMMAND" in
  t2s)
    opencc -f t2s.json -i /dev/stdin <<< "$INPUT"
    ;;
  s2t)
    opencc -f s2t.json -i /dev/stdin <<< "$INPUT"
    ;;
  t2tw)
    opencc -f t2tw.json -i /dev/stdin <<< "$INPUT"
    ;;
  tw2t)
    opencc -f tw2t.json -i /dev/stdin <<< "$INPUT"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# WebEdit — macOS native plugin for NotepadMac
# HTML tag abbreviation expansion and wrapping

COMMAND="$1"
if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi
# NPP_WEBEDIT_TAG environment variable for the tag name
TAG="${NPP_WEBEDIT_TAG:-div}"

case "$COMMAND" in
  expand-tag)
    INPUT=$(cat)
    # Expand abbreviation: input text is the tag name
    TAGNAME="$INPUT"
    TAGNAME=$(echo "$TAGNAME" | xargs)  # trim whitespace
    echo "<${TAGNAME}></${TAGNAME}>"
    ;;
  wrap-selection)
    INPUT=$(cat)
    echo "<${TAG}>${INPUT}</${TAG}>"
    ;;
  remove-tag)
    python3 -c "
import sys, re
text = sys.stdin.read()
# Remove opening and closing tags, keep content
text = re.sub(r'<[^>]+>', '', text)
print(text)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

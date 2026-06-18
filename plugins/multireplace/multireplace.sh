#!/bin/bash
# MultiReplace — macOS native plugin stub for NotepadMac
# Full multi-rule UI needs native Find/Replace panel extension

COMMAND="$1"
if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi
# NPP_REPLACE_RULES: newline-separated "pattern→replacement" pairs
RULES="${NPP_REPLACE_RULES:-}"

case "$COMMAND" in
  multi-replace|apply-replace-list)
    if [ -z "$RULES" ]; then
        echo "Error: NPP_REPLACE_RULES not set. Format: pattern1→replacement1\\npattern2→replacement2" >&2
        exit 1
    fi
    python3 -c "
import sys, re, os

text = sys.stdin.read()
rules_str = os.environ.get('NPP_REPLACE_RULES', '')

for rule in rules_str.split('\n'):
    if not rule:
        continue
    parts = rule.split('→', 1)
    if len(parts) != 2:
        continue
    pattern, replacement = parts
    text = re.sub(pattern, replacement, text)

print(text)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

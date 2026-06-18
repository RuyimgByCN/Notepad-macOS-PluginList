#!/bin/bash
# Auto Detect Indention — macOS native plugin for NotepadMac
# Detects whether the file uses tabs or spaces for indentation

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  detect-indent)
    # Analyze stdin text for indentation patterns
    python3 -c "
import sys, re

text = sys.stdin.read()
lines = text.split('\n')

tab_lines = 0
space_lines = 0
space_counts = []

for line in lines:
    if not line or line[0] not in (' ', '\t'):
        continue
    if line[0] == '\t':
        tab_lines += 1
    else:
        m = re.match(r'( +)', line)
        if m:
            space_lines += 1
            space_counts.append(len(m.group(1)))

total = tab_lines + space_lines
if total == 0:
    print('NO_INDENT')
    sys.exit(0)

if tab_lines > space_lines:
    print('TAB')
else:
    # Determine most common space width
    if space_counts:
        from collections import Counter
        common = Counter(space_counts).most_common(1)[0][0]
        print(f'SPACE_{common}')
    else:
        print('SPACE_4')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

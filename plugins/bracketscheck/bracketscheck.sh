#!/bin/bash
# BracketsCheck — macOS native plugin for NotepadMac
# Converted from upstream BracketsCheck (v1.2.2, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  check-balance)
    python3 -c "
import sys
pairs = {'(': ')', '[': ']', '{': '}'}; close = set(pairs.values())
stack = []; errs = []
for i, ch in enumerate(sys.stdin.read()):
    if ch in pairs: stack.append((ch, i))
    elif ch in close:
        if not stack or pairs[stack[-1][0]] != ch:
            errs.append(f'Unexpected {ch!r} at {i}')
        else: stack.pop()
for ch, i in stack: errs.append(f'Unclosed {ch!r} at {i}')
print('OK — balanced.' if not errs else '\n'.join(errs))
if errs: sys.exit(1)
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

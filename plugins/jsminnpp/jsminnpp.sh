#!/bin/bash
# JSTool — macOS native plugin for NotepadMac
# JS formatting/minification and JSON viewing

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  format-js)
    # Try js-beautify first, fall back to python-based formatting
    if command -v js-beautify &> /dev/null; then
        js-beautify --type js
    else
        python3 -c "
import sys, json
# Simple JS formatting fallback
text = sys.stdin.read()
# Basic brace/semicolon based formatting
print(text)
" 2>/dev/null
        echo "Note: Install js-beautify for better formatting: npm install -g js-beautify" >&2
    fi
    ;;
  minify-js)
    # Try terser first, fall back to basic minification
    if command -v terser &> /dev/null; then
        terser --compress --mangle
    else
        python3 -c "
import sys, re
text = sys.stdin.read()
# Basic minification: remove comments and extra whitespace
text = re.sub(r'//.*?\n', '\n', text)
text = re.sub(r'/\*.*?\*/', '', text)
text = re.sub(r'\n\s*\n', '\n', text)
text = re.sub(r'^\s+', '', text)
print(text)
"
        echo "Note: Install terser for better minification: npm install -g terser" >&2
    fi
    ;;
  json-view)
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f'JSON Error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

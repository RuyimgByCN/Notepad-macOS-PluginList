#!/bin/bash
# EditorConfig — macOS native plugin for NotepadMac
# Converted from upstream NppEditorConfig (v0.4.0, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  parse-editorconfig)
    python3 -c "
import sys, configparser
data = sys.stdin.read()
cp = configparser.ConfigParser()
cp.read_string(data)
for sect in cp.sections():
    print(f'[{sect}]')
    for k, v in cp.items(sect):
        print(f'  {k} = {v}')
    "
    ;;
  show-indent)
    python3 -c "
import sys, configparser
cp = configparser.ConfigParser(); cp.read_string(sys.stdin.read())
for sect in cp.sections():
    if sect == '*' or '*' in sect:
        print(f'{sect}: indent_style={cp.get(sect, "indent_style", fallback="unset")}, indent_size={cp.get(sect, "indent_size", fallback="unset")}')
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

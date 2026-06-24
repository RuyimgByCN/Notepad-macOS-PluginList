#!/bin/bash
# XML Tools — macOS native plugin for NotepadMac
# Converted from upstream XMLTools (v3.1.1.13, x64)

COMMAND="$1"

if ! command -v xmllint > /dev/null 2>&1; then
    echo "Error: xmllint is required. Install: preinstalled on macOS (libxml2)" >&2
    exit 1
fi

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  format-xml)
    xmllint --format -
    ;;
  validate-xml)
    python3 -c "
import sys
from xml.dom import minidom
data = sys.stdin.read()
try:
    minidom.parseString(data)
    print('XML is well-formed.')
except Exception as e:
    print('XML error:', e, file=sys.stderr)
    sys.exit(1)
    "
    ;;
  escape-xml)
    python3 -c "
import sys
s = sys.stdin.read()
print(s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# XPatherizerNPP — macOS native plugin for NotepadMac
# Converted from upstream XPatherizerNPP (v2.10, x86)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  list-elements)
    python3 -c "
import sys
from xml.etree import ElementTree as ET
data = sys.stdin.read()
try:
    root = ET.fromstring(data)
    tags = sorted({el.tag for el in root.iter()})
    print('\n'.join(tags))
except Exception as e:
    print('Parse error:', e, file=sys.stderr); sys.exit(1)
    "
    ;;
  count-elements)
    python3 -c "
import sys
from xml.etree import ElementTree as ET
data = sys.stdin.read()
try:
    root = ET.fromstring(data)
    print(sum(1 for _ in root.iter()))
except Exception as e:
    print('Parse error:', e, file=sys.stderr); sys.exit(1)
    "
    ;;
  xpath-query)
    echo "XPath query execution needs an expression input UI — pending native implementation" >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

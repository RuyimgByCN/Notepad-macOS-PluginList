#!/bin/bash
# PlantUML Viewer — macOS native plugin for NotepadMac
# Converted from upstream PlantUmlViewer (v1.9.0.13, x64)

COMMAND="$1"

if ! command -v plantuml > /dev/null 2>&1; then
    echo "Error: plantuml is required. Install: brew install plantuml" >&2
    exit 1
fi

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  extract-diagrams)
    python3 -c "
import sys, re
blocks = re.findall(r'@startuml.*?@enduml', sys.stdin.read(), re.S)
print('\n\n'.join(blocks) if blocks else '(no @startuml blocks found)')
    "
    ;;
  validate-syntax)
    python3 -c "
import sys, re
data = sys.stdin.read()
starts = len(re.findall(r'@startuml', data)); ends = len(re.findall(r'@enduml', data))
if starts == ends and starts > 0: print(f'OK — {starts} balanced diagram block(s).')
elif starts == 0: print('No @startuml found.')
else: print(f'Mismatch: {starts} @startuml vs {ends} @enduml', file=sys.stderr); sys.exit(1)
    "
    ;;
  render-to-file)
    echo "Rendering requires java + plantuml.jar — run: plantuml -tpng <file>. Needs native preview UI." >&2
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

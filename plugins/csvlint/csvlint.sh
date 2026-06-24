#!/bin/bash
# CSV Lint — macOS native plugin for NotepadMac
# Converted from upstream CSVLint (v0.4.8, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  validate-csv)
    python3 -c "
import sys, csv
rows = list(csv.reader(sys.stdin))
if not rows:
    print('Empty'); sys.exit(0)
n = len(rows[0]); bad = [i+1 for i, r in enumerate(rows) if len(r) != n]
print(f'Rows: {len(rows)}, Columns: {n}')
print('Inconsistent rows:', bad if bad else 'none')
if bad: sys.exit(1)
    "
    ;;
  csv-to-json)
    python3 -c "
import sys, csv, json
rows = list(csv.reader(sys.stdin))
if not rows: print('[]'); sys.exit(0)
hdr = rows[0]
print(json.dumps([dict(zip(hdr, r)) for r in rows[1:]], indent=2, ensure_ascii=False))
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

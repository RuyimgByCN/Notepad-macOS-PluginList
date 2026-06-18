#!/bin/bash
# Markdown Table Editor — macOS native plugin stub for NotepadMac
# Full interactive editing needs NSTableView UI

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  align-table|format-table)
    python3 -c "
import sys, re

text = sys.stdin.read()
lines = text.strip().split('\n')
if len(lines) < 2:
    print(text)
    sys.exit(0)

# Parse pipe-delimited table
rows = []
for line in lines:
    if line.strip().startswith('|'):
        cells = [c.strip() for c in line.strip().split('|') if c.strip()]
        rows.append(cells)

if not rows:
    print(text)
    sys.exit(0)

# Calculate column widths
ncols = max(len(r) for r in rows)
widths = [0] * ncols
for row in rows:
    for i, cell in enumerate(row):
        if i < ncols:
            widths[i] = max(widths[i], len(cell))

# Format aligned table
result = []
for idx, row in enumerate(rows):
    padded = []
    for i in range(ncols):
        cell = row[i] if i < len(row) else ''
        padded.append(cell.ljust(widths[i]))
    result.append('| ' + ' | '.join(padded) + ' |')
    if idx == 0:
        # Add separator row
        sep = ['-' * widths[i] for i in range(ncols)]
        result.append('| ' + ' | '.join(sep) + ' |')

print('\n'.join(result))
"
    ;;
  csv-to-table)
    python3 -c "
import sys, csv, io

text = sys.stdin.read()
reader = csv.reader(io.StringIO(text))
rows = list(reader)

if not rows:
    print('No CSV data')
    sys.exit(1)

# Calculate widths
ncols = max(len(r) for r in rows)
widths = [0] * ncols
for row in rows:
    for i, cell in enumerate(row):
        if i < ncols:
            widths[i] = max(widths[i], len(cell))

# Build markdown table
result = []
for idx, row in enumerate(rows):
    padded = []
    for i in range(ncols):
        cell = row[i] if i < len(row) else ''
        padded.append(cell.ljust(widths[i]))
    result.append('| ' + ' | '.join(padded) + ' |')
    if idx == 0:
        sep = ['-' * widths[i] for i in range(ncols)]
        result.append('| ' + ' | '.join(sep) + ' |')

print('\n'.join(result))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

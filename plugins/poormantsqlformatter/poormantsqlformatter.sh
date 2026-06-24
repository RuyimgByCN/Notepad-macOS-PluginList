#!/bin/bash
# Poor Man's T-Sql Formatter — macOS native plugin for NotepadMac
# Converted from upstream PoorMansTSqlFormatterNppPlugin (v1.6.13.31508, x64)

COMMAND="$1"

if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: python3 is required but not installed." >&2
    exit 1
fi

case "$COMMAND" in
  format-sql)
    python3 -c "
import sys
sql = sys.stdin.read()
try:
    import sqlparse
    print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
except ImportError:
    kw = ('SELECT','FROM','WHERE','AND','OR','ORDER BY','GROUP BY','LEFT JOIN','INNER JOIN','ON','SET','INSERT INTO','VALUES','UPDATE','DELETE')
    out = sql
    for k in kw:
        out = out.replace(k.lower(), k).replace(k.capitalize(), k)
    import re
    out = re.sub(r'\s+', ' ', out).strip()
    print(out)
    "
    ;;
  minify-sql)
    python3 -c "
import sys, re
print(re.sub(r'\s+', ' ', sys.stdin.read()).strip())
    "
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

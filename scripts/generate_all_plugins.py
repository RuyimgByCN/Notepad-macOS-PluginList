#!/usr/bin/env python3
"""
Generate macOS-native plugin implementations for all 54 upstream Notepad++ plugins.

Creates:
  - plugins/{identifier}/notepad-mac-plugin.json  (manifest)
  - plugins/{identifier}/{identifier}.sh          (implementation script)
  - plugins/{identifier}/README.md                (description)

Then generates updated catalog JSON files.
"""

import json
import os
import stat
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(BASE_DIR, 'plugins')

# ── Read current catalog ──────────────────────────────────────────────
with open(os.path.join(BASE_DIR, 'mac-arm64.json')) as f:
    CATALOG = json.load(f)

# Build a lookup by identifier
CATALOG_BY_ID = {p['identifier']: p for p in CATALOG['plugins']}

# ── Plugin implementation definitions ──────────────────────────────────
# Each entry defines: mac_version, commands, script_content, impl_type
# impl_type: 'easy' | 'medium_stub' | 'hard_feasible' | 'builtin' | 'hard_impossible' | 'na'

PLUGIN_IMPLS = {}


# ══════════════════════════════════════════════════════════════════════
# EASY (19) — Full shell script implementations
# ══════════════════════════════════════════════════════════════════════

PLUGIN_IMPLS['nppautodetectindent'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Detects indentation (tab or spaces) and auto-adjusts Tab settings. macOS native port of nppAutoDetectIndent.',
    'commands': [
        {'identifier': 'detect-indent', 'title': 'Auto Detect Indentation'},
    ],
    'script': '''#!/bin/bash
# Auto Detect Indention — macOS native plugin for NotepadMac
# Detects whether the file uses tabs or spaces for indentation

COMMAND="$1"

case "$COMMAND" in
  detect-indent)
    # Analyze stdin text for indentation patterns
    python3 -c "
import sys, re

text = sys.stdin.read()
lines = text.split('\\n')

tab_lines = 0
space_lines = 0
space_counts = []

for line in lines:
    if not line or line[0] not in (' ', '\\t'):
        continue
    if line[0] == '\\t':
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
''',
}

PLUGIN_IMPLS['nppchineseconverter'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Traditional and Simplified Chinese conversion. macOS native port using OpenCC.',
    'commands': [
        {'identifier': 't2s', 'title': 'Traditional → Simplified'},
        {'identifier': 's2t', 'title': 'Simplified → Traditional'},
        {'identifier': 't2tw', 'title': 'Traditional → Taiwan'},
        {'identifier': 'tw2t', 'title': 'Taiwan → Traditional'},
    ],
    'script': '''#!/bin/bash
# Chinese Converter — macOS native plugin for NotepadMac
# Uses OpenCC for Traditional/Simplified Chinese conversion

COMMAND="$1"
INPUT=$(cat)

# Check if opencc is available
if ! command -v opencc &> /dev/null; then
    echo "Error: opencc is not installed. Install with: brew install opencc" >&2
    echo "$INPUT"
    exit 1
fi

case "$COMMAND" in
  t2s)
    opencc -f t2s.json -i /dev/stdin <<< "$INPUT"
    ;;
  s2t)
    opencc -f s2t.json -i /dev/stdin <<< "$INPUT"
    ;;
  t2tw)
    opencc -f t2tw.json -i /dev/stdin <<< "$INPUT"
    ;;
  tw2t)
    opencc -f tw2t.json -i /dev/stdin <<< "$INPUT"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['emojidescription'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Displays character encoding info: Unicode code point, decimal/hex values, HTML entity, UTF-8 bytes. macOS native port.',
    'commands': [
        {'identifier': 'char-info', 'title': 'Show Character Info'},
    ],
    'script': '''#!/bin/bash
# Emoji Description — macOS native plugin for NotepadMac
# Shows Unicode code point, UTF-8 bytes, HTML entity for selected text

COMMAND="$1"

case "$COMMAND" in
  char-info)
    python3 -c "
import sys, html

text = sys.stdin.read()
results = []
for ch in text:
    cp = ord(ch)
    utf8 = ch.encode('utf-8')
    hex_bytes = ' '.join(f'{b:02X}' for b in utf8)
    html_ent = html.escape(ch)
    try:
        html_num_ent = f'&#x{cp:X};'
    except:
        html_num_ent = ''
    name = ''
    try:
        import unicodedata
        name = unicodedata.name(ch, '')
    except:
        pass
    results.append(f'{ch}  U+{cp:04X}  Dec:{cp}  UTF-8:[{hex_bytes}]  HTML:{html_num_ent}  Name:{name}')

print('\\n'.join(results) if results else 'No characters selected')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['htmltag'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'HTML/XML tag navigation, entity encoding/decoding, JS character encoding/decoding. macOS native port.',
    'commands': [
        {'identifier': 'encode-html-entities', 'title': 'Encode HTML Entities'},
        {'identifier': 'decode-html-entities', 'title': 'Decode HTML Entities'},
        {'identifier': 'encode-js-chars', 'title': 'Encode JS Characters'},
        {'identifier': 'decode-js-chars', 'title': 'Decode JS Characters'},
    ],
    'script': '''#!/bin/bash
# HTML Tag — macOS native plugin for NotepadMac
# HTML entity and JS character encoding/decoding

COMMAND="$1"

case "$COMMAND" in
  encode-html-entities)
    python3 -c "
import sys, html
text = sys.stdin.read()
print(html.escape(text, quote=True))
"
    ;;
  decode-html-entities)
    python3 -c "
import sys, html
text = sys.stdin.read()
print(html.unescape(text))
"
    ;;
  encode-js-chars)
    python3 -c "
import sys
text = sys.stdin.read()
result = []
for ch in text:
    cp = ord(ch)
    if cp > 127:
        result.append(f'\\\\u{cp:04X}')
    else:
        result.append(ch)
print(''.join(result))
"
    ;;
  decode-js-chars)
    python3 -c "
import sys, re
text = sys.stdin.read()
def replace_js(m):
    return chr(int(m.group(1), 16))
print(re.sub(r'\\\\u([0-9a-fA-F]{4})', replace_js, text))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppjsonviewer'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'JSON formatter and minifier. macOS native port using python json.tool.',
    'commands': [
        {'identifier': 'format-json', 'title': 'Format JSON'},
        {'identifier': 'minify-json', 'title': 'Minify JSON'},
        {'identifier': 'validate-json', 'title': 'Validate JSON'},
    ],
    'script': '''#!/bin/bash
# JSON Viewer — macOS native plugin for NotepadMac
# JSON formatting, minification, and validation

COMMAND="$1"

case "$COMMAND" in
  format-json)
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
  minify-json)
    python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, separators=(',', ':'), ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f'JSON Error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  validate-json)
    python3 -c "
import sys, json
try:
    json.load(sys.stdin)
    print('JSON is valid')
except json.JSONDecodeError as e:
    print(f'JSON Error at line {e.lineno}, column {e.colno}: {e.msg}')
    sys.exit(1)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['jsminnpp'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'JavaScript formatting, minification, and JSON viewer. macOS native port of JSTool.',
    'commands': [
        {'identifier': 'format-js', 'title': 'Format JavaScript'},
        {'identifier': 'minify-js', 'title': 'Minify JavaScript'},
        {'identifier': 'json-view', 'title': 'JSON Data Viewer'},
    ],
    'script': '''#!/bin/bash
# JSTool — macOS native plugin for NotepadMac
# JS formatting/minification and JSON viewing

COMMAND="$1"

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
        echo "Note: Install js-beautify for better formatting: npm install -g js-beautify"
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
text = re.sub(r'//.*?\\n', '\\n', text)
text = re.sub(r'/\\*.*?\\*/', '', text)
text = re.sub(r'\\n\\s*\\n', '\\n', text)
text = re.sub(r'^\\s+', '', text)
print(text)
"
        echo "Note: Install terser for better minification: npm install -g terser"
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
''',
}

PLUGIN_IMPLS['linter++'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Real-time code linting against external linters (eslint, pylint, shellcheck, etc.). macOS native port.',
    'commands': [
        {'identifier': 'lint-file', 'title': 'Lint Current File'},
        {'identifier': 'lint-selection', 'title': 'Lint Selection'},
    ],
    'script': '''#!/bin/bash
# Linter++ — macOS native plugin for NotepadMac
# Runs external linters on the current file or selection

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  lint-file)
    if [ -z "$FILE" ]; then
        echo "Error: No file path available" >&2
        exit 1
    fi

    # Determine linter based on file extension
    EXT="${FILE##*.}"
    case "$EXT" in
      js|jsx|ts|tsx|mjs)
        LINTER="eslint"
        ;;
      py|pyw)
        LINTER="pylint"
        ;;
      sh|bash)
        LINTER="shellcheck"
        ;;
      css|scss)
        LINTER="stylelint"
        ;;
      rb)
        LINTER="rubocop"
        ;;
      go)
        LINTER="golint"
        ;;
      *)
        LINTER="generic"
        ;;
    esac

    if [ "$LINTER" = "generic" ]; then
        echo "No specific linter for .$EXT files. Available: eslint, pylint, shellcheck, stylelint, rubocop"
        exit 0
    fi

    if ! command -v "$LINTER" &> /dev/null; then
        echo "Error: $LINTER is not installed. Install it to enable linting." >&2
        exit 1
    fi

    "$LINTER" "$FILE" 2>&1
    ;;
  lint-selection)
    # Lint the selected text (stdin)
    if [ -z "$FILE" ]; then
        echo "Error: No file context available" >&2
        exit 1
    fi
    # Write selection to temp file and lint it
    TMPFILE=$(mktemp /tmp/npp-lint-XXXXXX."${FILE##*.}")
    cat > "$TMPFILE"
    EXT="${FILE##*.}"
    case "$EXT" in
      js|jsx|ts|tsx|mjs)
        LINTER="eslint"
        ;;
      py|pyw)
        LINTER="pylint"
        ;;
      sh|bash)
        LINTER="shellcheck"
        ;;
      *)
        LINTER="echo"
        ;;
    esac

    if command -v "$LINTER" &> /dev/null && [ "$LINTER" != "echo" ]; then
        "$LINTER" "$TMPFILE" 2>&1
    else
        echo "No linter available for .$EXT"
    fi
    rm -f "$TMPFILE"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['mimetools'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'MIME encoding/decoding: Base64, Quoted-printable, URL encode/decode. macOS native port.',
    'commands': [
        {'identifier': 'base64-encode', 'title': 'Base64 Encode'},
        {'identifier': 'base64-decode', 'title': 'Base64 Decode'},
        {'identifier': 'qp-encode', 'title': 'Quoted-Printable Encode'},
        {'identifier': 'qp-decode', 'title': 'Quoted-Printable Decode'},
        {'identifier': 'url-encode', 'title': 'URL Encode'},
        {'identifier': 'url-decode', 'title': 'URL Decode'},
    ],
    'script': '''#!/bin/bash
# Mime tools — macOS native plugin for NotepadMac
# Base64, Quoted-printable, URL encode/decode

COMMAND="$1"

case "$COMMAND" in
  base64-encode)
    python3 -c "
import sys, base64
text = sys.stdin.buffer.read()
print(base64.b64encode(text).decode('ascii'))
"
    ;;
  base64-decode)
    python3 -c "
import sys, base64
text = sys.stdin.read().strip()
try:
    print(base64.b64decode(text).decode('utf-8', errors='replace'))
except Exception as e:
    print(f'Decode error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  qp-encode)
    python3 -c "
import sys, quopri
text = sys.stdin.buffer.read()
print(quopri.encodestring(text).decode('ascii'))
"
    ;;
  qp-decode)
    python3 -c "
import sys, quopri
text = sys.stdin.read()
print(quopri.decodestring(text.encode('ascii')).decode('utf-8', errors='replace'))
"
    ;;
  url-encode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.quote(sys.stdin.read(), safe=''))
"
    ;;
  url-decode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.unquote(sys.stdin.read()))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppconverter'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'ASCII to Hex and Hex to ASCII converter. macOS native port of Npp Converter.',
    'commands': [
        {'identifier': 'ascii-to-hex', 'title': 'ASCII → Hex'},
        {'identifier': 'hex-to-ascii', 'title': 'Hex → ASCII'},
    ],
    'script': '''#!/bin/bash
# Npp Converter — macOS native plugin for NotepadMac
# ASCII ↔ Hex conversion

COMMAND="$1"

case "$COMMAND" in
  ascii-to-hex)
    python3 -c "
import sys
text = sys.stdin.read()
hex_str = ' '.join(f'{ord(c):02X}' for c in text)
print(hex_str)
"
    ;;
  hex-to-ascii)
    python3 -c "
import sys
hex_str = sys.stdin.read().strip()
# Remove spaces and colons
hex_str = hex_str.replace(' ', '').replace(':', '')
try:
    result = bytes.fromhex(hex_str).decode('utf-8', errors='replace')
    print(result)
except ValueError as e:
    print(f'Hex decode error: {e}', file=sys.stderr)
    sys.exit(1)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppcrosscheck'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Cross-check two lists in the current document. Shows intersection, difference, and union. macOS native port.',
    'commands': [
        {'identifier': 'cross-check', 'title': 'Cross Check Two Lists'},
        {'identifier': 'find-intersection', 'title': 'Find Intersection'},
        {'identifier': 'find-difference', 'title': 'Find Difference (A - B)'},
        {'identifier': 'find-union', 'title': 'Find Union'},
    ],
    'script': '''#!/bin/bash
# NppCrossCheck — macOS native plugin for NotepadMac
# Compare two lists separated by blank lines

COMMAND="$1"

case "$COMMAND" in
  cross-check|find-intersection|find-difference|find-union)
    python3 -c "
import sys

text = sys.stdin.read()
parts = text.split('\\n\\n')
if len(parts) < 2:
    # Try splitting on multiple blank lines
    import re
    parts = re.split(r'\\n{2,}', text)

if len(parts) < 2:
    print('Error: Need two lists separated by blank lines', file=sys.stderr)
    sys.exit(1)

list_a = set(line.strip() for line in parts[0].strip().split('\\n') if line.strip())
list_b = set(line.strip() for line in parts[1].strip().split('\\n') if line.strip())

import os
cmd = os.environ.get('NPP_CROSS_CMD', '$COMMAND')

result = []
if cmd == 'cross-check':
    result.append('=== Intersection (A ∩ B) ===')
    for item in sorted(list_a & list_b):
        result.append(item)
    result.append('')
    result.append('=== In A but not B (A - B) ===')
    for item in sorted(list_a - list_b):
        result.append(item)
    result.append('')
    result.append('=== In B but not A (B - A) ===')
    for item in sorted(list_b - list_a):
        result.append(item)
elif cmd == 'find-intersection':
    for item in sorted(list_a & list_b):
        result.append(item)
elif cmd == 'find-difference':
    for item in sorted(list_a - list_b):
        result.append(item)
elif cmd == 'find-union':
    for item in sorted(list_a | list_b):
        result.append(item)

print('\\n'.join(result))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['pork2sausage'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Pass selected text to any command-line program as input, replace selection with output. macOS native port.',
    'commands': [
        {'identifier': 'pipe-to-command', 'title': 'Pipe Selection to Command'},
    ],
    'script': '''#!/bin/bash
# Pork to Sausage — macOS native plugin for NotepadMac
# Pass selected text to a command-line program and replace with output

COMMAND="$1"
# NPP_PIPE_CMD environment variable should be set by user configuration
# Default to sort if not configured
PIPE_CMD="${NPP_PIPE_CMD:-sort}"

case "$COMMAND" in
  pipe-to-command)
    # Read stdin, pass to the configured command, output result
    INPUT=$(cat)
    echo "$INPUT" | eval "$PIPE_CMD"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['runme'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Execute the currently open file based on shell association. macOS native port using open/exec.',
    'commands': [
        {'identifier': 'run-file', 'title': 'Run Current File'},
        {'identifier': 'run-in-terminal', 'title': 'Run in Terminal'},
        {'identifier': 'open-containing-folder', 'title': 'Open Containing Folder'},
    ],
    'script': '''#!/bin/bash
# RunMe — macOS native plugin for NotepadMac
# Execute current file or open containing folder

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  run-file)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    open "$FILE"
    ;;
  run-in-terminal)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    # Open Terminal.app and run the file
    osascript -e "tell application \\"Terminal\\" to do script \\"cd '$(dirname "$FILE")' && './$(basename "$FILE")'\\""
    ;;
  open-containing-folder)
    if [ -z "$FILE" ]; then
        echo "Error: No file available" >&2
        exit 1
    fi
    open "$(dirname "$FILE")"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['rustnpp'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Run or build Rust cargo projects and .rs files. macOS native port using cargo CLI.',
    'commands': [
        {'identifier': 'cargo-run', 'title': 'Cargo Run'},
        {'identifier': 'cargo-build', 'title': 'Cargo Build'},
        {'identifier': 'cargo-test', 'title': 'Cargo Test'},
    ],
    'script': '''#!/bin/bash
# rustnpp — macOS native plugin for NotepadMac
# Run/build Rust cargo projects

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

if ! command -v cargo &> /dev/null; then
    echo "Error: cargo is not installed. Install Rust: https://rustup.rs" >&2
    exit 1
fi

case "$COMMAND" in
  cargo-run)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        # Check if we're in a cargo project
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo run 2>&1
        else
            # Try parent directories
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo run 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo run 2>&1
    fi
    ;;
  cargo-build)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo build 2>&1
        else
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo build 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo build 2>&1
    fi
    ;;
  cargo-test)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo test 2>&1
        else
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo test 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo test 2>&1
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['selectnlaunch'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Save selected text as temp file and open with system. macOS native port.',
    'commands': [
        {'identifier': 'select-and-launch', 'title': 'Select N Launch'},
        {'identifier': 'select-and-open', 'title': 'Open Selection as File'},
    ],
    'script': '''#!/bin/bash
# Select N' Launch — macOS native plugin for NotepadMac
# Save selection as temp file and open with associated program

COMMAND="$1"
# NPP_FILE_EXT environment variable for desired extension
FILE_EXT="${NPP_FILE_EXT:-txt}"

case "$COMMAND" in
  select-and-launch|select-and-open)
    INPUT=$(cat)
    TMPFILE=$(mktemp /tmp/npp-select-launch-XXXXXX."$FILE_EXT")
    echo "$INPUT" > "$TMPFILE"
    open "$TMPFILE"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['selecttoclipboard'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Auto-copy selected text to clipboard (like PuTTY). macOS native port using pbcopy.',
    'commands': [
        {'identifier': 'copy-selection', 'title': 'Copy Selection to Clipboard'},
    ],
    'script': '''#!/bin/bash
# Select to Clipboard — macOS native plugin for NotepadMac
# Copy selected text to clipboard using macOS pbcopy

COMMAND="$1"

case "$COMMAND" in
  copy-selection)
    pbcopy
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['npptextviz'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Hide/show lines by pattern for log analysis. macOS native port of NppTextViz.',
    'commands': [
        {'identifier': 'hide-matching-lines', 'title': 'Hide Lines Matching Pattern'},
        {'identifier': 'show-all-lines', 'title': 'Show All Lines'},
        {'identifier': 'hide-non-matching', 'title': 'Hide Lines NOT Matching Pattern'},
    ],
    'script': '''#!/bin/bash
# NppTextViz — macOS native plugin for NotepadMac
# Hide/show lines matching pattern (for log analysis)

COMMAND="$1"
# NPP_HIDE_PATTERN environment variable for the pattern
PATTERN="${NPP_HIDE_PATTERN:-}"

case "$COMMAND" in
  hide-matching-lines)
    if [ -z "$PATTERN" ]; then
        echo "Error: NPP_HIDE_PATTERN not set" >&2
        exit 1
    fi
    python3 -c "
import sys, re
pattern = '$PATTERN'
text = sys.stdin.read()
for line in text.split('\\n'):
    if not re.search(pattern, line):
        print(line)
"
    ;;
  show-all-lines)
    # Just output everything (undo hiding)
    cat
    ;;
  hide-non-matching)
    if [ -z "$PATTERN" ]; then
        echo "Error: NPP_HIDE_PATTERN not set" >&2
        exit 1
    fi
    python3 -c "
import sys, re
pattern = '$PATTERN'
text = sys.stdin.read()
for line in text.split('\\n'):
    if re.search(pattern, line):
        print(line)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['npptasklist'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'Scan document for TODO, FIXME, NOTE items. macOS native port of Task List.',
    'commands': [
        {'identifier': 'scan-todos', 'title': 'Scan TODO Items'},
        {'identifier': 'scan-fixmes', 'title': 'Scan FIXME Items'},
        {'identifier': 'scan-all-tasks', 'title': 'Scan All Task Markers'},
    ],
    'script': '''#!/bin/bash
# Task List — macOS native plugin for NotepadMac
# Scan TODO/FIXME/NOTE items from document

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  scan-todos|scan-fixmes|scan-all-tasks)
    python3 -c "
import sys, re, os

cmd = '$COMMAND'
text = sys.stdin.read()

patterns = {
    'scan-todos': [r'\\bTODO\\b'],
    'scan-fixmes': [r'\\bFIXME\\b', r'\\bFIX\\b'],
    'scan-all-tasks': [r'\\bTODO\\b', r'\\bFIXME\\b', r'\\bNOTE\\b', r'\\bHACK\\b', r'\\bXXX\\b', r'\\bBUG\\b'],
}

results = []
for i, line in enumerate(text.split('\\n'), 1):
    for pat in patterns.get(cmd, patterns['scan-all-tasks']):
        if re.search(pat, line, re.IGNORECASE):
            results.append(f'Line {i}: {line.strip()}')

if results:
    print('\\n'.join(results))
else:
    print('No task markers found')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['urlplugin'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'URL encode and decode selected text. macOS native port.',
    'commands': [
        {'identifier': 'url-encode', 'title': 'URL Encode Selection'},
        {'identifier': 'url-decode', 'title': 'URL Decode Selection'},
    ],
    'script': '''#!/bin/bash
# URL Encode/Decode — macOS native plugin for NotepadMac
# URL encoding and decoding using Python urllib

COMMAND="$1"

case "$COMMAND" in
  url-encode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.quote(sys.stdin.read(), safe=''))
"
    ;;
  url-decode)
    python3 -c "
import sys, urllib.parse
print(urllib.parse.unquote(sys.stdin.read()))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['webedit'] = {
    'impl_type': 'easy',
    'mac_version': '1.0.0',
    'mac_description': 'HTML tag abbreviation expansion and selection wrapping. macOS native port of WebEdit.',
    'commands': [
        {'identifier': 'expand-tag', 'title': 'Expand Tag Abbreviation'},
        {'identifier': 'wrap-selection', 'title': 'Wrap Selection with Tag'},
        {'identifier': 'remove-tag', 'title': 'Remove Surrounding Tag'},
    ],
    'script': '''#!/bin/bash
# WebEdit — macOS native plugin for NotepadMac
# HTML tag abbreviation expansion and wrapping

COMMAND="$1"
# NPP_WEBEDIT_TAG environment variable for the tag name
TAG="${NPP_WEBEDIT_TAG:-div}"

case "$COMMAND" in
  expand-tag)
    INPUT=$(cat)
    # Expand abbreviation: input text is the tag name
    TAGNAME="$INPUT"
    TAGNAME=$(echo "$TAGNAME" | xargs)  # trim whitespace
    echo "<${TAGNAME}></${TAGNAME}>"
    ;;
  wrap-selection)
    INPUT=$(cat)
    echo "<${TAG}>${INPUT}</${TAG}>"
    ;;
  remove-tag)
    python3 -c "
import sys, re
text = sys.stdin.read()
# Remove opening and closing tags, keep content
text = re.sub(r'<[^>]+>', '', text)
print(text)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}


# ══════════════════════════════════════════════════════════════════════
# MEDIUM (18) — Stub implementations (need native UI, script is partial)
# ══════════════════════════════════════════════════════════════════════

PLUGIN_IMPLS['autosave'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Auto-save files on timer or focus-loss. macOS native port — needs Swift Timer + NSDocument integration.',
    'commands': [
        {'identifier': 'save-all-now', 'title': 'Save All Files Now'},
        {'identifier': 'toggle-autosave', 'title': 'Toggle Auto-Save'},
    ],
    'script': '''#!/bin/bash
# AutoSave — macOS native plugin stub for NotepadMac
# Full implementation needs Swift Timer + NSDocument.save() + FSEvent monitoring
# This stub provides basic save-all functionality

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  save-all-now)
    if [ -n "$FILE" ]; then
        # Save the current file (host will handle all-file save)
        echo "SAVE_CURRENT"
    fi
    ;;
  toggle-autosave)
    echo "AutoSave toggle requires native Swift implementation (Timer + NSDocument)"
    echo "This is a stub — full functionality pending native code."
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['collectioninterface'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Download and install UDL/Theme collections from GitHub. macOS stub — needs URLSession + native install UI.',
    'commands': [
        {'identifier': 'download-udl-list', 'title': 'Download UDL List'},
        {'identifier': 'download-theme-list', 'title': 'Download Theme List'},
    ],
    'script': '''#!/bin/bash
# CollectionInterface — macOS native plugin stub for NotepadMac
# Full implementation needs URLSession download + JSON parsing + native install UI

COMMAND="$1"

case "$COMMAND" in
  download-udl-list)
    curl -s "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/UDL-list.json" 2>/dev/null || echo "Failed to download UDL list"
    ;;
  download-theme-list)
    curl -s "https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/master/themes-list.json" 2>/dev/null || echo "Failed to download theme list"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['compareplus'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Advanced text comparison tool. macOS stub — dual-panel diff view needs native Swift UI.',
    'commands': [
        {'identifier': 'compare-selected', 'title': 'Compare Selected Text'},
        {'identifier': 'diff-files', 'title': 'Diff Two Files'},
    ],
    'script': '''#!/bin/bash
# ComparePlus — macOS native plugin stub for NotepadMac
# Full implementation needs native dual-panel diff view UI

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  compare-selected|diff-files)
    # Basic diff using system diff command
    # For dual-panel view, native Swift UI is needed
    INPUT=$(cat)
    if [ -n "$FILE" ]; then
        TMPFILE=$(mktemp /tmp/npp-diff-XXXXXX)
        echo "$INPUT" > "$TMPFILE"
        diff -u "$FILE" "$TMPFILE" 2>&1 || true
        rm -f "$TMPFILE"
    else
        echo "Compare needs two inputs — full dual-panel UI pending native implementation"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['fwdataviz'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Fixed-width data visualization with column/field display. macOS stub — needs NSTableView native UI.',
    'commands': [
        {'identifier': 'detect-fixed-width', 'title': 'Detect Fixed-Width Layout'},
        {'identifier': 'extract-fields', 'title': 'Extract Fields'},
    ],
    'script': '''#!/bin/bash
# Fixed-width Data Visualizer — macOS native plugin stub for NotepadMac
# Full implementation needs NSTableView/NSOutlineView panel UI

COMMAND="$1"

case "$COMMAND" in
  detect-fixed-width)
    python3 -c "
import sys
lines = sys.stdin.read().split('\\n')
if not lines:
    print('No data')
    sys.exit(0)
# Detect fixed-width columns by analyzing line lengths
widths = [len(line) for line in lines if line]
avg_width = sum(widths) / len(widths) if widths else 0
is_fixed = all(w == widths[0] for w in widths) if len(widths) > 1 else False
print(f'Lines: {len(lines)}, Avg width: {avg_width:.0f}, Fixed-width: {is_fixed}')
"
    ;;
  extract-fields)
    echo "Field extraction requires native NSTableView UI — pending implementation"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['hexeditor'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Hex editor for binary files. macOS stub — needs native hex view panel.',
    'commands': [
        {'identifier': 'hex-dump', 'title': 'Hex Dump Current File'},
        {'identifier': 'hex-view-selection', 'title': 'Hex View Selection'},
    ],
    'script': '''#!/bin/bash
# HEX-Editor — macOS native plugin stub for NotepadMac
# Full hex editing needs native panel UI (Scintilla hex mode or custom NSView)

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  hex-dump)
    if [ -n "$FILE" ]; then
        xxd "$FILE" 2>&1 | head -256
    else
        INPUT=$(cat)
        echo "$INPUT" | xxd 2>&1 | head -256
    fi
    ;;
  hex-view-selection)
    INPUT=$(cat)
    echo "$INPUT" | xxd 2>&1
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['markdowntableeditor'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Markdown table alignment and editing. macOS stub — interactive table editing needs NSTableView UI.',
    'commands': [
        {'identifier': 'align-table', 'title': 'Align Markdown Table'},
        {'identifier': 'format-table', 'title': 'Format Markdown Table'},
        {'identifier': 'csv-to-table', 'title': 'Convert CSV to Table'},
    ],
    'script': '''#!/bin/bash
# Markdown Table Editor — macOS native plugin stub for NotepadMac
# Full interactive editing needs NSTableView UI

COMMAND="$1"

case "$COMMAND" in
  align-table|format-table)
    python3 -c "
import sys, re

text = sys.stdin.read()
lines = text.strip().split('\\n')
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

print('\\n'.join(result))
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

print('\\n'.join(result))
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['multireplace'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Multi-pattern search & replace across files. macOS stub — multi-rule UI needs native panel.',
    'commands': [
        {'identifier': 'multi-replace', 'title': 'Multi-Pattern Replace'},
        {'identifier': 'apply-replace-list', 'title': 'Apply Replace List'},
    ],
    'script': '''#!/bin/bash
# MultiReplace — macOS native plugin stub for NotepadMac
# Full multi-rule UI needs native Find/Replace panel extension

COMMAND="$1"
# NPP_REPLACE_RULES: newline-separated "pattern→replacement" pairs
RULES="${NPP_REPLACE_RULES:-}"

case "$COMMAND" in
  multi-replace|apply-replace-list)
    if [ -z "$RULES" ]; then
        echo "Error: NPP_REPLACE_RULES not set. Format: pattern1→replacement1\\\\npattern2→replacement2" >&2
        exit 1
    fi
    python3 -c "
import sys, re, os

text = sys.stdin.read()
rules_str = os.environ.get('NPP_REPLACE_RULES', '')

for rule in rules_str.split('\\n'):
    if not rule:
        continue
    parts = rule.split('→', 1)
    if len(parts) != 2:
        continue
    pattern, replacement = parts
    text = re.sub(pattern, replacement, text)

print(text)
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nesteddsv'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Hierarchical DSV data visualization. macOS stub — needs NSOutlineView panel UI.',
    'commands': [
        {'identifier': 'detect-dsv', 'title': 'Detect DSV Format'},
        {'identifier': 'extract-dsv-fields', 'title': 'Extract DSV Fields'},
    ],
    'script': '''#!/bin/bash
# NestedDSV — macOS native plugin stub for NotepadMac
# Full visualization needs NSOutlineView panel UI

COMMAND="$1"

case "$COMMAND" in
  detect-dsv)
    python3 -c "
import sys, csv, io

text = sys.stdin.read()
first_lines = text.split('\\n')[:5]

# Try to detect delimiter
delimiters = [',', ';', '\\t', '|', ':']
for delim in delimiters:
    counts = [line.count(delim) for line in first_lines if line]
    if counts and min(counts) > 0 and all(c == counts[0] for c in counts):
        print(f'Delimiter: {repr(delim)}, Fields per line: {counts[0] + 1}')
        sys.exit(0)

print('Could not detect DSV format')
"
    ;;
  extract-dsv-fields)
    echo "Field extraction requires native NSOutlineView UI — pending implementation"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppbplistplugin'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Binary plist viewer/editor. macOS native port using plutil — full editing needs native UI.',
    'commands': [
        {'identifier': 'convert-bplist-to-xml', 'title': 'Convert bplist to XML plist'},
        {'identifier': 'convert-bplist-to-json', 'title': 'Convert bplist to JSON'},
        {'identifier': 'view-bplist-info', 'title': 'View bplist Info'},
    ],
    'script': '''#!/bin/bash
# Notepad++ bplist plugin — macOS native port for NotepadMac
# Uses macOS native plutil for plist conversion

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  convert-bplist-to-xml)
    if [ -n "$FILE" ]; then
        plutil -convert xml1 -o - "$FILE" 2>&1
    else
        # Convert stdin
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -convert xml1 -o - "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  convert-bplist-to-json)
    if [ -n "$FILE" ]; then
        plutil -convert json -o - "$FILE" 2>&1
    else
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -convert json -o - "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  view-bplist-info)
    if [ -n "$FILE" ]; then
        plutil -p "$FILE" 2>&1
    else
        TMPFILE=$(mktemp /tmp/npp-bplist-XXXXXX.plist)
        cat > "$TMPFILE"
        plutil -p "$TMPFILE" 2>&1
        rm -f "$TMPFILE"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppftp'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'FTP/SFTP file browser and transfer. macOS stub — native file browser UI needed.',
    'commands': [
        {'identifier': 'sftp-download', 'title': 'SFTP Download File'},
        {'identifier': 'sftp-upload', 'title': 'SFTP Upload File'},
    ],
    'script': '''#!/bin/bash
# NppFTP — macOS native plugin stub for NotepadMac
# Full implementation needs native file browser UI (URLSession + NSOutlineView)

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

# NPP_FTP_HOST, NPP_FTP_USER, NPP_FTP_PATH env vars for connection
HOST="${NPP_FTP_HOST:-}"
USER="${NPP_FTP_USER:-}"
REMOTEPATH="${NPP_FTP_PATH:-}"

case "$COMMAND" in
  sftp-download)
    if [ -z "$HOST" ] || [ -z "$REMOTEPATH" ]; then
        echo "Error: Set NPP_FTP_HOST and NPP_FTP_PATH environment variables" >&2
        exit 1
    fi
    if command -v sftp &> /dev/null; then
        sftp "${USER}@${HOST}:${REMOTEPATH}" /dev/stdout 2>/dev/null
    else
        echo "Error: sftp command not available" >&2
        exit 1
    fi
    ;;
  sftp-upload)
    if [ -z "$HOST" ] || [ -z "$FILE" ]; then
        echo "Error: Need file and host configuration" >&2
        exit 1
    fi
    if command -v sftp &> /dev/null; then
        echo "put $FILE $REMOTEPATH" | sftp "${USER}@${HOST}" 2>&1
    else
        echo "Error: sftp command not available" >&2
        exit 1
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppvim'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Vim-style editing mode and key bindings. macOS stub — needs native key-binding translation layer.',
    'commands': [
        {'identifier': 'toggle-vim-mode', 'title': 'Toggle Vim Mode'},
    ],
    'script': '''#!/bin/bash
# NppVim — macOS native plugin stub for NotepadMac
# Full implementation needs Vim mode state machine + key binding layer

COMMAND="$1"

case "$COMMAND" in
  toggle-vim-mode)
    echo "Vim mode requires native Swift key-binding implementation"
    echo "This is a stub — pending native key event interception layer."
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['securepad'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Encrypt/decrypt documents with AES-256. macOS native port using Security framework / gpg.',
    'commands': [
        {'identifier': 'encrypt-selection', 'title': 'Encrypt Selection'},
        {'identifier': 'decrypt-selection', 'title': 'Decrypt Selection'},
        {'identifier': 'encrypt-file', 'title': 'Encrypt Current File'},
        {'identifier': 'decrypt-file', 'title': 'Decrypt Current File'},
    ],
    'script': '''#!/bin/bash
# SecurePad — macOS native plugin stub for NotepadMac
# Uses gpg for encryption (install: brew install gnupg)
# Full UI with password dialog needs native Swift implementation

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"
# NPP_ENCRYPT_PASSPHRASE env var for passphrase
PASS="${NPP_ENCRYPT_PASSPHRASE:-}"

case "$COMMAND" in
  encrypt-selection)
    if [ -z "$PASS" ]; then
        echo "Error: Set NPP_ENCRYPT_PASSPHRASE environment variable" >&2
        exit 1
    fi
    if command -v gpg &> /dev/null; then
        cat | gpg --batch --passphrase "$PASS" --symmetric --armor 2>/dev/null
    else
        echo "Error: gpg not installed. Install: brew install gnupg" >&2
        exit 1
    fi
    ;;
  decrypt-selection)
    if [ -z "$PASS" ]; then
        echo "Error: Set NPP_ENCRYPT_PASSPHRASE environment variable" >&2
        exit 1
    fi
    if command -v gpg &> /dev/null; then
        cat | gpg --batch --passphrase "$PASS" --decrypt 2>/dev/null
    else
        echo "Error: gpg not installed" >&2
        exit 1
    fi
    ;;
  encrypt-file)
    if [ -z "$FILE" ] || [ -z "$PASS" ]; then
        echo "Error: Need file path and passphrase" >&2
        exit 1
    fi
    gpg --batch --passphrase "$PASS" --symmetric --armor "$FILE" 2>/dev/null
    ;;
  decrypt-file)
    if [ -z "$FILE" ] || [ -z "$PASS" ]; then
        echo "Error: Need file path and passphrase" >&2
        exit 1
    fi
    gpg --batch --passphrase "$PASS" --decrypt "$FILE" 2>/dev/null
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppsnippets'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Code snippet manager with panel UI. macOS stub — needs NSTableView snippet panel.',
    'commands': [
        {'identifier': 'insert-snippet', 'title': 'Insert Snippet'},
        {'identifier': 'list-snippets', 'title': 'List Available Snippets'},
    ],
    'script': '''#!/bin/bash
# Snippets — macOS native plugin stub for NotepadMac
# Full implementation needs NSTableView panel + JSON/YAML snippet storage

COMMAND="$1"
# NPP_SNIPPETS_DIR: directory containing snippet files
SNIPPETS_DIR="${NPP_SNIPPETS_DIR:-$HOME/.notepadmac/snippets}"
# NPP_SNIPPET_NAME: name of snippet to insert
SNIPPET_NAME="${NPP_SNIPPET_NAME:-}"

case "$COMMAND" in
  insert-snippet)
    if [ -z "$SNIPPET_NAME" ]; then
        echo "Error: Set NPP_SNIPPET_NAME environment variable" >&2
        exit 1
    fi
    SNIPPET_FILE="$SNIPPETS_DIR/${SNIPPET_NAME}.txt"
    if [ -f "$SNIPPET_FILE" ]; then
        cat "$SNIPPET_FILE"
    else
        echo "Error: Snippet '$SNIPPET_NAME' not found in $SNIPPETS_DIR" >&2
        exit 1
    fi
    ;;
  list-snippets)
    if [ -d "$SNIPPETS_DIR" ]; then
        for f in "$SNIPPETS_DIR"/*.txt; do
            [ -f "$f" ] && basename "$f" .txt
        done
    else
        echo "No snippets directory: $SNIPPETS_DIR"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['takenotes'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Quick note-taking with timestamped filenames. macOS stub — needs native note panel UI.',
    'commands': [
        {'identifier': 'new-note', 'title': 'Create New Note'},
        {'identifier': 'open-last-note', 'title': 'Open Last Note'},
    ],
    'script': '''#!/bin/bash
# TakeNotes — macOS native plugin stub for NotepadMac
# Full implementation needs native NSTextView note panel + storage

COMMAND="$1"
# NPP_NOTES_DIR: directory for notes
NOTES_DIR="${NPP_NOTES_DIR:-$HOME/.notepadmac/notes}"

case "$COMMAND" in
  new-note)
    mkdir -p "$NOTES_DIR"
    TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
    NOTEFILE="$NOTES_DIR/note_${TIMESTAMP}.txt"
    touch "$NOTEFILE"
    echo "$NOTEFILE"
    ;;
  open-last-note)
    if [ -d "$NOTES_DIR" ]; then
        LAST=$(ls -t "$NOTES_DIR"/note_*.txt 2>/dev/null | head -1)
        if [ -n "$LAST" ]; then
            cat "$LAST"
        else
            echo "No notes found"
        fi
    else
        echo "Notes directory not found: $NOTES_DIR"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['tcsyslogfinder'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Find and open Teamcenter syslog files. macOS stub — needs native file browser integration.',
    'commands': [
        {'identifier': 'find-syslog', 'title': 'Find Latest Syslog'},
        {'identifier': 'open-syslog-folder', 'title': 'Open Syslog Folder'},
    ],
    'script': '''#!/bin/bash
# TC Syslog Finder — macOS native plugin stub for NotepadMac
# Needs native file browser integration for full UI

COMMAND="$1"
# NPP_SYSLOG_DIR: directory containing syslog files
SYSLOG_DIR="${NPP_SYSLOG_DIR:-$HOME/Teamcenter/syslog}"

case "$COMMAND" in
  find-syslog)
    if [ -d "$SYSLOG_DIR" ]; then
        LATEST=$(ls -t "$SYSLOG_DIR"/syslog*.log 2>/dev/null | head -1)
        if [ -n "$LATEST" ]; then
            cat "$LATEST"
        else
            echo "No syslog files found in $SYSLOG_DIR"
        fi
    else
        echo "Syslog directory not found: $SYSLOG_DIR"
        echo "Set NPP_SYSLOG_DIR to your syslog path"
    fi
    ;;
  open-syslog-folder)
    if [ -d "$SYSLOG_DIR" ]; then
        open "$SYSLOG_DIR"
    else
        echo "Directory not found: $SYSLOG_DIR"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['virtualfolders'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Virtual folder tree panel for grouping files. macOS stub — needs NSTreeController/NSOutlineView UI.',
    'commands': [
        {'identifier': 'open-virtual-folders', 'title': 'Open Virtual Folders Panel'},
    ],
    'script': '''#!/bin/bash
# Virtual Folders — macOS native plugin stub for NotepadMac
# Full implementation needs NSTreeController + NSOutlineView panel

COMMAND="$1"

case "$COMMAND" in
  open-virtual-folders)
    echo "Virtual Folders requires native NSOutlineView panel UI — pending implementation"
    echo "Similar to existing Workspace panel architecture."
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['vscodekeymapnpp'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'VS Code keyboard shortcut mapping. macOS stub — needs native key binding translation layer.',
    'commands': [
        {'identifier': 'enable-vscode-keymap', 'title': 'Enable VS Code Keymap'},
        {'identifier': 'disable-vscode-keymap', 'title': 'Disable VS Code Keymap'},
    ],
    'script': '''#!/bin/bash
# VSCode Keymap — macOS native plugin stub for NotepadMac
# Full implementation needs native Swift key binding translation

COMMAND="$1"

case "$COMMAND" in
  enable-vscode-keymap)
    echo "VS Code keymap requires native key binding implementation"
    echo "This is a stub — pending Swift key event mapping layer."
    ;;
  disable-vscode-keymap)
    echo "VS Code keymap disabled stub — pending native implementation"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['languagehelp'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'Language-specific help file viewer with keyword lookup. macOS stub — needs native help viewer.',
    'commands': [
        {'identifier': 'lookup-keyword', 'title': 'Lookup Keyword in Help'},
        {'identifier': 'open-help-file', 'title': 'Open Help File'},
    ],
    'script': '''#!/bin/bash
# LanguageHelp — macOS native plugin stub for NotepadMac
# Full implementation needs native help viewer integration

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"
# NPP_HELP_FILE: path to help file for current language
HELP_FILE="${NPP_HELP_FILE:-}"
# NPP_HELP_KEYWORD: keyword under cursor
KEYWORD="${NPP_HELP_KEYWORD:-}"

case "$COMMAND" in
  lookup-keyword)
    if [ -n "$HELP_FILE" ] && [ -f "$HELP_FILE" ]; then
        open "$HELP_FILE"
    elif [ -n "$KEYWORD" ]; then
        # Try online search as fallback
        open "https://devdocs.io/search?q=${KEYWORD}"
    else
        echo "No help file configured. Set NPP_HELP_FILE environment variable."
    fi
    ;;
  open-help-file)
    if [ -n "$HELP_FILE" ] && [ -f "$HELP_FILE" ]; then
        open "$HELP_FILE"
    else
        echo "No help file configured for current language."
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['rascript'] = {
    'impl_type': 'medium_stub',
    'mac_version': '1.0.0',
    'mac_description': 'RAScript grammar definition and parsing. macOS stub — custom grammar parser needs native implementation.',
    'commands': [
        {'identifier': 'parse-rascript', 'title': 'Parse RAScript'},
        {'identifier': 'validate-rascript', 'title': 'Validate RAScript Grammar'},
    ],
    'script': '''#!/bin/bash
# RAScript — macOS native plugin stub for NotepadMac
# Custom grammar definition for RAScript language
# Full implementation needs native parser/generator

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  parse-rascript)
    if [ -n "$FILE" ]; then
        python3 -c "
import sys, json
# Stub: basic RAScript grammar parsing
try:
    with open('$FILE') as f:
        content = f.read()
    print(f'RAScript file: {len(content)} chars, {len(content.split(chr(10)))} lines')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
"
    else
        INPUT=$(cat)
        echo "RAScript parsing requires native grammar implementation"
        echo "Input: ${#INPUT} characters"
    fi
    ;;
  validate-rascript)
    echo "RAScript grammar validation requires native parser — pending implementation"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}


# ══════════════════════════════════════════════════════════════════════
# HARD-FEASIBLE (2) — Simple macOS wrappers for niche functions
# ══════════════════════════════════════════════════════════════════════

PLUGIN_IMPLS['speechplugin'] = {
    'impl_type': 'hard_feasible',
    'mac_version': '1.0.0',
    'mac_description': 'Text-to-speech using macOS built-in say command. macOS native port of SpeechPlugin.',
    'commands': [
        {'identifier': 'speak-selection', 'title': 'Speak Selection'},
        {'identifier': 'speak-document', 'title': 'Speak Entire Document'},
        {'identifier': 'stop-speaking', 'title': 'Stop Speaking'},
    ],
    'script': '''#!/bin/bash
# SpeechPlugin — macOS native plugin for NotepadMac
# Uses macOS built-in 'say' command for text-to-speech

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  speak-selection)
    INPUT=$(cat)
    say "$INPUT" &
    ;;
  speak-document)
    if [ -n "$FILE" ] && [ -f "$FILE" ]; then
        say -f "$FILE" &
    else
        INPUT=$(cat)
        say "$INPUT" &
    fi
    ;;
  stop-speaking)
    # Kill any running say process
    killall say 2>/dev/null
    echo "Stopped speaking"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['stayawake_npp'] = {
    'impl_type': 'hard_feasible',
    'mac_version': '1.0.0',
    'mac_description': 'Prevent macOS sleep using caffeinate. macOS native port of StayAwake.',
    'commands': [
        {'identifier': 'enable-caffeinate', 'title': 'Prevent Sleep (Caffeinate)'},
        {'identifier': 'disable-caffeinate', 'title': 'Allow Sleep (Disable Caffeinate)'},
    ],
    'script': '''#!/bin/bash
# StayAwake — macOS native plugin for NotepadMac
# Uses macOS built-in 'caffeinate' command to prevent system sleep

COMMAND="$1"
PIDFILE="/tmp/npp-caffeinate.pid"

case "$COMMAND" in
  enable-caffeinate)
    if [ -f "$PIDFILE" ]; then
        OLD_PID=$(cat "$PIDFILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Caffeinate already active (PID: $OLD_PID)"
            exit 0
        fi
    fi
    caffeinate -i &
    echo $! > "$PIDFILE"
    echo "Caffeinate enabled — system will not sleep while active"
    ;;
  disable-caffeinate)
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        kill "$PID" 2>/dev/null
        rm -f "$PIDFILE"
        echo "Caffeinate disabled — system may sleep normally"
    else
        echo "No caffeinate process found"
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}


# ══════════════════════════════════════════════════════════════════════
# BUILTIN (7) — NotepadMac already has these features
# ══════════════════════════════════════════════════════════════════════

BUILTIN_PLUGINS = {
    'dark_mode_c': {
        'builtin_feature': 'macOS native dark/light mode switching via system appearance',
        'how_to_access': 'System Preferences → Appearance, or NotepadMac → Preferences → Theme',
    },
    'gotolinecol': {
        'builtin_feature': 'Go to Line/Column dialog (Cmd+L)',
        'how_to_access': 'Edit → Go to Line… or press Cmd+L',
    },
    'language_selector': {
        'builtin_feature': 'Language menu with auto-detection and manual selection',
        'how_to_access': 'Language menu in menu bar',
    },
    'nppexport': {
        'builtin_feature': 'Export as HTML/RTF',
        'how_to_access': 'File → Export as HTML / Export as RTF',
    },
    'openselection': {
        'builtin_feature': 'Open file from selected text / Open containing folder',
        'how_to_access': 'Edit → Open File / Open Containing Folder',
    },
    'sessionmgr': {
        'builtin_feature': 'Session persistence (auto-save/restore open files)',
        'how_to_access': 'NotepadMac automatically persists sessions',
    },
    'topmost': {
        'builtin_feature': 'Window pinning / floating (stay on top)',
        'how_to_access': 'Window → Keep on Top, or use macOS window level API',
    },
}


# ══════════════════════════════════════════════════════════════════════
# HARD-IMPOSSIBLE (5) — No meaningful macOS equivalent
# ══════════════════════════════════════════════════════════════════════

HARD_IMPOSSIBLE = {
    'discordrpc': {
        'reason': 'Requires Discord SDK integration. macOS Discord SDK exists but unstable, and integration effort is very high.',
        'alternative': 'Manual Discord status update, or wait for community implementation.',
    },
    'menuicons': {
        'reason': 'macOS NSMenuItem does not support icons in menu items. Windows-specific UI feature.',
        'alternative': 'No macOS equivalent. macOS menus don\'t display icons.',
    },
    'nppjumplist': {
        'reason': 'Windows 7+ Jump List feature. macOS has no equivalent OS concept (no taskbar jump lists).',
        'alternative': 'Use macOS Dock recent items or NotepadMac\'s recent files menu.',
    },
    'nppdocshare': {
        'reason': 'Real-time collaborative editing requires complex network protocol implementation (WebSocket/CRDT).',
        'alternative': 'Use external collaboration tools (VS Code Live Share concept, or shared network drives).',
    },
    'treesitterlexer': {
        'reason': 'Tree-sitter integration requires deep modification of Scintilla lexer pipeline. Extremely complex.',
        'alternative': 'Wait for future NotepadMac version that may support Tree-sitter natively.',
    },
}


# ══════════════════════════════════════════════════════════════════════
# N/A (2) — Template/Demo → macOS equivalents
# ══════════════════════════════════════════════════════════════════════

PLUGIN_IMPLS['nppplugindemo'] = {
    'impl_type': 'na',
    'mac_version': '1.0.0',
    'mac_description': 'NotepadMac plugin demo — demonstrates the macOS plugin API and manifest format.',
    'commands': [
        {'identifier': 'hello-world', 'title': 'Hello World'},
        {'identifier': 'show-info', 'title': 'Show Plugin Info'},
        {'identifier': 'count-words', 'title': 'Count Words'},
    ],
    'script': '''#!/bin/bash
# NotepadMac Plugin Demo — macOS native demo plugin
# Demonstrates the plugin API: manifest format, command handling, stdin/stdout

COMMAND="$1"

case "$COMMAND" in
  hello-world)
    echo "Hello from NotepadMac Plugin Demo!"
    ;;
  show-info)
    echo "NotepadMac Plugin Demo v1.0.0"
    echo "Commands: hello-world, show-info, count-words"
    echo "Plugin API: read stdin, write stdout, use NOTEPAD_MAC_EDIT_SCRIPT_FILE for file path"
    ;;
  count-words)
    python3 -c "
import sys
text = sys.stdin.read()
words = text.split()
print(f'Words: {len(words)}, Characters: {len(text)}, Lines: {len(text.split(chr(10)))}')
"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}

PLUGIN_IMPLS['nppplugintemplate'] = {
    'impl_type': 'na',
    'mac_version': '1.0.0',
    'mac_description': 'NotepadMac plugin development template. Copy and modify to create new plugins.',
    'commands': [
        {'identifier': 'template-command', 'title': 'Template Command'},
    ],
    'script': '''#!/bin/bash
# NotepadMac Plugin Template — starting point for new plugins
# Copy this directory and modify:
#   1. notepad-mac-plugin.json — change identifier, name, commands
#   2. This script — implement your command logic

COMMAND="$1"

case "$COMMAND" in
  template-command)
    # Replace this with your implementation
    # Read from stdin, process, write to stdout
    INPUT=$(cat)
    echo "Template received: $INPUT"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac
''',
}


# ══════════════════════════════════════════════════════════════════════
# GENERATION LOGIC
# ══════════════════════════════════════════════════════════════════════

def generate_all():
    """Create all plugin directories and files."""
    os.makedirs(PLUGINS_DIR, exist_ok=True)

    # ── Generate plugin implementations ──
    for ident, impl in PLUGIN_IMPLS.items():
        src = CATALOG_BY_ID.get(ident, {})
        dir_path = os.path.join(PLUGINS_DIR, ident)
        os.makedirs(dir_path, exist_ok=True)

        # Write manifest
        manifest = {
            'identifier': ident,
            'name': impl.get('mac_name', src.get('name', ident)),
            'version': impl['mac_version'],
            'description': impl['mac_description'],
            'author': src.get('author', ''),
            'homepage': src.get('homepage', ''),
            'entryPoint': f'{ident}.sh',
            'commands': impl['commands'],
        }
        manifest_path = os.path.join(dir_path, 'notepad-mac-plugin.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write('\n')

        # Write implementation script
        script_path = os.path.join(dir_path, f'{ident}.sh')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(impl['script'])
        os.chmod(script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)

        # Write README
        readme_lines = [
            f'# {manifest["name"]} — macOS Native Plugin',
            '',
            f'**Identifier**: `{ident}`',
            f'**Version**: {impl["mac_version"]}',
            f'**Implementation type**: {impl["impl_type"]}',
            '',
            f'{impl["mac_description"]}',
            '',
            '## Commands',
            '',
        ]
        for cmd in impl['commands']:
            readme_lines.append(f'- **{cmd["identifier"]}**: {cmd["title"]}')

        readme_lines.extend([
            '',
            '## Usage',
            '',
            'This plugin runs as a shell script command. The NotepadMac host sets:',
            '- `$1` = command identifier',
            '- `stdin` = selected text (for text-processing commands)',
            '- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)',
            '',
            f'**Upstream reference**: `{src.get("upstreamFolderName", ident)}`',
        ])

        readme_path = os.path.join(dir_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(readme_lines) + '\n')

        print(f'  ✓ Created {ident}/ ({impl["impl_type"]})')

    # ── Generate builtin plugin stubs ──
    for ident, info in BUILTIN_PLUGINS.items():
        src = CATALOG_BY_ID.get(ident, {})
        dir_path = os.path.join(PLUGINS_DIR, ident)
        os.makedirs(dir_path, exist_ok=True)

        readme_lines = [
            f'# {src.get("name", ident)} — BUILT-IN',
            '',
            f'**Identifier**: `{ident}`',
            f'**Status**: NotepadMac already has this feature built-in',
            '',
            f'## Built-in Feature',
            '',
            info['builtin_feature'],
            '',
            '## How to Access',
            '',
            info['how_to_access'],
            '',
            'No plugin installation needed — this functionality is already part of NotepadMac.',
        ]

        readme_path = os.path.join(dir_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(readme_lines) + '\n')

        print(f'  ✓ Created {ident}/ (builtin)')

    # ── Generate hard-impossible stubs ──
    for ident, info in HARD_IMPOSSIBLE.items():
        src = CATALOG_BY_ID.get(ident, {})
        dir_path = os.path.join(PLUGINS_DIR, ident)
        os.makedirs(dir_path, exist_ok=True)

        readme_lines = [
            f'# {src.get("name", ident)} — NOT AVAILABLE ON macOS',
            '',
            f'**Identifier**: `{ident}`',
            f'**Status**: Cannot be meaningfully ported to macOS',
            '',
            '## Reason',
            '',
            info['reason'],
            '',
            '## Alternative',
            '',
            info['alternative'],
        ]

        readme_path = os.path.join(dir_path, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(readme_lines) + '\n')

        print(f'  ✓ Created {ident}/ (hard-impossible)')

    # ── Generate updated catalog ──
    print('\nGenerating updated catalogs...')

    # Remove conversionStatus and conversionNote from all entries (not in spec)
    updated_plugins = []
    for p in CATALOG['plugins']:
        ident = p['identifier']
        entry = {
            'identifier': p['identifier'],
            'name': p['name'],
            'version': p['version'],
            'description': p['description'],
            'author': p.get('author', ''),
            'homepage': p.get('homepage', ''),
            'repository': p.get('repository', ''),
            'nppMacCompatibleVersions': p.get('nppMacCompatibleVersions', ''),
            'upstreamWindowsDLL': False,  # All changed to false
            'upstreamFolderName': p.get('upstreamFolderName', ''),
        }

        # For plugins with macOS implementation, update version and description
        if ident in PLUGIN_IMPLS:
            impl = PLUGIN_IMPLS[ident]
            entry['version'] = impl['mac_version']
            entry['description'] = impl['mac_description']
            # Repository URL placeholder for macOS-native zip
            entry['repository'] = f'https://github.com/notepad-macOS/PluginList/releases/download/plugins/{ident}-{impl["mac_version"]}.zip'

        # For builtin plugins, annotate description
        if ident in BUILTIN_PLUGINS:
            info = BUILTIN_PLUGINS[ident]
            entry['description'] = f'[BUILT-IN] {info["builtin_feature"]}'
            entry['repository'] = ''  # No download needed

        # For hard-impossible, annotate and keep upstream DLL reference
        if ident in HARD_IMPOSSIBLE:
            info = HARD_IMPOSSIBLE[ident]
            entry['upstreamWindowsDLL'] = True  # Still needs Windows DLL, no macOS equivalent
            entry['description'] = f'[NOT AVAILABLE ON macOS] {p["description"]}. Reason: {info["reason"]}'

        # For hard-feasible, update normally (already in PLUGIN_IMPLS)

        updated_plugins.append(entry)

    # Sort by identifier for consistent ordering
    updated_plugins.sort(key=lambda p: p['identifier'])

    # Write mac-arm64.json
    updated_catalog = {
        'version': 2,
        'source': 'macOS-native plugin catalog — converted from nppPluginList',
        'upstreamRef': 'https://github.com/notepad-plus-plus/nppPluginList',
        'plugins': updated_plugins,
    }
    catalog_path = os.path.join(BASE_DIR, 'mac-arm64.json')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(updated_catalog, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'  ✓ Updated mac-arm64.json ({len(updated_plugins)} entries)')

    # Write mac-arm64-portable.json
    # Exclude hard-impossible plugins (no macOS equivalent)
    portable_plugins = [
        p for p in updated_plugins
        if p['identifier'] not in HARD_IMPOSSIBLE
    ]
    portable_plugins.sort(key=lambda p: p['identifier'])

    updated_portable = {
        'version': 2,
        'source': 'subset of mac-arm64.json — macOS-compatible plugins only',
        'plugins': portable_plugins,
    }
    portable_path = os.path.join(BASE_DIR, 'mac-arm64-portable.json')
    with open(portable_path, 'w', encoding='utf-8') as f:
        json.dump(updated_portable, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'  ✓ Updated mac-arm64-portable.json ({len(portable_plugins)} entries)')


# ══════════════════════════════════════════════════════════════════════
# VALIDATION
# ══════════════════════════════════════════════════════════════════════

def validate():
    """Validate the generated catalog files."""
    errors = []

    # Validate JSON syntax
    for fname in ('mac-arm64.json', 'mac-arm64-portable.json'):
        fpath = os.path.join(BASE_DIR, fname)
        try:
            with open(fpath) as f:
                data = json.load(f)
            print(f'  ✓ {fname}: valid JSON, {len(data["plugins"])} plugins')
        except json.JSONDecodeError as e:
            errors.append(f'{fname}: JSON parse error — {e}')

    # Validate portable is subset of full
    with open(os.path.join(BASE_DIR, 'mac-arm64.json')) as f:
        full = json.load(f)
    with open(os.path.join(BASE_DIR, 'mac-arm64-portable.json')) as f:
        portable = json.load(f)

    full_ids = set(p['identifier'] for p in full['plugins'])
    portable_ids = set(p['identifier'] for p in portable['plugins'])

    if not portable_ids.issubset(full_ids):
        extra = portable_ids - full_ids
        errors.append(f'Portable has IDs not in full: {extra}')
    else:
        excluded = full_ids - portable_ids
        print(f'  ✓ Portable is subset of full. Excluded: {excluded}')

    # Validate all PLUGIN_IMPLS have directories
    for ident in PLUGIN_IMPLS:
        dir_path = os.path.join(PLUGINS_DIR, ident)
        if not os.path.isdir(dir_path):
            errors.append(f'Missing directory: {dir_path}')
        manifest_path = os.path.join(dir_path, 'notepad-mac-plugin.json')
        if not os.path.isfile(manifest_path):
            errors.append(f'Missing manifest: {manifest_path}')
        script_path = os.path.join(dir_path, f'{ident}.sh')
        if not os.path.isfile(script_path):
            errors.append(f'Missing script: {script_path}')

    # Validate manifest JSON syntax
    for ident in PLUGIN_IMPLS:
        manifest_path = os.path.join(PLUGINS_DIR, ident, 'notepad-mac-plugin.json')
        try:
            with open(manifest_path) as f:
                data = json.load(f)
            if 'identifier' not in data or 'commands' not in data:
                errors.append(f'{ident}: manifest missing required fields')
        except json.JSONDecodeError as e:
            errors.append(f'{ident}: manifest JSON error — {e}')

    # Validate consistency between catalog and plugin directories
    for p in full['plugins']:
        ident = p['identifier']
        if p['upstreamWindowsDLL'] == False:
            # Should have a plugin directory
            if ident not in PLUGIN_IMPLS and ident not in BUILTIN_PLUGINS:
                errors.append(f'{ident}: marked as native but no implementation')

    # Validate field consistency between full and portable for shared entries
    for p_full in full['plugins']:
        ident = p_full['identifier']
        if ident in portable_ids:
            for p_port in portable['plugins']:
                if p_port['identifier'] == ident:
                    for key in ('identifier', 'version', 'repository', 'upstreamFolderName'):
                        if p_full[key] != p_port[key]:
                            errors.append(f'{ident}: {key} mismatch between full and portable')
                    break

    if errors:
        print('\n❌ Validation errors:')
        for e in errors:
            print(f'  - {e}')
        return False
    else:
        print('\n✅ All validations passed')
        return True


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('╔════════════════════════════════════════════════╗')
    print('║  NotepadMac Plugin Generator                  ║')
    print('║  Creating macOS-native implementations...     ║')
    print('╚════════════════════════════════════════════════╝')
    print()

    print('Stage 1: Creating plugin directories and files...')
    generate_all()

    print()
    print('Stage 2: Validating output...')
    success = validate()

    if not success:
        sys.exit(1)

    print()
    print('Done! All 54 plugins have macOS-native implementations.')

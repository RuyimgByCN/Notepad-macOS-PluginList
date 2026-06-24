#!/usr/bin/env python3
"""生成「Windows 扩展集」35 个 macOS 插件。

从上游 nppPluginList 的 pl.x64.json / pl.x86.json 中精选的 35 个高价值插件，
转为 macOS 原生（CLI 包装）或 stub 形态。与 generate_all_plugins.py 独立，
不改动原脚本。详见 docs/superpowers/specs/2026-06-24-windows-highvalue-plugins-intake-design.md

用法: python3 scripts/generate_extended_plugins.py
"""
import json
import os

# ---------------------------------------------------------------------------
# 上游元数据（从 pl.x64/pl.x86 提取，内嵌以保证脚本自包含、可复现）
# origin: "x64" | "x86"
# ---------------------------------------------------------------------------
META = {
    "XMLTools":                         ("x64", "XML Tools",                  "3.1.1.13",     "Nicolas Crittin",                "https://github.com/morbac/xmltools",                "Small set of useful tools for editing XML."),
    "XPatherizerNPP":                   ("x86", "XPatherizerNPP",             "2.10",         "bguenthner",                     "https://code.google.com/p/xpatherizernpp/",         "Analyze multiple XPath queries with reverse lookup."),
    "JsonTools":                        ("x64", "JSON Tools",                 "8.5",          "Mark Johnston Olson",            "https://github.com/molsonkiko/JsonToolsNppPlugin",  "Query/editing tool for JSON including linting, reformatting."),
    "CSVLint":                          ("x64", "CSV Lint",                   "0.4.8",        "Bas de Reuver",                  "https://github.com/BdR76/CSVLint/",                 "Syntax highlighting and quality control for csv and fixed width data."),
    "PoorMansTSqlFormatterNppPlugin":   ("x64", "Poor Man's T-Sql Formatter", "1.6.13.31508", "Tao Klerks",                     "http://architectshack.com/PoorMansTSqlFormatter.ashx", "Simple SQL formatter performing full multi-batch T-SQL formatting."),
    "Tidy2":                            ("x86", "Tidy2",                      "0.2",          "Dave Brotherstone",              "https://code.google.com/p/npp-tidy2/",              "HTML Tidy with support for HTML5."),
    "NppExec":                          ("x64", "NppExec",                    "0.8.10",       "Vitaliy Dovgan",                 "https://github.com/d0vgan/nppexec",                 "Execute commands or saved scripts without leaving Notepad++."),
    "PythonScript":                     ("x64", "PythonScript",               "2.1.0.0",      "Dave Brotherstone + Jocelyn Legault", "https://github.com/bruderstein/PythonScript",  "Python Script plugin."),
    "PyNPP":                            ("x86", "PyNPP",                      "1.2",          "Abdullah Diab",                  "https://mpcabd.xyz/notepad-plugin-to-run-python-scripts/", "Run Python scripts from Notepad++."),
    "pycalc":                           ("x64", "pycalc",                     "1.0.0",        "pycalc",                         "https://github.com/pycalc-plugin/notepad-plus-plus", "Execute python code directly within the editor."),
    "NppHasher":                        ("x86", "NppHash",                    "1.0",          "Don HO",                         "https://github.com/npp-plugins/hasher",            "Computes the hash of selected text."),
    "Remove Duplicate Lines":           ("x64", "Remove Duplicate Lines",     "1.3.0.0",      "G. Singh",                       "https://github.com/gurikbal/Remove_dup_lines",      "Remove duplicate lines without removing empty lines."),
    "NppRegExTractorPlugin":            ("x64", "NppRegExTractor",            "2.1.0",        "Jan Graefe",                     "https://github.com/viper3400/RegExTractor/wiki/de_userdocumentation", "Search regular expressions and extract matches."),
    "XBrackets":                        ("x64", "XBrackets Lite",             "1.3.1",        "Vitaliy Dovgan",                 "https://github.com/d0vgan/npp-XBracketsLite",       "Autocompletion of brackets."),
    "BracketsCheck":                    ("x64", "BracketsCheck",              "1.2.2",        "niccord",                        "https://github.com/niccord/BracketsCheck/",         "Check if brackets in your file are balanced."),
    "AutoCodepage":                     ("x64", "AutoCodepage",               "1.2.7",        "Andreas Heim",                   "https://sourceforge.net/projects/autocodepage",     "Automatically sets a document's code page."),
    "NppEditorConfig":                  ("x64", "EditorConfig",               "0.4.0",        "EditorConfig Team",              "https://github.com/editorconfig/editorconfig-notepad-plus-plus", "EditorConfig defines coding conventions for a project."),
    "CodeAlignmentNpp":                 ("x64", "Code Alignment",             "14.1.107",     "Chris McGrath",                  "https://github.com/cpmcgrath/codealignment",        "Code alignment helps you present your code beautifully."),
    "ColumnsPlusPlus":                  ("x64", "Columns++",                  "1.3.1",        "Randall Joseph Fellmy",          "https://github.com/Coises/ColumnsPlusPlus",         "Features for working with text and data arranged in columns."),
    "AnalysePlugin":                    ("x64", "AnalysePlugin",              "1.13.49.0",    "Mattes H.",                      "https://sourceforge.net/projects/analyseplugin",    "Search for more than one search pattern at a time."),
    "PlantUmlViewer":                   ("x64", "PlantUML Viewer",            "1.9.0.13",     "Philipp Schmidt",                "https://github.com/Fruchtzwerg94/PlantUmlViewer",   "Generate, view and export PlantUML diagrams."),
    "DSpellCheck":                      ("x64", "DSpellCheck",                "1.5.0",        "Sergey Semushin",                "https://github.com/Predelnik/DSpellCheck",          "Spell-checking with underlining of spelling mistakes."),
    "ColorPicker":                      ("x86", "Don Rowlett Color Picker",   "2.3",          "Don Rowlett",                    "https://sourceforge.net/projects/npp-plugins/files/ColorPicker/", "Select and convert color codes in various formats."),
    "Explorer":                         ("x64", "Explorer",                   "1.9.9.0",      "Jens Lorenz",                    "https://github.com/oviradoi/npp-explorer-plugin",   "File browser."),
    "FileSwitcher":                     ("x86", "File Switcher",              "1.0.3.0",      "Dave Brotherstone",              "https://github.com/bruderstein/FileSwitcher",       "Switch the active buffer using just the keyboard."),
    "QuickOpenPlugin":                  ("x86", "QuickOpenPlugin",            "1.1",          "Sandor Gezel",                   "https://sourceforge.net/projects/quickopenplugin/", "Quick open selected file."),
    "MarkdownViewerPlusPlus":           ("x64", "MarkdownViewer++",           "0.8.2",        "nea",                            "https://nea.github.io/MarkdownViewerPlusPlus/",     "View Markdown/CommonMark rendered on-the-fly."),
    "NppMarkdownPanel":                 ("x64", "Markdown Panel",             "0.9.1",        "Mohzy83",                        "https://github.com/mohzy83/NppMarkdownPanel",       "Lightweight plugin to display rendered Markdown files."),
    "PreviewHTML":                      ("x64", "Preview HTML",               "1.4.5.0",      "Martijn Coppoolse",              "https://github.com/rdipardo/npp_preview",           "Preview HTML files inside an embedded browser."),
    "DoxyIt":                           ("x64", "DoxyIt",                     "0.4.4",        "Justin Dailey",                  "https://github.com/dail8859/DoxyIt",                "Supports creating Doxygen comments."),
    "NppMenuSearch":                    ("x64", "NppMenuSearch",              "0.9.7",        "Peter Frentrup",                 "https://github.com/peterfrentrup/NppMenuSearch",    "Search menu items and preference dialog from the toolbar."),
    "GitSCM":                           ("x64", "GitSCM",                     "1.4.10.1",     "Michael J. Vincent",             "https://github.com/vinsworldcom/nppGitSCM",         "GUI for already installed Git SCM."),
    "NppFavorites":                     ("x64", "NppFavorites",               "1.0.0.1",      "Helder Sepulveda",               "https://github.com/heldersepu/nppfavorites",        "Favorites plugin."),
    "MultiClipboard":                   ("x86", "MultiClipboard",             "2.1.0.0",      "LoonyChewy",                     "https://sourceforge.net/projects/npp-plugins/files/MultiClipboard/", "Multiple text buffers via copying/cutting."),
    "IndentByFold":                     ("x64", "Indent By Fold",             "0.7.3",        "Ben Bluemel, Frank Fesevur",     "https://github.com/ffes/indentbyfold/",             "Indent using Fold points."),
}


def C(cid, title, py=None, sh=None, stub=None):
    """命令定义：py=python3 代码 / sh=shell 命令 / stub=提示文案"""
    d = {"id": cid, "title": title}
    if py is not None:
        d["py"] = py
    elif sh is not None:
        d["sh"] = sh
    else:
        d["stub"] = stub or (title + " — pending native implementation")
    return d


# ---------------------------------------------------------------------------
# 35 个插件定义
# kind: "full" | "stub"   depends: [(cmd, install_hint), ...]
# ---------------------------------------------------------------------------
PLUGINS = [
    # ===== 完整实现批（23）=====
    {"id": "xmltools", "folder": "XMLTools", "kind": "full", "depends": [("xmllint", "preinstalled on macOS (libxml2)")], "commands": [
        C("format-xml", "Format XML", sh="xmllint --format -"),
        C("validate-xml", "Validate XML", py="import sys\nfrom xml.dom import minidom\ndata = sys.stdin.read()\ntry:\n    minidom.parseString(data)\n    print('XML is well-formed.')\nexcept Exception as e:\n    print('XML error:', e, file=sys.stderr)\n    sys.exit(1)"),
        C("escape-xml", "Escape XML Special Characters", py="import sys\ns = sys.stdin.read()\nprint(s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))"),
    ]},
    {"id": "xpatherizer", "folder": "XPatherizerNPP", "kind": "full", "commands": [
        C("list-elements", "List XML Elements", py="import sys\nfrom xml.etree import ElementTree as ET\ndata = sys.stdin.read()\ntry:\n    root = ET.fromstring(data)\n    tags = sorted({el.tag for el in root.iter()})\n    print('\\n'.join(tags))\nexcept Exception as e:\n    print('Parse error:', e, file=sys.stderr); sys.exit(1)"),
        C("count-elements", "Count XML Elements", py="import sys\nfrom xml.etree import ElementTree as ET\ndata = sys.stdin.read()\ntry:\n    root = ET.fromstring(data)\n    print(sum(1 for _ in root.iter()))\nexcept Exception as e:\n    print('Parse error:', e, file=sys.stderr); sys.exit(1)"),
        C("xpath-query", "Run XPath Query", stub="XPath query execution needs an expression input UI — pending native implementation"),
    ]},
    {"id": "jsontools", "folder": "JsonTools", "kind": "full", "commands": [
        C("format-json", "Format JSON", py="import sys, json\nprint(json.dumps(json.loads(sys.stdin.read()), indent=2, ensure_ascii=False))"),
        C("minify-json", "Minify JSON", py="import sys, json\nprint(json.dumps(json.loads(sys.stdin.read()), separators=(',', ':'), ensure_ascii=False))"),
        C("validate-json", "Validate JSON", py="import sys, json\ntry:\n    json.loads(sys.stdin.read()); print('JSON is valid.')\nexcept Exception as e:\n    print('JSON error:', e, file=sys.stderr); sys.exit(1)"),
    ]},
    {"id": "csvlint", "folder": "CSVLint", "kind": "full", "commands": [
        C("validate-csv", "Validate CSV", py="import sys, csv\nrows = list(csv.reader(sys.stdin))\nif not rows:\n    print('Empty'); sys.exit(0)\nn = len(rows[0]); bad = [i+1 for i, r in enumerate(rows) if len(r) != n]\nprint(f'Rows: {len(rows)}, Columns: {n}')\nprint('Inconsistent rows:', bad if bad else 'none')\nif bad: sys.exit(1)"),
        C("csv-to-json", "CSV to JSON", py="import sys, csv, json\nrows = list(csv.reader(sys.stdin))\nif not rows: print('[]'); sys.exit(0)\nhdr = rows[0]\nprint(json.dumps([dict(zip(hdr, r)) for r in rows[1:]], indent=2, ensure_ascii=False))"),
    ]},
    {"id": "poormantsqlformatter", "folder": "PoorMansTSqlFormatterNppPlugin", "kind": "full", "commands": [
        C("format-sql", "Format SQL", py="import sys\nsql = sys.stdin.read()\ntry:\n    import sqlparse\n    print(sqlparse.format(sql, reindent=True, keyword_case='upper'))\nexcept ImportError:\n    kw = ('SELECT','FROM','WHERE','AND','OR','ORDER BY','GROUP BY','LEFT JOIN','INNER JOIN','ON','SET','INSERT INTO','VALUES','UPDATE','DELETE')\n    out = sql\n    for k in kw:\n        out = out.replace(k.lower(), k).replace(k.capitalize(), k)\n    import re\n    out = re.sub(r'\\s+', ' ', out).strip()\n    print(out)"),
        C("minify-sql", "Minify SQL", py="import sys, re\nprint(re.sub(r'\\s+', ' ', sys.stdin.read()).strip())"),
    ]},
    {"id": "tidy2", "folder": "Tidy2", "kind": "full", "depends": [("tidy", "brew install tidy-html5")], "commands": [
        C("tidy-html", "Tidy HTML", sh="tidy -q -utf8 --tidy-mark n 2>/dev/null"),
        C("tidy-xml", "Tidy XML", sh="tidy -q -xml -utf8 --tidy-mark n 2>/dev/null"),
    ]},
    {"id": "nppexec", "folder": "NppExec", "kind": "full", "commands": [
        C("exec-command", "Execute Selection as Command", py="import sys, subprocess\ncmd = sys.stdin.read()\nr = subprocess.run(cmd, shell=True, capture_output=True, text=True)\nsys.stdout.write(r.stdout); sys.stderr.write(r.stderr); sys.exit(r.returncode)"),
        C("echo-selection", "Echo Selection", py="import sys\nsys.stdout.write(sys.stdin.read())"),
    ]},
    {"id": "pythonscript", "folder": "PythonScript", "kind": "full", "commands": [
        C("exec-python", "Execute Selection as Python", py="import sys, io\ncode = sys.stdin.read()\nbuf = io.StringIO()\ntry:\n    exec(code, {'__name__': '__main__'}, {'__stdout__': buf})\nexcept Exception as e:\n    print('Error:', e, file=sys.stderr); sys.exit(1)\nsys.stdout.write(buf.getvalue())"),
        C("eval-python", "Eval Selection", py="import sys\ntry:\n    print(eval(sys.stdin.read(), {'__builtins__': __builtins__}))\nexcept Exception as e:\n    print('Error:', e, file=sys.stderr); sys.exit(1)"),
    ]},
    {"id": "pynpp", "folder": "PyNPP", "kind": "full", "commands": [
        C("run-python", "Run Selection as Python", py="import sys, io\ncode = sys.stdin.read()\nbuf = io.StringIO()\nold = sys.stdout; sys.stdout = buf\ntry:\n    exec(code, {'__name__': '__main__'})\nexcept Exception as e:\n    sys.stdout = old; print('Error:', e, file=sys.stderr); sys.exit(1)\nsys.stdout = old; sys.stdout.write(buf.getvalue())"),
        C("python-version", "Show Python Version", sh="python3 --version"),
    ]},
    {"id": "pycalc", "folder": "pycalc", "kind": "full", "commands": [
        C("calc", "Evaluate Selection", py="import sys\nexpr = sys.stdin.read().strip()\ntry:\n    print(eval(expr, {'__builtins__': {}}, __import__('math').__dict__))\nexcept Exception as e:\n    print('Error:', e, file=sys.stderr); sys.exit(1)"),
    ]},
    {"id": "npphasher", "folder": "NppHasher", "kind": "full", "commands": [
        C("md5", "MD5 Hash", py="import sys, hashlib\nprint(hashlib.md5(sys.stdin.buffer.read()).hexdigest())"),
        C("sha256", "SHA-256 Hash", py="import sys, hashlib\nprint(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"),
        C("base64-encode", "Base64 Encode", py="import sys, base64\nprint(base64.b64encode(sys.stdin.buffer.read()).decode())"),
        C("base64-decode", "Base64 Decode", py="import sys, base64\nprint(base64.b64decode(sys.stdin.read()).decode(errors='replace'))"),
    ]},
    {"id": "remove-duplicate-lines", "folder": "Remove Duplicate Lines", "kind": "full", "commands": [
        C("remove-dups", "Remove Duplicate Lines", py="import sys\nseen = set(); out = []\nfor ln in sys.stdin.read().splitlines(True):\n    if ln not in seen:\n        seen.add(ln); out.append(ln)\nsys.stdout.write(''.join(out))"),
        C("sort-unique", "Sort and Unique", py="import sys\nsys.stdout.write(''.join(sorted(set(sys.stdin.read().splitlines(True)))))"),
        C("count-duplicates", "Count Duplicate Lines", py="import sys, collections\nc = collections.Counter(sys.stdin.read().splitlines())\nprint('Total lines:', sum(c.values()))\nprint('Unique:', len(c))\nprint('Duplicates:', sum(1 for v in c.values() if v > 1))"),
    ]},
    {"id": "nppregextractor", "folder": "NppRegExTractorPlugin", "kind": "full", "commands": [
        C("extract-emails", "Extract Email Addresses", py="import sys, re\nprint('\\n'.join(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}', sys.stdin.read())))"),
        C("extract-urls", "Extract URLs", py="import sys, re\nprint('\\n'.join(re.findall(r'https?://[^\\s)\\]\\\"\\']+', sys.stdin.read())))"),
        C("extract-ips", "Extract IP Addresses", py="import sys, re\nprint('\\n'.join(re.findall(r'\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b', sys.stdin.read())))"),
    ]},
    {"id": "xbrackets", "folder": "XBrackets", "kind": "full", "commands": [
        C("wrap-paren", "Wrap with Parentheses", py="import sys\ns = sys.stdin.read(); print('(' + s + ')')"),
        C("wrap-bracket", "Wrap with Brackets", py="import sys\ns = sys.stdin.read(); print('[' + s + ']')"),
        C("wrap-brace", "Wrap with Braces", py="import sys\ns = sys.stdin.read(); print('{' + s + '}')"),
        C("wrap-quote", "Wrap with Double Quotes", py="import sys\ns = sys.stdin.read(); print('\"' + s + '\"')"),
    ]},
    {"id": "bracketscheck", "folder": "BracketsCheck", "kind": "full", "commands": [
        C("check-balance", "Check Bracket Balance", py="import sys\npairs = {'(': ')', '[': ']', '{': '}'}; close = set(pairs.values())\nstack = []; errs = []\nfor i, ch in enumerate(sys.stdin.read()):\n    if ch in pairs: stack.append((ch, i))\n    elif ch in close:\n        if not stack or pairs[stack[-1][0]] != ch:\n            errs.append(f'Unexpected {ch!r} at {i}')\n        else: stack.pop()\nfor ch, i in stack: errs.append(f'Unclosed {ch!r} at {i}')\nprint('OK — balanced.' if not errs else '\\n'.join(errs))\nif errs: sys.exit(1)"),
    ]},
    {"id": "autocodepage", "folder": "AutoCodepage", "kind": "full", "commands": [
        C("detect-encoding", "Detect Encoding", py="import sys\nraw = sys.stdin.buffer.read()\nenc = 'ascii'\nif raw.startswith(b'\\xef\\xbb\\xbf'): enc = 'utf-8-sig'\nelif raw.startswith(b'\\xff\\xfe'): enc = 'utf-16-le'\nelif raw.startswith(b'\\xfe\\xff'): enc = 'utf-16-be'\nelse:\n    try: raw.decode('ascii'); enc = 'ascii'\n    except UnicodeDecodeError:\n        try: raw.decode('utf-8'); enc = 'utf-8'\n        except UnicodeDecodeError: enc = 'latin-1 (fallback)'\nprint(f'Bytes: {len(raw)}, detected encoding: {enc}')"),
        C("byte-stats", "Byte Statistics", py="import sys, collections\nraw = sys.stdin.buffer.read()\nc = collections.Counter(raw)\nprint(f'Total bytes: {len(raw)}')\nprint(f'Non-ASCII bytes: {sum(v for b, v in c.items() if b > 127)}')"),
    ]},
    {"id": "nppeditorconfig", "folder": "NppEditorConfig", "kind": "full", "commands": [
        C("parse-editorconfig", "Parse .editorconfig", py="import sys, configparser\ndata = sys.stdin.read()\ncp = configparser.ConfigParser()\ncp.read_string(data)\nfor sect in cp.sections():\n    print(f'[{sect}]')\n    for k, v in cp.items(sect):\n        print(f'  {k} = {v}')"),
        C("show-indent", "Show Indent Style", py="import sys, configparser\ncp = configparser.ConfigParser(); cp.read_string(sys.stdin.read())\nfor sect in cp.sections():\n    if sect == '*' or '*' in sect:\n        print(f'{sect}: indent_style={cp.get(sect, \"indent_style\", fallback=\"unset\")}, indent_size={cp.get(sect, \"indent_size\", fallback=\"unset\")}')"),
    ]},
    {"id": "codealignment", "folder": "CodeAlignmentNpp", "kind": "full", "commands": [
        C("align-equals", "Align by Equals", py="import sys\nlines = sys.stdin.read().splitlines()\nmaxlen = 0\nparts = []\nfor ln in lines:\n    idx = ln.find('=')\n    parts.append((ln[:idx], ln[idx:]) if idx >= 0 else (ln, ''))\n    if idx > maxlen: maxlen = idx\nfor left, right in parts:\n    print(left.rstrip() + ' ' * (maxlen - len(left.rstrip())) + right)"),
        C("align-spaces", "Align into Columns", py="import sys\nrows = [ln.split() for ln in sys.stdin.read().splitlines()]\nif not rows: sys.exit(0)\nncols = max(len(r) for r in rows)\nwidths = [0] * ncols\nfor r in rows:\n    for i, w in enumerate(r): widths[i] = max(widths[i], len(w))\nfor r in rows:\n    print(' '.join(r[i].ljust(widths[i]) if i < len(r) else ''.ljust(widths[i]) for i in range(ncols)).rstrip())"),
    ]},
    {"id": "columnsplusplus", "folder": "ColumnsPlusPlus", "kind": "full", "commands": [
        C("align-columns", "Align Columns", py="import sys, re\nlines = sys.stdin.read().splitlines()\nsplit = [re.split(r'\\s+', ln.strip()) for ln in lines if ln.strip()]\nif not split: sys.exit(0)\nnc = max(len(s) for s in split)\nw = [0] * nc\nfor s in split:\n    for i, x in enumerate(s): w[i] = max(w[i], len(x))\nfor s in split:\n    print('  '.join(s[i].ljust(w[i]) if i < len(s) else ''.ljust(w[i]) for i in range(nc)).rstrip())"),
        C("column-info", "Column Info", py="import sys, re\nlines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]\nif not lines: print('Empty'); sys.exit(0)\ncounts = [len(re.split(r'\\s+', ln.strip())) for ln in lines]\nprint(f'Rows: {len(lines)}, min cols: {min(counts)}, max cols: {max(counts)}, consistent: {len(set(counts)) == 1}')"),
    ]},
    {"id": "analyseplugin", "folder": "AnalysePlugin", "kind": "full", "commands": [
        C("word-frequency", "Word Frequency (Top 20)", py="import sys, collections, re\nwords = re.findall(r'\\w+', sys.stdin.read().lower())\nfor w, n in collections.Counter(words).most_common(20):\n    print(f'{n:6d}  {w}')"),
        C("line-stats", "Line Statistics", py="import sys\ndata = sys.stdin.read()\nlines = data.splitlines()\nwords = data.split()\nprint(f'Lines: {len(lines)}')\nprint(f'Words: {len(words)}')\nprint(f'Characters: {len(data)}')"),
    ]},
    {"id": "plantumlviewer", "folder": "PlantUmlViewer", "kind": "full", "depends": [("plantuml", "brew install plantuml")], "commands": [
        C("extract-diagrams", "Extract PlantUML Blocks", py="import sys, re\nblocks = re.findall(r'@startuml.*?@enduml', sys.stdin.read(), re.S)\nprint('\\n\\n'.join(blocks) if blocks else '(no @startuml blocks found)')"),
        C("validate-syntax", "Validate PlantUML Syntax", py="import sys, re\ndata = sys.stdin.read()\nstarts = len(re.findall(r'@startuml', data)); ends = len(re.findall(r'@enduml', data))\nif starts == ends and starts > 0: print(f'OK — {starts} balanced diagram block(s).')\nelif starts == 0: print('No @startuml found.')\nelse: print(f'Mismatch: {starts} @startuml vs {ends} @enduml', file=sys.stderr); sys.exit(1)"),
        C("render-to-file", "Render Diagram to PNG", stub="Rendering requires java + plantuml.jar — run: plantuml -tpng <file>. Needs native preview UI."),
    ]},
    {"id": "dspellcheck", "folder": "DSpellCheck", "kind": "full", "depends": [("hunspell", "brew install hunspell")], "commands": [
        C("list-misspellings", "List Misspelled Words", sh="hunspell -l | sort -u"),
        C("count-errors", "Count Misspelled Words", py="import sys, subprocess\nr = subprocess.run(['hunspell', '-l'], input=sys.stdin.read(), text=True, capture_output=True)\nwords = sorted(set(w for w in r.stdout.split() if w))\nprint(f'Misspelled unique words: {len(words)}')\nfor w in words: print(w)"),
    ]},
    {"id": "colorpicker", "folder": "ColorPicker", "kind": "full", "commands": [
        C("hex-to-rgb", "Hex to RGB", py="import sys, re\ns = sys.stdin.read().strip().lstrip('#')\nif len(s) == 3: s = ''.join(c*2 for c in s)\nr, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)\nprint(f'rgb({r}, {g}, {b})')"),
        C("rgb-to-hex", "RGB to Hex", py="import sys, re\nm = re.search(r'(\\d+)\\D+(\\d+)\\D+(\\d+)', sys.stdin.read())\nif not m: print('Input: rgb(r, g, b)', file=sys.stderr); sys.exit(1)\nr, g, b = map(int, m.groups())\nprint('#{:02x}{:02x}{:02x}'.format(r, g, b))"),
    ]},

    # ===== stub 占位批（12）=====
    {"id": "explorer", "folder": "Explorer", "kind": "stub", "stub_reason": "file browser side panel (NSOutlineView)", "commands": [
        C("list-directory", "List Current Directory", sh="ls -la"),
        C("current-path", "Show Current Path", sh="pwd"),
        C("browse-tree", "Browse Folder Tree", stub="Folder tree browser requires native NSOutlineView UI — pending implementation"),
    ]},
    {"id": "fileswitcher", "folder": "FileSwitcher", "kind": "stub", "stub_reason": "keyboard buffer switcher panel", "commands": [
        C("list-buffers", "List Open Buffers", stub="Listing open buffers requires editor API integration — pending implementation"),
        C("switch-buffer", "Switch Buffer by Name", stub="Buffer switcher panel requires native UI — pending implementation"),
    ]},
    {"id": "quickopenplugin", "folder": "QuickOpenPlugin", "kind": "stub", "stub_reason": "fuzzy quick-open panel", "commands": [
        C("open-selected", "Open Selected File Path", sh='open "$(cat)" 2>/dev/null || echo "Selected text is not a valid path" >&2'),
        C("quick-open", "Quick Open File", stub="Fuzzy quick-open panel requires native UI — pending implementation"),
    ]},
    {"id": "markdownviewerplusplus", "folder": "MarkdownViewerPlusPlus", "kind": "stub", "stub_reason": "live Markdown render (WKWebView)", "commands": [
        C("extract-markdown", "Extract Markdown Content", py="import sys\nsys.stdout.write(sys.stdin.read())"),
        C("render-preview", "Render Markdown Preview", stub="Live Markdown rendering requires native WKWebView — pending implementation"),
    ]},
    {"id": "nppmarkdownpanel", "folder": "NppMarkdownPanel", "kind": "stub", "stub_reason": "Markdown panel (WKWebView)", "commands": [
        C("extract-markdown", "Extract Markdown Content", py="import sys\nsys.stdout.write(sys.stdin.read())"),
        C("render-panel", "Render Markdown Panel", stub="Markdown panel requires native WKWebView — pending implementation"),
    ]},
    {"id": "previewhtml", "folder": "PreviewHTML", "kind": "stub", "stub_reason": "HTML preview (WKWebView)", "commands": [
        C("validate-html", "Validate HTML Tags", py="import sys, re\ndata = sys.stdin.read()\nopens = re.findall(r'<([a-zA-Z0-9]+)[^>]*>', data)\ncloses = re.findall(r'</([a-zA-Z0-9]+)>', data)\nprint(f'Opening tags: {len(opens)}, closing tags: {len(closes)}')"),
        C("preview", "Preview HTML", stub="HTML preview requires native WKWebView — pending implementation"),
    ]},
    {"id": "doxyit", "folder": "DoxyIt", "kind": "stub", "stub_reason": "interactive Doxygen comment editor integration", "commands": [
        C("generate-comment", "Generate Doxygen Comment", py="import sys\nlines = sys.stdin.read().rstrip('\\n').splitlines()\nout = ['/**']\nfor ln in lines:\n    out.append(' * ' + ln)\nout.append(' */')\nprint('\\n'.join(out))"),
        C("convert-javadoc", "Convert to Javadoc Style", py="import sys\nlines = sys.stdin.read().rstrip('\\n').splitlines()\nout = ['/**']\nfor ln in lines:\n    out.append(' * ' + ln)\nout += [' *', ' * @return description', ' */']\nprint('\\n'.join(out))"),
    ]},
    {"id": "nppmenusearch", "folder": "NppMenuSearch", "kind": "stub", "stub_reason": "toolbar menu-search field", "commands": [
        C("search-menus", "Search Menu Items", stub="Menu search requires native toolbar integration — pending implementation"),
    ]},
    {"id": "gitscm", "folder": "GitSCM", "kind": "stub", "stub_reason": "full Git GUI panel", "depends": [("git", "install from https://git-scm.com")], "commands": [
        C("git-status", "Git Status", sh="git status -s 2>/dev/null || echo 'Not a git repository' >&2"),
        C("git-branch", "Git Branch", sh="git branch --show-current 2>/dev/null || echo 'Not a git repository' >&2"),
        C("git-log", "Git Log (last 10)", sh="git log --oneline -10 2>/dev/null || echo 'Not a git repository' >&2"),
        C("full-gui", "Open Full Git GUI", stub="Full Git GUI panel requires native UI — pending implementation"),
    ]},
    {"id": "nppfavorites", "folder": "NppFavorites", "kind": "stub", "stub_reason": "favorites panel", "commands": [
        C("list-favorites", "List Favorites", stub="Favorites panel requires native UI and persistent storage — pending implementation"),
        C("add-favorite", "Add to Favorites", stub="Adding favorites requires native panel UI — pending implementation"),
    ]},
    {"id": "multiclipboard", "folder": "MultiClipboard", "kind": "stub", "stub_reason": "clipboard history panel", "commands": [
        C("show-history", "Show Clipboard History", stub="Clipboard history requires native panel UI — pending implementation"),
        C("paste-buffer", "Paste from Buffer", stub="Multi-buffer paste requires native UI — pending implementation"),
    ]},
    {"id": "indentbyfold", "folder": "IndentByFold", "kind": "stub", "stub_reason": "fold-point based indent (editor API)", "commands": [
        C("reindent", "Reindent by Fold", stub="Fold-based indent requires editor fold-point API — pending implementation"),
    ]},
]


# ---------------------------------------------------------------------------
# 生成器
# ---------------------------------------------------------------------------
def manifest_desc(p, meta):
    desc = meta[5]
    if p["kind"] == "full":
        return desc + " macOS native port (CLI wrapper)."
    return desc + " macOS stub — needs native " + p.get("stub_reason", "UI") + "."


def gen_manifest(p, meta):
    m = {
        "identifier": p["id"],
        "name": meta[1],
        "version": "1.0.0",
        "description": manifest_desc(p, meta),
        "author": meta[3],
        "homepage": meta[4],
        "entryPoint": p["id"] + ".sh",
        "commands": [{"identifier": c["id"], "title": c["title"]} for c in p["commands"]],
    }
    return json.dumps(m, indent=2, ensure_ascii=False) + "\n"


def gen_script(p, meta):
    lines = [
        "#!/bin/bash",
        "# " + meta[1] + " — macOS native plugin for NotepadMac",
        "# Converted from upstream " + p["folder"] + " (v" + meta[2] + ", " + META[p["folder"]][0] + ")",
        "",
        'COMMAND="$1"',
        "",
    ]
    for cmd, hint in p.get("depends", []):
        lines += [
            'if ! command -v %s > /dev/null 2>&1; then' % cmd,
            '    echo "Error: %s is required. Install: %s" >&2' % (cmd, hint),
            '    exit 1',
            'fi',
            "",
        ]
    uses_python = any("py" in c for c in p["commands"])
    if uses_python:
        lines += [
            'if ! command -v python3 > /dev/null 2>&1; then',
            '    echo "Error: python3 is required but not installed." >&2',
            '    exit 1',
            'fi',
            "",
        ]
    lines.append('case "$COMMAND" in')
    for c in p["commands"]:
        lines.append('  ' + c["id"] + ')')
        if "py" in c:
            lines.append('    python3 -c "')
            for code_line in c["py"].split("\n"):
                lines.append(code_line)
            lines.append('    "')
        elif "sh" in c:
            lines.append("    " + c["sh"])
        else:
            lines.append('    echo "%s" >&2' % c["stub"].replace('"', '\\"'))
        lines.append("    ;;")
    lines += [
        '  *)',
        '    echo "Unknown command: $COMMAND" >&2',
        '    exit 1',
        '    ;;',
        'esac',
    ]
    return "\n".join(lines) + "\n"


def gen_readme(p, meta):
    origin = META[p["folder"]][0]
    kind_label = "完整实现（CLI 包装）" if p["kind"] == "full" else "stub 占位"
    lines = [
        "# " + meta[1],
        "",
        "- 上游: [" + p["folder"] + "](" + meta[4] + ") v" + meta[2] + " (" + origin + ")",
        "- 作者: " + meta[3],
        "- 形态: " + kind_label,
        "",
        meta[5],
        "",
        "## 命令",
        "",
    ]
    for c in p["commands"]:
        tag = "stub" if ("stub" in c) else "ok"
        lines.append("- `" + c["id"] + "` — " + c["title"] + "  (" + tag + ")")
    if p.get("depends"):
        lines += ["", "## 外部依赖", ""]
        for cmd, hint in p["depends"]:
            lines.append("- `" + cmd + "`: " + hint)
    if p["kind"] == "stub":
        lines += ["", "> 本插件当前为 stub，真正可用需后续原生 Swift UI 实现（" + p.get("stub_reason", "") + "）。"]
    lines += ["", "## 上游原版本", "", "v" + meta[2] + "（本 macOS 实现为 v1.0.0）", ""]
    return "\n".join(lines)


def catalog_entry(p, meta):
    return {
        "identifier": p["id"],
        "name": meta[1],
        "version": "1.0.0",
        "description": manifest_desc(p, meta),
        "author": meta[3],
        "homepage": meta[4],
        "repository": "https://github.com/RuyimgByCN/Notepad-macOS-PluginList/releases/download/plugins/" + p["id"] + "-1.0.0.zip",
        "nppMacCompatibleVersions": "",
        "upstreamWindowsDLL": False,
        "upstreamFolderName": p["folder"],
        "upstreamOrigin": meta[0],
    }


def update_catalogs():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(here, "..")
    for fname in ["mac-arm64.json", "mac-arm64-portable.json"]:
        path = os.path.join(root, fname)
        with open(path) as f:
            data = json.load(f)
        for e in data["plugins"]:
            e.setdefault("upstreamOrigin", "arm64")
        existing = {e["identifier"] for e in data["plugins"]}
        for p in PLUGINS:
            if p["id"] not in existing:
                data["plugins"].append(catalog_entry(p, META[p["folder"]]))
        data["plugins"].sort(key=lambda e: e["identifier"])
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("updated %s: %d entries" % (fname, len(data["plugins"])))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    plugins_dir = os.path.join(here, "..", "plugins")
    os.makedirs(plugins_dir, exist_ok=True)
    count = {"full": 0, "stub": 0}
    for p in PLUGINS:
        meta = META[p["folder"]]
        d = os.path.join(plugins_dir, p["id"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "notepad-mac-plugin.json"), "w") as f:
            f.write(gen_manifest(p, meta))
        sh_path = os.path.join(d, p["id"] + ".sh")
        with open(sh_path, "w") as f:
            f.write(gen_script(p, meta))
        os.chmod(sh_path, 0o755)
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write(gen_readme(p, meta))
        count[p["kind"]] += 1
        print("generated %s (%s)" % (p["id"], p["kind"]))
    print("done: %d full + %d stub = %d plugins" % (count["full"], count["stub"], len(PLUGINS)))
    update_catalogs()


if __name__ == "__main__":
    main()

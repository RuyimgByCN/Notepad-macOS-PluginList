# 上游插件 macOS 转换路线图

上游 Notepad++ 有 54 个 ARM64 插件（来自 `nppPluginList/pl.arm64.json`）。
本文件逐条标注每个插件的 macOS 转换状态、实现建议和依赖关系。

## 分类总览

| 分类 | 数量 | 说明 |
|------|------|------|
| easy | 19 | 文本处理、格式转换类 — 可用 Python/Shell 脚本命令行包装实现 |
| medium | 18 | 需 macOS 原生代码 — 涉及网络、文件系统、复杂 UI |
| hard | 8 | Windows 专属 — 依赖 Win32 API/COM/注册表，无法有意义移植 |
| builtin | 7 | NotepadMac 已内置同等功能，无需单独插件 |
| n/a | 2 | 模板/Demo，非功能插件 |

---

## easy（19 个 — 命令行脚本包装）

| 插件 | 上游版本 | 实现建议 |
|------|----------|----------|
| Auto Detect Indention | 2.3 | 检测文件中 tab/space 缩进模式，自动切换 Tab 设置。用 Python 脚本扫描缓冲区统计缩进字符比例即可。 |
| Chinese Converter | 1.0.2 | 繁简中文转换。用 [OpenCC](https://github.com/BYVoid/OpenCC) 命令行工具做包装，`opencc -f t2s.json -i input -o output`。 |
| Emoji Description | 0.1.0 | 显示字符编码信息（Unicode 码位、UTF-8 字节序列）。Python 脚本分析缓冲区选中字符即可。 |
| HTML Tag | 1.6.0.0 | HTML/XML 标签跳转（跳到匹配标签）。用正则匹配 `<[^>]+>` 并在缓冲区中搜索对应闭合标签。 |
| JSTool (jsminnpp) | 25.11.16 | JS 格式化/压缩。用 [js-beautify](https://github.com/beautify-web/js-beautify) 或 [terser](https://github.com/terser/terser) 命令行包装。 |
| Linter++ | 1.0.3.0 | 实时代码 lint。包装 eslint / pylint / shellcheck 等外部 lint 工具，把输出解析为编辑脚本应用到缓冲区。 |
| Mime tools | 3.1 | Base64 / quoted-printable 编解码。Python `base64` / `quopri` 模块一行命令即可。 |
| Npp Converter | 4.7 | ASCII↔Hex 转换。纯文本变换，`xxd` 或 Python 一行脚本。 |
| NppCrossCheck | 1.2.0.0 | 比较两个列表。Python 脚本做集合运算（交集/差集/对称差），结果输出为编辑脚本。 |
| Pork to Sausage | 2.6 | 把选区文本传给命令行程序处理。**直接映射到 macOS 原生插件命令系统** — 本项目的 PluginEditScript 机制已原生支持此模式。 |
| RunMe | 1.6.1.0 | 执行当前文件（按 shell association）。**直接映射** — 用 `open` 或直接执行脚本文件。 |
| rustnpp | 1.0.2 | 运行/构建 Rust cargo 项目。包装 `cargo run` / `cargo build` 命令。 |
| Select N' Launch | 2.2 | 保存选区为临时文件并执行。**直接映射** — 写临时文件 + 执行，PluginEditScript 天然支持。 |
| Select to Clipboard | 1.0.3.0 | 自动复制选中文本。简单缓冲区事件监听 + pasteboard 写入。 |
| NppTextViz | 0.4.3 | 隐藏/显示行（日志分析）。Python 脚本按正则模式过滤行，输出为编辑脚本。 |
| Task List | 2.7 | 扫描文档中 TODO/FIXME/NOTE 项。grep 模式搜索 + 结果列表。 |
| URL Encode/Decode | 1.2.0.0 | URL 编码/解码。Python `urllib.parse.quote/unquote` 一行调用。 |
| WebEdit | 2.9.0.1 | HTML 标签缩写展开（输入 `div` → `<div></div>`）。文本模板替换脚本。 |
| JSON Viewer | 2.2.0.0 | JSON 树形查看。用 `python -m json.tool` 或 `jq` 格式化，树形 UI 需原生面板（但格式化部分可先做脚本包装）。 |

### 实现模式（easy 类通用模板）

每个 easy 插件可按以下 macOS 原生插件 manifest 结构实现：

```json
{
  "identifier": "url-encode-decode",
  "name": "URL Encode/Decode",
  "version": "1.0.0",
  "entryPoint": "url-plugin.sh",
  "commands": [
    { "identifier": "url-encode", "title": "URL Encode Selection" },
    { "identifier": "url-decode", "title": "URL Decode Selection" }
  ]
}
```

`url-plugin.sh` 脚本：

```bash
#!/bin/bash
# NOTEPAD_MAC_EDIT_SCRIPT_FILE is set by the host
COMMAND="$1"   # url-encode or url-decode
case "$COMMAND" in
  url-encode)
    python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read()))"
    ;;
  url-decode)
    python3 -c "import urllib.parse,sys; print(urllib.parse.unquote(sys.stdin.read()))"
    ;;
esac
```

---

## medium（18 个 — 需要 macOS 原生代码）

| 插件 | 上游版本 | 实现建议 |
|------|----------|----------|
| AutoSave | 2.0 | 定时保存 + 夀焦保存。需 Swift 实现：`Timer` + `NSDocument.save()` + `FSEvent` 文件变更检测。可参考本项目已有的 FileMonitor。 |
| CollectionInterface | 1.3.0 | 从 GitHub 下载 UDL/主题集。需 Swift 实现 `URLSession` 下载 + JSON 解析 + 安装到本地目录。 |
| ComparePlus | 3.0.0 | 高级文本比较工具。核心 diff 算法可用 `diff` 命令，但双面板并排对比 UI 需原生 Swift 实现（类似现有 Clone View 模式）。 |
| Fixed-width Data Visualizer | 2.6.7.0 | 定宽数据可视化（列/字段）。需原生 Swift NSTableView/NSOutlineView 面板。 |
| FWDataViz（同上） | — | 同 Fixed-width Data Visualizer。 |
| Go to Line/Col | 2.4.5.1 | 虽然已有 Go to Line，但"指定列偏移"功能需增强。扩展现有 Cmd+L 对话框加 Column 字段。 |
| HEX-Editor | 0.9.14.0 | 二进制 hex 编辑。可利用 Scintilla 的十六进制显示模式（SCI_SETREPRESENTATION），或实现独立 hex 面板。 |
| Markdown Table Editor | 11.0.0 | Markdown 表格对齐编辑。需交互式表格编辑 UI — NSTableView 编辑模式 + 文本对齐算法。 |
| MultiReplace | 6.0.0.36 | 多模式批量查找替换。需扩展现有 Find/Replace 面板，添加多规则列表 UI。 |
| NestedDSV Data Visualizer | 1.1.0.1 | 层级 DSV 可视化。需 NSTableView/NSOutlineView 面板。 |
| Notepad++ bplist plugin | 3.0.0.0 | 二进制 plist 查看/编辑。macOS 有 `plutil` 命令行可做基本查看，完整编辑需原生 Swift plist 解析器。 |
| NppFTP | 0.29.15 | FTP/SFTP 文件浏览器。需 Swift `URLSession` + 文件列表 UI。可参考现有 Folder as Workspace 面板模式。 |
| NppVim | 1.8.0.0 | Vim 键绑定模式。需实现 Vim 模式状态机（normal/insert/visual）+ 键映射层。大工程。 |
| SecurePad | 2.4 | 文档加密/解密。可用 macOS Security.framework 或 `gpg` 命令行包装。完整 UI 需原生面板。 |
| Snippets | 1.7.1 | 代码片段管理。需片段面板 UI（NSTableView）+ JSON/YAML 存储。 |
| TakeNotes | 1.2.7.0 | 带时间戳的笔记面板。需原生 NSTextView 面板 + 存储。 |
| TC Syslog Finder | 1.0.0.0 | 定位 Teamcenter syslog 文件。文件系统导航 — 需原生文件浏览器集成。 |
| Virtual Folders | 1.0.3 | 虚拟文件夹树。需原生 NSTreeController + NSOutlineView 面板（类似现有 Workspace 面板）。 |
| VSCode Keymap NPP | 0.2.0 | VS Code 快捷键映射。需翻译 VS Code 键绑定到 macOS 键绑定系统的映射层。 |
| Code Snippets | — | 需原生片段面板 + 存储。 |

---

## hard（8 个 — Windows 专属，无法有意义移植）

| 插件 | 上游版本 | 原因 |
|------|----------|------|
| Dark Mode C | 1.0.3 | macOS 已原生支持深色/浅色模式切换，无需插件。此插件针对 Windows 深色模式 API。 |
| Discord Rich Presence | 2.1.711.1 | 需要 Discord SDK 原生集成。技术上可行但工作量极大，且 Discord macOS SDK 稳定性不确定。 |
| MenuIcons | 2.0.7 | 给 Windows 菜单添加图标。macOS 菜单栏不支持图标（NSMenuItem 无图标 API），完全不同机制。 |
| NppJumpList | 1.2.2 | Windows 7 任务栏跳转列表。macOS 无此概念（无等效 OS 功能）。 |
| NppNetNote (Doc Share) | 0.2.0.0 | 实时文档共享。需完整网络协议栈实现，极复杂。 |
| StayAwake | 1.1.0.0 | 阻止 Windows 系统休眠。macOS 有 `caffeinate` 命令但场景极不同。 |
| SpeechPlugin | 0.4.0.0 | TTS 朗读。macOS 有 `say` 命令可用，但与编辑器集成需原生代码。技术上可行但 ROI 低。 |
| TreeSitter | 1.2.0 | Tree-sitter AST 语法高亮。需要与 Scintilla 深度集成（修改词法分析器管线），极复杂。 |

---

## builtin（7 个 — NotepadMac 已内置）

| 插件 | 上游版本 | NotepadMac 对应功能 |
|------|----------|----------------------|
| Dark Mode C | 1.0.3 | 系统外观自动适配深色/浅色模式 |
| Go to Line/Col | 2.4.5.1 | Cmd+L Go to Line 对话框 |
| Language Selector | 1.2.0.0 | Language 菜单（自动检测 + 手动选择） |
| NppExport | 0.4.0.0 | File > Export as HTML / Export as RTF |
| Open Selection | 1.1.3.0 | Edit > Open File / Open Containing Folder |
| Session Manager | 1.4.4 | 会话持久化（自动保存/恢复打开文件） |
| TopMost | 1.4.2.0 | 窗口置顶/浮动面板 |

---

## n/a（2 个 — 模板/Demo）

| 插件 | 说明 |
|------|------|
| Notepad++ Plugin Demo | 插件开发示例代码，无功能转换需求 |
| Notepad++ Plugin Template | 插件开发模板，可创建 macOS 版本模板 |

---

## 优先级排序（建议实施顺序）

### 第一批（快速见效 — 5 个 easy 插件）

1. **Pork to Sausage** — 本项目 PluginEditScript 机制天然支持，零代码改动只需 manifest
2. **RunMe** — 同上，命令执行包装
3. **Select N' Launch** — 同上
4. **Npp Converter** — ASCII↔Hex，纯文本变换
5. **URL Encode/Decode** — URL 编解码，纯文本变换

### 第二批（实用增强 — 10 个 easy + 3 个 medium）

6. **Task List** — TODO/FIXME 扫描
7. **Chinese Converter** — 繁简转换（OpenCC 包装）
8. **Linter++** — 外部 lint 工具包装
9. **Mime tools** — Base64/QP 编解码
10. **NppTextViz** — 行隐藏/显示
11. **JSON Viewer** — JSON 格式化
12. **Auto Detect Indention** — 缩进检测
13. **JSTool** — JS 格式化/压缩
14. **HTML Tag** — 标签跳转
15. **Emoji Description** — 字符信息展示
16. **Go to Line/Col** (medium) — 增强现有对话框加 Column 字段
17. **AutoSave** (medium) — 定时/失焦保存
18. **NppFTP** (medium) — FTP/SFTP 浏览器

### 第三批（长期目标 — UI 重型 medium）

19-36. 各 medium 类插件需原生 Swift UI 实现，逐个推进。

---

> 维护者：当某个插件有了 macOS 原生实现后，请更新 `mac-arm64.json` 中对应条目的 `upstreamWindowsDLL` 为 `false`，填写 `repository` 为原生 zip 下载地址，并在此文件中标注完成日期。

---

## 扩展集（2026-06-24 新增 35 个）

主集（上游 `pl.arm64.json` 54 个）之外，从上游 `pl.x64.json`/`pl.x86.json` 精选纳入 35 个跨平台可行的高价值插件。完整设计见 `docs/superpowers/specs/2026-06-24-windows-highvalue-plugins-intake-design.md`。

| 形态 | 数量 | 说明 |
|------|------|------|
| 完整实现（CLI 包装） | 23 | 纯文本变换/格式化/脚本执行，python3 + macOS 自带工具，开箱即用 |
| stub 占位 | 12 | 需原生 Swift UI（NSOutlineView/WKWebView 等），当前为 manifest + 提示脚本 |

**完整实现批（23）**：xmltools, xpatherizer, jsontools, csvlint, poormantsqlformatter, tidy2, nppexec, pythonscript, pynpp, pycalc, npphasher, remove-duplicate-lines, nppregextractor, xbrackets, bracketscheck, autocodepage, nppeditorconfig, codealignment, columnsplusplus, analyseplugin, plantumlviewer, dspellcheck, colorpicker

**stub 批（12）**：explorer, fileswitcher, quickopenplugin, markdownviewerplusplus, nppmarkdownpanel, previewhtml, doxyit, nppmenusearch, gitscm, nppfavorites, multiclipboard, indentbyfold

**来源平台分布**：27 个 `x64` + 8 个 `x86`（colorpicker / fileswitcher / multiclipboard / npphasher / pynpp / quickopenplugin / tidy2 / xpatherizer）。

**外部依赖**（脚本内 `command -v` 检查 + 安装提示）：`hunspell`（dspellcheck）、`tidy`（tidy2）、`plantuml`（plantumlviewer）；其余零依赖。

**生成入口**：`python3 scripts/generate_extended_plugins.py`（同时生成 35 个插件目录并更新两个 JSON 目录）。打包：`python3 scripts/package_plugins.py`。

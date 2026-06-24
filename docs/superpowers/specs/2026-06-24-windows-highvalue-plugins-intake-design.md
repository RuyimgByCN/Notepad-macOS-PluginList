# 纳入上游 Windows 高价值插件到 macOS 目录 — 设计文档

- 日期：2026-06-24
- 状态：待审阅
- 作者：zhaomingzhen

## 1. 背景与动机

本项目（Notepad-macOS-PluginList）的插件目录源自上游 nppPluginList 的 `pl.arm64.json`（54 个），已 100% 覆盖。但上游 `pl.x64.json`（182）与 `pl.x86.json`（201）中有 **164 个 ARM64 目录没有的插件**，其中相当一部分是跨平台可行、用户需求高的工具（拼写检查、XML/JSON/SQL 处理、脚本引擎、文件浏览器等）。

本设计把这 164 个中**精选的 35 个高价值项**纳入 macOS 目录，使 macOS 用户也能获得这些常用插件的能力。

## 2. 目标与非目标

**目标**
- 将 35 个高价值 Windows 插件以 macOS 实现/stub 形态纳入 `mac-arm64.json` 与 `mac-arm64-portable.json`
- 扩展 CLAUDE.md 范围规则，正式允许"扩展集"
- 全部产出可校验、可复现、可打包发布

**非目标**
- 不纳入 164 个全部（仅精选 35 个高价值）
- 不纳入纯 Windows 专有不可移植项（ActiveX、NppSaveAsAdmin、NppTFS 等）
- 不实现需深度改造编辑器内核的功能（TreeSitter 已属现有 hard 类，不在此范围）
- stub 批不做完整原生 UI 实现（仅占位 + CLI 基本版）

## 3. 范围：35 个清单

### 3.1 完整实现批（23 个）— CLI 可包装，`upstreamWindowsDLL:false`，真实可用

| identifier | upstreamFolderName | macOS 实现方式 | 依赖 |
|---|---|---|---|
| `xmltools` | XMLTools | `xmllint` 格式化/校验/XSLT | 自带 libxml2 |
| `xpatherizer` | XPatherizerNPP | `xmllint --xpath` 查询 | 自带 |
| `jsontools` | JsonTools | python `json` lint+reformat | python3 |
| `csvlint` | CSVLint | python `csv` 校验列一致 | python3 |
| `poormantsqlformatter` | PoorMansTSqlFormatterNppPlugin | python 正则兜底 / `sqlparse` | python3（sqlparse 可选） |
| `tidy2` | Tidy2 | `tidy` HTML5 整理 | `brew install tidy-html5` |
| `nppexec` | NppExec | shell 执行命令/脚本 | 自带 |
| `pythonscript` | PythonScript | `python3` 脚本引擎 | python3 |
| `pynpp` | PyNPP | `python3` 运行 .py | python3 |
| `pycalc` | pycalc | `python3` 表达式求值 | python3 |
| `npphasher` | NppHasher | `shasum` / `openssl dgst` | 自带 |
| `remove-duplicate-lines` | Remove Duplicate Lines | `awk` / `sort -u` | 自带 |
| `nppregextractor` | NppRegExTractorPlugin | `grep -P` / python `re` 提取 | 自带 |
| `xbrackets` | XBrackets | 选区括号自动补全 | python3 |
| `bracketscheck` | BracketsCheck | 括号配对校验 | python3 |
| `autocodepage` | AutoCodepage | `file -I` 编码检测 | 自带 |
| `nppeditorconfig` | NppEditorConfig | python `configparser` 解析 | python3 |
| `codealignment` | CodeAlignmentNpp | 列对齐算法 | python3 |
| `columnsplusplus` | ColumnsPlusPlus | `awk`/python 列操作 | 自带/python3 |
| `analyseplugin` | AnalysePlugin | 多模式并行搜索 | grep/python3 |
| `plantumlviewer` | PlantUmlViewer | `java -jar plantuml.jar` | `brew install plantuml` |
| `dspellcheck` | DSpellCheck | `hunspell` 检查 | `brew install hunspell` |
| `colorpicker` | ColorPicker | 颜色码格式转换 | python3 |

### 3.2 stub 占位批（12 个）— 需原生 UI，有 manifest + 提示脚本

| identifier | upstreamFolderName | stub 原因（需原生 UI） |
|---|---|---|
| `explorer` | Explorer | 文件浏览器侧栏（NSOutlineView） |
| `fileswitcher` | FileSwitcher | 键盘文件切换面板 |
| `quickopenplugin` | QuickOpenPlugin | 模糊快速打开面板 |
| `markdownviewerplusplus` | MarkdownViewerPlusPlus | Markdown 实时渲染（WKWebView） |
| `nppmarkdownpanel` | NppMarkdownPanel | Markdown 面板（WKWebView） |
| `previewhtml` | PreviewHTML | HTML/Markdown 预览（WKWebView） |
| `doxyit` | DoxyIt | Doxygen 注释生成（编辑器集成） |
| `nppmenusearch` | NppMenuSearch | 工具栏菜单搜索框 |
| `gitscm` | GitSCM | Git GUI 面板 |
| `nppfavorites` | NppFavorites | 收藏夹面板 |
| `multiclipboard` | MultiClipboard | 剪贴板历史面板 |
| `indentbyfold` | IndentByFold | 基于折叠点缩进（编辑器 API） |

## 4. 设计决策

### 4.1 规则与纳入策略

**4.1.1 CLAUDE.md 第 5 条扩展** —— 从"仅 ARM64"扩展为两层语义：
- **主集**：上游 `pl.arm64.json` 全量（必跟）
- **扩展集**：上游 `pl.x64.json`/`pl.x86.json` 中跨平台可行的高价值插件（精选纳入，需 macOS 实现/stub）
- 扩展集条目用 `upstreamOrigin` 标注来源平台，便于将来上游 ARM64 补入时去重合并

条目数更新：`mac-arm64.json` 54→89，`mac-arm64-portable.json` 50→85。

**4.1.2 新增可选字段 `upstreamOrigin`**（值 `"arm64"` | `"x64"` | `"x86"`）：
- 现有 54 个补 `"arm64"`
- 新增 35 个多数标 `"x64"`，仅 32 位有的标 `"x86"`
- CLAUDE.md「字段规范」表从 10 字段增至 11 字段

**4.1.3 portable 纳入** —— 35 个全部进入 `mac-arm64-portable.json`（均为 macOS 实现，非"仅 Windows 不可用"，符合现有 portable 排除规则）。

### 4.2 条目数据规范

**4.2.1 `identifier` 命名** —— folder-name 衍生：全小写、空格→连字符、去点号；去掉**末尾**冗余后缀（`Plugin`/`NppPlugin`/`NPP` 等）以保持可读；`Npp` 作为**前缀**时保留（与现有 `nppconverter`/`nppftp` 一致）；`upstreamFolderName` 始终保留上游原名。

**4.2.2 `version`** —— 35 个统一 `"1.0.0"`（新写 macOS 实现 v1）。上游原版本号记录在各插件 README 备查。

**4.2.3 `repository`** —— 填预期 release URL：`https://github.com/RuyimgByCN/Notepad-macOS-PluginList/releases/download/plugins/<id>-1.0.0.zip`；执行计划含打包发布步骤使其生效。

**4.2.4 其他字段** —— `name` 取上游 `display-name`；`author`/`homepage` 取上游条目；`description` 完整批写"功能 + macOS 实现方式"，stub 批标注"macOS stub — needs <NSXxxView> UI"；`nppMacCompatibleVersions` 默认 `""`。

### 4.3 实现规范

**4.3.1 目录与 manifest** —— 每个插件 `plugins/<id>/{<id>.sh, notepad-mac-plugin.json, README.md}`。manifest 9 字段与现有一致（`identifier`/`name`/`version`/`description`/`author`/`homepage`/`entryPoint`/`commands[]`）。`commands[]` 每插件 2–6 个命令，`identifier` kebab-case、`title` 人类可读。

**4.3.2 `.sh` 双模板**：
- **完整实现**：`COMMAND="$1"` → `command -v` 依赖检查 → `case` 分发 → python3/自带工具真实逻辑，stdin 读选区文本、stdout 输出替换结果（host 据此改缓冲区）。
- **stub**：同 case 结构，能做的命令做 CLI 基本版（如 Explorer 的"列出当前目录"），做不了的 `echo "... requires native <NSXxxView> UI — pending implementation" >&2`。

**4.3.3 依赖策略（核心）** —— 零依赖优先：
- **零依赖**（python3 标准库 + macOS 自带）：JsonTools/CSVLint/NppEditorConfig/PoorMansSql 兜底/pycalc/PythonScript/PyNPP/RemoveDupLines/AnalysePlugin/NppHasher/AutoCodepage/XBrackets/BracketsCheck/CodeAlignment/ColumnsPlusPlus/NppRegExTractor 等
- **自带系统工具**：XMLTools/XPatherizerNPP（`xmllint`/`xsltproc`，macOS 自带 libxml2）、NppExec（shell）
- **需 brew/pip，脚本检查 + 安装提示**：DSpellCheck（hunspell）、Tidy2（tidy-html5）、PlantUmlViewer（plantuml）、PoorMansSql 进阶（sqlparse）

### 4.4 执行结构

**4.4.1 生成方式** —— 新独立脚本 `scripts/generate_extended_plugins.py`：从上游 JSON 读元数据（author/homepage/description/display-name）+ 内置 35 个命令定义表，生成插件目录。**不改动**原 `generate_all_plugins.py`。

**4.4.2 JSON 目录更新** —— 用 jq 脚本：现有 54 条补 `upstreamOrigin:"arm64"`；新增 35 条按 `identifier` 字母序插入两个 JSON。禁止手拼 JSON。

**4.4.3 打包发布** —— 写/复用打包脚本，35 个插件各打 zip（manifest+.sh+README），上传 `RuyimgByCN/Notepad-macOS-PluginList` 的 `plugins` release（与现有 42 个同址）。

**4.4.4 文档更新** —— CLAUDE.md（第 5 条扩展 + 字段表加 `upstreamOrigin` + 条目数 54→89/50→85）+ CONVERSION_ROADMAP（追加「扩展集」章节列 35 项）。

## 5. 校验清单

- [ ] `python3 -m json.tool mac-arm64.json` / `mac-arm64-portable.json` 合法
- [ ] `bash -n` 全部 .sh 通过
- [ ] `mac-arm64-portable.json` ⊆ `mac-arm64.json`（identifier 子集）
- [ ] 89 条均有 `upstreamOrigin` 字段，值合法
- [ ] manifest `commands` 与 `.sh` `case` 分支对齐
- [ ] 35 个 zip 打包并发布，`repository` URL 可访问

## 6. 执行步骤（顺序）

1. 从 `/tmp/pl.x64.json` + `pl.x86.json` 提取 35 个上游元数据（author/homepage/description/display-name），确定每个 `upstreamOrigin`（x64/x86 都有标 x64，仅 x86 标 x86）
2. 写 `scripts/generate_extended_plugins.py`（含 35 个命令定义表）
3. 运行生成 35 个 `plugins/<id>/` 三件套
4. jq 脚本：现有 54 条补 `upstreamOrigin=arm64`；新增 35 条按字母序插入两个 JSON
5. 全量校验（JSON/bash/portable 子集/commands 对齐）
6. 打包 35 个 zip + 发布 `plugins` release
7. 更新 CLAUDE.md + CONVERSION_ROADMAP
8. 分逻辑提交（生成脚本 / 插件文件 / JSON 目录 / 文档 / 打包脚本）

## 7. 风险与备注

- **依赖可用性**：hunspell/tidy/plantuml 需用户自行 `brew install`，脚本会 stderr 提示；零依赖项开箱即用。
- **stub 价值**：stub 批当前仅占位 + CLI 基本版，真正可用需后续原生 Swift UI 实现（超出本次范围）。
- **上游同步**：将来上游 `pl.arm64.json` 若补入同名插件，需凭 `upstreamOrigin` + `upstreamFolderName` 识别并合并，避免重复条目。
- **打包发布权限**：发布 zip 需对 `RuyimgByCN/Notepad-macOS-PluginList` 的 release 有写权限。
- **identifier 缩写一致性**：去冗余后缀的缩写需在 PR 评审时确认可读性，`upstreamFolderName` 保留原名确保可追溯。

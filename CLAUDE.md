# Notepad-macOS PluginList — Claude 项目指南

Notepad-macOS 的插件目录仓库，作用等同于上游 Notepad++ 的
[nppPluginList](https://github.com/notepad-plus-plus/nppPluginList)。
提供机器可读的 JSON 目录供 Notepad-macOS Plugin Admin 拉取、比对和安装插件。

## 不可违反的规则

### 1. JSON 必须合法且可解析

- `mac-arm64.json` 和 `mac-arm64-portable.json` 是 Plugin Admin 直接拉取的目录文件，
  **畸形 JSON 会导致客户端崩溃**。
- 提交前务必验证：`python3 -m json.tool mac-arm64.json` 或 `jq . mac-arm64.json`。
- **禁止**手动拼接 JSON 字符串；增删条目后用 jq 或脚本操作，再整体校验。

### 2. 两个文件的用途和关系

| 文件 | 内容 | 条目数 |
|------|------|--------|
| `mac-arm64.json` | 全量目录（含所有已知插件） | 54 |
| `mac-arm64-portable.json` | 可移植子集（排除明显仅 Windows 的插件） | 50 |

- `mac-arm64-portable.json` **必须是 `mac-arm64.json` 的子集**，不能包含全量文件中不存在的条目。
- 两个文件中的同一条目 `identifier`、`version`、`repository` 等关键字段必须一致。

### 3. 字段规范

每个插件条目必须包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `identifier` | string | 唯一标识，源自上游文件夹名（如 `auto-detect-indent`） |
| `name` | string | Plugin Admin 显示名 |
| `version` | string | 插件版本号 |
| `description` | string | 一行功能描述 |
| `author` | string | 插件作者 |
| `homepage` | string | 项目主页 URL |
| `repository` | string | 插件 zip 包下载 URL |
| `nppMacCompatibleVersions` | string | 语义版本区间（如 `[8.9.6,]` 表示 ≥8.9.6） |
| `upstreamWindowsDLL` | boolean | `true`=引用上游 Windows DLL，需 macOS 原生重实现；`false`=已有原生 macOS 插件 |
| `upstreamFolderName` | string | 上游原文件夹名，用于交叉引用 |

### 4. macOS 原生插件条目规则

- 新增 macOS 原生插件必须设 `upstreamWindowsDLL: false`。
- `repository` URL 指向的 zip 包内必须包含：
  1. `notepad-mac-plugin.json` 清单文件
  2. 原生 macOS 可执行文件（不是 .dll）
- 如条目从 `upstreamWindowsDLL: true` 变为 `false`（即已有原生实现），需**同步更新**
  `mac-arm64.json` 和 `mac-arm64-portable.json` 中的同一条目。

### 5. 与上游 nppPluginList 的关系

- 初始目录从上游 `pl.arm64.json` 转换而来，所有条目初始为 `upstreamWindowsDLL: true`。
- 当上游 nppPluginList 更新（新增/删除/改版插件）时，本仓库需同步跟进，
  但仅限于 **ARM64 平台** 的条目。
- 新增上游条目时，保留其 `upstreamFolderName` 以便交叉对照。

## 项目结构

```
mac-arm64.json            全量插件目录（54 条）
mac-arm64-portable.json   可移植子集（50 条）
CONVERSION_ROADMAP.md     从上游 nppPluginList 转换的规划记录
README.md                 用户文档（字段说明、PR 提交指南）
package.json              包元数据
```

## 常用命令

```bash
# JSON 合法性校验
python3 -m json.tool mac-arm64.json
python3 -m json.tool mac-arm64-portable.json

# 用 jq 查看/筛选
jq '.[] | select(.upstreamWindowsDLL == false)' mac-arm64.json   # 原生插件
jq '.[] | .identifier' mac-arm64.json                             # 所有 identifier
jq length mac-arm64.json                                          # 条目总数

# 比对两个文件的一致性
diff <(jq -S '.[] | .identifier' mac-arm64.json) \
     <(jq -S '.[] | .identifier' mac-arm64-portable.json)
```

## 编码约定

- 回复用户请使用简体中文（继承全局规则）。
- JSON 条目按 `identifier` 字母序排列，便于 diff 和审阅。
- 字段值不要有多余空格或换行。
- `nppMacCompatibleVersions` 使用语义版本区间 notation：`[8.9.6,]` 表示 ≥8.9.6，
  `[8.9.6,9.0.0)` 表示 ≥8.9.6 且 <9.0.0。

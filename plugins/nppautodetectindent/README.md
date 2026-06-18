# Auto Detect Indention — macOS Native Plugin

**Identifier**: `nppautodetectindent`
**Version**: 1.0.0
**Implementation type**: easy

Detects indentation (tab or spaces) and auto-adjusts Tab settings. macOS native port of nppAutoDetectIndent.

## Commands

- **detect-indent**: Auto Detect Indentation

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `nppAutoDetectIndent`

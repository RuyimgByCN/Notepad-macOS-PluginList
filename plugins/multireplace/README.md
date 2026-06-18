# MultiReplace — macOS Native Plugin

**Identifier**: `multireplace`
**Version**: 1.0.0
**Implementation type**: medium_stub

Multi-pattern search & replace across files. macOS stub — multi-rule UI needs native panel.

## Commands

- **multi-replace**: Multi-Pattern Replace
- **apply-replace-list**: Apply Replace List

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `MultiReplace`

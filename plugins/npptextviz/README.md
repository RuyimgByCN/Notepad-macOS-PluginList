# NppTextViz — macOS Native Plugin

**Identifier**: `npptextviz`
**Version**: 1.0.0
**Implementation type**: easy

Hide/show lines by pattern for log analysis. macOS native port of NppTextViz.

## Commands

- **hide-matching-lines**: Hide Lines Matching Pattern
- **show-all-lines**: Show All Lines
- **hide-non-matching**: Hide Lines NOT Matching Pattern

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppTextViz`

# Markdown Table Editor — macOS Native Plugin

**Identifier**: `markdowntableeditor`
**Version**: 1.0.0
**Implementation type**: medium_stub

Markdown table alignment and editing. macOS stub — interactive table editing needs NSTableView UI.

## Commands

- **align-table**: Align Markdown Table
- **format-table**: Format Markdown Table
- **csv-to-table**: Convert CSV to Table

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `MarkdownTableEditor`

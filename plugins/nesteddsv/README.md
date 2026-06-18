# NestedDSV Data Visualizer — macOS Native Plugin

**Identifier**: `nesteddsv`
**Version**: 1.0.0
**Implementation type**: medium_stub

Hierarchical DSV data visualization. macOS stub — needs NSOutlineView panel UI.

## Commands

- **detect-dsv**: Detect DSV Format
- **extract-dsv-fields**: Extract DSV Fields

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NestedDSV`

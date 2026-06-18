# Fixed-width Data Visualizer — macOS Native Plugin

**Identifier**: `fwdataviz`
**Version**: 1.0.0
**Implementation type**: medium_stub

Fixed-width data visualization with column/field display. macOS stub — needs NSTableView native UI.

## Commands

- **detect-fixed-width**: Detect Fixed-Width Layout
- **extract-fields**: Extract Fields

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `FWDataViz`

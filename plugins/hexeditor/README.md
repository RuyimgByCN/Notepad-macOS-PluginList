# HEX-Editor — macOS Native Plugin

**Identifier**: `hexeditor`
**Version**: 1.0.0
**Implementation type**: medium_stub

Hex editor for binary files. macOS stub — needs native hex view panel.

## Commands

- **hex-dump**: Hex Dump Current File
- **hex-view-selection**: Hex View Selection

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `HexEditor`

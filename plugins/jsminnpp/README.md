# JSTool — macOS Native Plugin

**Identifier**: `jsminnpp`
**Version**: 1.0.0
**Implementation type**: easy

JavaScript formatting, minification, and JSON viewer. macOS native port of JSTool.

## Commands

- **format-js**: Format JavaScript
- **minify-js**: Minify JavaScript
- **json-view**: JSON Data Viewer

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `JSMinNPP`

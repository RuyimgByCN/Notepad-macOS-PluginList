# URL Encode/Decode Plugin — macOS Native Plugin

**Identifier**: `urlplugin`
**Version**: 1.0.0
**Implementation type**: easy

URL encode and decode selected text. macOS native port.

## Commands

- **url-encode**: URL Encode Selection
- **url-decode**: URL Decode Selection

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `urlPlugin`

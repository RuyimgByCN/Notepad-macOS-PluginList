# HTML Tag — macOS Native Plugin

**Identifier**: `htmltag`
**Version**: 1.0.0
**Implementation type**: easy

HTML/XML tag navigation, entity encoding/decoding, JS character encoding/decoding. macOS native port.

## Commands

- **encode-html-entities**: Encode HTML Entities
- **decode-html-entities**: Decode HTML Entities
- **encode-js-chars**: Encode JS Characters
- **decode-js-chars**: Decode JS Characters

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `HTMLTag`

# Emoji Description — macOS Native Plugin

**Identifier**: `emojidescription`
**Version**: 1.0.0
**Implementation type**: easy

Displays character encoding info: Unicode code point, decimal/hex values, HTML entity, UTF-8 bytes. macOS native port.

## Commands

- **char-info**: Show Character Info

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `EmojiDescription`

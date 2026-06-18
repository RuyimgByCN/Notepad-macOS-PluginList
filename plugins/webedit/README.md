# WebEdit — macOS Native Plugin

**Identifier**: `webedit`
**Version**: 1.0.0
**Implementation type**: easy

HTML tag abbreviation expansion and selection wrapping. macOS native port of WebEdit.

## Commands

- **expand-tag**: Expand Tag Abbreviation
- **wrap-selection**: Wrap Selection with Tag
- **remove-tag**: Remove Surrounding Tag

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `WebEdit`

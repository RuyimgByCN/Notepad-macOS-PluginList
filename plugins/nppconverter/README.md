# Npp Converter — macOS Native Plugin

**Identifier**: `nppconverter`
**Version**: 1.0.0
**Implementation type**: easy

ASCII to Hex and Hex to ASCII converter. macOS native port of Npp Converter.

## Commands

- **ascii-to-hex**: ASCII → Hex
- **hex-to-ascii**: Hex → ASCII

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `nppConverter`

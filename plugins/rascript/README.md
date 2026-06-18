# RAScript — macOS Native Plugin

**Identifier**: `rascript`
**Version**: 1.0.0
**Implementation type**: medium_stub

RAScript grammar definition and parsing. macOS stub — custom grammar parser needs native implementation.

## Commands

- **parse-rascript**: Parse RAScript
- **validate-rascript**: Validate RAScript Grammar

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `RAScript`

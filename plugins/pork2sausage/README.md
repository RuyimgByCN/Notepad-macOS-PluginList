# Pork to Sausage — macOS Native Plugin

**Identifier**: `pork2sausage`
**Version**: 1.0.0
**Implementation type**: easy

Pass selected text to any command-line program as input, replace selection with output. macOS native port.

## Commands

- **pipe-to-command**: Pipe Selection to Command

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `pork2sausage`

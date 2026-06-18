# RunMe — macOS Native Plugin

**Identifier**: `runme`
**Version**: 1.0.0
**Implementation type**: easy

Execute the currently open file based on shell association. macOS native port using open/exec.

## Commands

- **run-file**: Run Current File
- **run-in-terminal**: Run in Terminal
- **open-containing-folder**: Open Containing Folder

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `RunMe`

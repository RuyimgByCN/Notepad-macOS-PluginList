# Select N' Launch — macOS Native Plugin

**Identifier**: `selectnlaunch`
**Version**: 1.0.0
**Implementation type**: easy

Save selected text as temp file and open with system. macOS native port.

## Commands

- **select-and-launch**: Select N Launch
- **select-and-open**: Open Selection as File

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `selectNLaunch`

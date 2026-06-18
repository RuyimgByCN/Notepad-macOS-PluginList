# TakeNotes — macOS Native Plugin

**Identifier**: `takenotes`
**Version**: 1.0.0
**Implementation type**: medium_stub

Quick note-taking with timestamped filenames. macOS stub — needs native note panel UI.

## Commands

- **new-note**: Create New Note
- **open-last-note**: Open Last Note

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `TakeNotes`

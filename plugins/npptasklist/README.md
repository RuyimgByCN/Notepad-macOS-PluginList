# Task List — macOS Native Plugin

**Identifier**: `npptasklist`
**Version**: 1.0.0
**Implementation type**: easy

Scan document for TODO, FIXME, NOTE items. macOS native port of Task List.

## Commands

- **scan-todos**: Scan TODO Items
- **scan-fixmes**: Scan FIXME Items
- **scan-all-tasks**: Scan All Task Markers

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppTaskList`

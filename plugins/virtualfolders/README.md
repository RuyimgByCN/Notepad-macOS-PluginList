# Virtual Folders — macOS Native Plugin

**Identifier**: `virtualfolders`
**Version**: 1.0.0
**Implementation type**: medium_stub

Virtual folder tree panel for grouping files. macOS stub — needs NSTreeController/NSOutlineView UI.

## Commands

- **open-virtual-folders**: Open Virtual Folders Panel

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `VirtualFolders`

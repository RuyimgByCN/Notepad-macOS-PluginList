# NppCrossCheck — macOS Native Plugin

**Identifier**: `nppcrosscheck`
**Version**: 1.0.0
**Implementation type**: easy

Cross-check two lists in the current document. Shows intersection, difference, and union. macOS native port.

## Commands

- **cross-check**: Cross Check Two Lists
- **find-intersection**: Find Intersection
- **find-difference**: Find Difference (A - B)
- **find-union**: Find Union

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppCrossCheck`

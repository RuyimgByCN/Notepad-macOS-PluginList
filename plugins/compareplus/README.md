# ComparePlus — macOS Native Plugin

**Identifier**: `compareplus`
**Version**: 1.0.0
**Implementation type**: medium_stub

Advanced text comparison tool. macOS stub — dual-panel diff view needs native Swift UI.

## Commands

- **compare-selected**: Compare Selected Text
- **diff-files**: Diff Two Files

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `ComparePlus`

# LanguageHelp — macOS Native Plugin

**Identifier**: `languagehelp`
**Version**: 1.0.0
**Implementation type**: medium_stub

Language-specific help file viewer with keyword lookup. macOS stub — needs native help viewer.

## Commands

- **lookup-keyword**: Lookup Keyword in Help
- **open-help-file**: Open Help File

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `LanguageHelp`

# Notepad++ Plugin Demo — macOS Native Plugin

**Identifier**: `nppplugindemo`
**Version**: 1.0.0
**Implementation type**: na

NotepadMac plugin demo — demonstrates the macOS plugin API and manifest format.

## Commands

- **hello-world**: Hello World
- **show-info**: Show Plugin Info
- **count-words**: Count Words

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppPluginDemo`

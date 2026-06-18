# Notepad++ Plugin Template — macOS Native Plugin

**Identifier**: `nppplugintemplate`
**Version**: 1.0.0
**Implementation type**: na

NotepadMac plugin development template. Copy and modify to create new plugins.

## Commands

- **template-command**: Template Command

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppPluginTemplate`

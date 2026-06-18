# Notepad++ bplist plugin — macOS Native Plugin

**Identifier**: `nppbplistplugin`
**Version**: 1.0.0
**Implementation type**: medium_stub

Binary plist viewer/editor. macOS native port using plutil — full editing needs native UI.

## Commands

- **convert-bplist-to-xml**: Convert bplist to XML plist
- **convert-bplist-to-json**: Convert bplist to JSON
- **view-bplist-info**: View bplist Info

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppBplistPlugin`

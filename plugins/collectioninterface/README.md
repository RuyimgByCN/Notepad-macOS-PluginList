# CollectionInterface — macOS Native Plugin

**Identifier**: `collectioninterface`
**Version**: 1.0.0
**Implementation type**: medium_stub

Download and install UDL/Theme collections from GitHub. macOS stub — needs URLSession + native install UI.

## Commands

- **download-udl-list**: Download UDL List
- **download-theme-list**: Download Theme List

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `CollectionInterface`

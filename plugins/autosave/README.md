# AutoSave — macOS Native Plugin

**Identifier**: `autosave`
**Version**: 1.0.0
**Implementation type**: medium_stub

Auto-save files on timer or focus-loss. macOS native port — needs Swift Timer + NSDocument integration.

## Commands

- **save-all-now**: Save All Files Now
- **toggle-autosave**: Toggle Auto-Save

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `AutoSave`

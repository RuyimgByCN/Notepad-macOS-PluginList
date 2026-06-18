# Select to Clipboard — macOS Native Plugin

**Identifier**: `selecttoclipboard`
**Version**: 1.0.0
**Implementation type**: easy

Auto-copy selected text to clipboard (like PuTTY). macOS native port using pbcopy.

## Commands

- **copy-selection**: Copy Selection to Clipboard

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `SelectToClipboard`

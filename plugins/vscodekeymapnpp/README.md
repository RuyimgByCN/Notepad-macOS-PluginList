# VSCode Keymap NPP — macOS Native Plugin

**Identifier**: `vscodekeymapnpp`
**Version**: 1.0.0
**Implementation type**: medium_stub

VS Code keyboard shortcut mapping. macOS stub — needs native key binding translation layer.

## Commands

- **enable-vscode-keymap**: Enable VS Code Keymap
- **disable-vscode-keymap**: Disable VS Code Keymap

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `VSCodeKeymapNpp`

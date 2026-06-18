# NppVim — macOS Native Plugin

**Identifier**: `nppvim`
**Version**: 1.0.0
**Implementation type**: medium_stub

Vim-style editing mode and key bindings. macOS stub — needs native key-binding translation layer.

## Commands

- **toggle-vim-mode**: Toggle Vim Mode

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppVim`

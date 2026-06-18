# Snippets — macOS Native Plugin

**Identifier**: `nppsnippets`
**Version**: 1.0.0
**Implementation type**: medium_stub

Code snippet manager with panel UI. macOS stub — needs NSTableView snippet panel.

## Commands

- **insert-snippet**: Insert Snippet
- **list-snippets**: List Available Snippets

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppSnippets`

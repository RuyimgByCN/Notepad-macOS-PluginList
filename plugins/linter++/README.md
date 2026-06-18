# Linter++ — macOS Native Plugin

**Identifier**: `linter++`
**Version**: 1.0.0
**Implementation type**: easy

Real-time code linting against external linters (eslint, pylint, shellcheck, etc.). macOS native port.

## Commands

- **lint-file**: Lint Current File
- **lint-selection**: Lint Selection

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `Linter++`

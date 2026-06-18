# rustnpp — macOS Native Plugin

**Identifier**: `rustnpp`
**Version**: 1.0.0
**Implementation type**: easy

Run or build Rust cargo projects and .rs files. macOS native port using cargo CLI.

## Commands

- **cargo-run**: Cargo Run
- **cargo-build**: Cargo Build
- **cargo-test**: Cargo Test

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `rustnpp`

# SecurePad — macOS Native Plugin

**Identifier**: `securepad`
**Version**: 1.0.0
**Implementation type**: medium_stub

Encrypt/decrypt documents with AES-256. macOS native port using Security framework / gpg.

## Commands

- **encrypt-selection**: Encrypt Selection
- **decrypt-selection**: Decrypt Selection
- **encrypt-file**: Encrypt Current File
- **decrypt-file**: Decrypt Current File

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `SecurePad`

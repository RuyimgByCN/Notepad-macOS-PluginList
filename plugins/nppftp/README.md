# NppFTP — macOS Native Plugin

**Identifier**: `nppftp`
**Version**: 1.0.0
**Implementation type**: medium_stub

FTP/SFTP file browser and transfer. macOS stub — native file browser UI needed.

## Commands

- **sftp-download**: SFTP Download File
- **sftp-upload**: SFTP Upload File

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppFTP`

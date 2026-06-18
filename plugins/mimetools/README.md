# Mime tools — macOS Native Plugin

**Identifier**: `mimetools`
**Version**: 1.0.0
**Implementation type**: easy

MIME encoding/decoding: Base64, Quoted-printable, URL encode/decode. macOS native port.

## Commands

- **base64-encode**: Base64 Encode
- **base64-decode**: Base64 Decode
- **qp-encode**: Quoted-Printable Encode
- **qp-decode**: Quoted-Printable Decode
- **url-encode**: URL Encode
- **url-decode**: URL Decode

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `mimeTools`

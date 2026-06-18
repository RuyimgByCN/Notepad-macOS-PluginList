# Chinese Converter — macOS Native Plugin

**Identifier**: `nppchineseconverter`
**Version**: 1.0.0
**Implementation type**: easy

Traditional and Simplified Chinese conversion. macOS native port using OpenCC.

## Commands

- **t2s**: Traditional → Simplified
- **s2t**: Simplified → Traditional
- **t2tw**: Traditional → Taiwan
- **tw2t**: Taiwan → Traditional

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NppChineseConverter`

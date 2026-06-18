# SpeechPlugin — macOS Native Plugin

**Identifier**: `speechplugin`
**Version**: 1.0.0
**Implementation type**: hard_feasible

Text-to-speech using macOS built-in say command. macOS native port of SpeechPlugin.

## Commands

- **speak-selection**: Speak Selection
- **speak-document**: Speak Entire Document
- **stop-speaking**: Stop Speaking

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `SpeechPlugin`

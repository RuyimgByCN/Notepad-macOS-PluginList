# StayAwake — macOS Native Plugin

**Identifier**: `stayawake_npp`
**Version**: 1.0.0
**Implementation type**: hard_feasible

Prevent macOS sleep using caffeinate. macOS native port of StayAwake.

## Commands

- **enable-caffeinate**: Prevent Sleep (Caffeinate)
- **disable-caffeinate**: Allow Sleep (Disable Caffeinate)

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `StayAwake_NPP`

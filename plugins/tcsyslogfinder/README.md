# TC Syslog Finder — macOS Native Plugin

**Identifier**: `tcsyslogfinder`
**Version**: 1.0.0
**Implementation type**: medium_stub

Find and open Teamcenter syslog files. macOS stub — needs native file browser integration.

## Commands

- **find-syslog**: Find Latest Syslog
- **open-syslog-folder**: Open Syslog Folder

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `TCSyslogFinder`

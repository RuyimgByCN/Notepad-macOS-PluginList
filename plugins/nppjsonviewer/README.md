# JSON Viewer — macOS Native Plugin

**Identifier**: `nppjsonviewer`
**Version**: 1.0.0
**Implementation type**: easy

JSON formatter and minifier. macOS native port using python json.tool.

## Commands

- **format-json**: Format JSON
- **minify-json**: Minify JSON
- **validate-json**: Validate JSON

## Usage

This plugin runs as a shell script command. The NotepadMac host sets:
- `$1` = command identifier
- `stdin` = selected text (for text-processing commands)
- `NOTEPAD_MAC_EDIT_SCRIPT_FILE` = current file path (for file operations)

**Upstream reference**: `NPPJSONViewer`

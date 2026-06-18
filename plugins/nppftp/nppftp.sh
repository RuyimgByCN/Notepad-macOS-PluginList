#!/bin/bash
# NppFTP — macOS native plugin stub for NotepadMac
# Full implementation needs native file browser UI (URLSession + NSOutlineView)

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

# NPP_FTP_HOST, NPP_FTP_USER, NPP_FTP_PATH env vars for connection
HOST="${NPP_FTP_HOST:-}"
USER="${NPP_FTP_USER:-}"
REMOTEPATH="${NPP_FTP_PATH:-}"

case "$COMMAND" in
  sftp-download)
    if [ -z "$HOST" ] || [ -z "$REMOTEPATH" ]; then
        echo "Error: Set NPP_FTP_HOST and NPP_FTP_PATH environment variables" >&2
        exit 1
    fi
    if command -v sftp &> /dev/null; then
        sftp "${USER}@${HOST}:${REMOTEPATH}" /dev/stdout 2>/dev/null
    else
        echo "Error: sftp command not available" >&2
        exit 1
    fi
    ;;
  sftp-upload)
    if [ -z "$HOST" ] || [ -z "$FILE" ]; then
        echo "Error: Need file and host configuration" >&2
        exit 1
    fi
    if command -v sftp &> /dev/null; then
        echo "put $FILE $REMOTEPATH" | sftp "${USER}@${HOST}" 2>&1
    else
        echo "Error: sftp command not available" >&2
        exit 1
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

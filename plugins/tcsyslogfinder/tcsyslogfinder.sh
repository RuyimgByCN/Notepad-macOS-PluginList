#!/bin/bash
# TC Syslog Finder — macOS native plugin stub for NotepadMac
# Needs native file browser integration for full UI

COMMAND="$1"
# NPP_SYSLOG_DIR: directory containing syslog files
SYSLOG_DIR="${NPP_SYSLOG_DIR:-$HOME/Teamcenter/syslog}"

case "$COMMAND" in
  find-syslog)
    if [ -d "$SYSLOG_DIR" ]; then
        LATEST=$(ls -t "$SYSLOG_DIR"/syslog*.log 2>/dev/null | head -1)
        if [ -n "$LATEST" ]; then
            cat "$LATEST"
        else
            echo "No syslog files found in $SYSLOG_DIR" >&2
        fi
    else
        echo "Syslog directory not found: $SYSLOG_DIR" >&2
        echo "Set NPP_SYSLOG_DIR to your syslog path" >&2
    fi
    ;;
  open-syslog-folder)
    if [ -d "$SYSLOG_DIR" ]; then
        open "$SYSLOG_DIR"
    else
        echo "Directory not found: $SYSLOG_DIR" >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

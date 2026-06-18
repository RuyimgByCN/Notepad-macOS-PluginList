#!/bin/bash
# StayAwake — macOS native plugin for NotepadMac
# Uses macOS built-in 'caffeinate' command to prevent system sleep

COMMAND="$1"
PIDFILE="/tmp/npp-caffeinate.pid"

case "$COMMAND" in
  enable-caffeinate)
    if [ -f "$PIDFILE" ]; then
        OLD_PID=$(cat "$PIDFILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Caffeinate already active (PID: $OLD_PID)"
            exit 0
        fi
    fi
    caffeinate -i &
    echo $! > "$PIDFILE"
    echo "Caffeinate enabled — system will not sleep while active"
    ;;
  disable-caffeinate)
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        kill "$PID" 2>/dev/null
        rm -f "$PIDFILE"
        echo "Caffeinate disabled — system may sleep normally"
    else
        echo "No caffeinate process found" >&2
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

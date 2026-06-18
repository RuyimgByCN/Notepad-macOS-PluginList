#!/bin/bash
# SecurePad — macOS native plugin stub for NotepadMac
# Uses gpg for encryption (install: brew install gnupg)
# Full UI with password dialog needs native Swift implementation

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"
# NPP_ENCRYPT_PASSPHRASE env var for passphrase
PASS="${NPP_ENCRYPT_PASSPHRASE:-}"

case "$COMMAND" in
  encrypt-selection)
    if [ -z "$PASS" ]; then
        echo "Error: Set NPP_ENCRYPT_PASSPHRASE environment variable" >&2
        exit 1
    fi
    if command -v gpg &> /dev/null; then
        cat | gpg --batch --passphrase "$PASS" --symmetric --armor 2>/dev/null
    else
        echo "Error: gpg not installed. Install: brew install gnupg" >&2
        exit 1
    fi
    ;;
  decrypt-selection)
    if [ -z "$PASS" ]; then
        echo "Error: Set NPP_ENCRYPT_PASSPHRASE environment variable" >&2
        exit 1
    fi
    if command -v gpg &> /dev/null; then
        cat | gpg --batch --passphrase "$PASS" --decrypt 2>/dev/null
    else
        echo "Error: gpg not installed" >&2
        exit 1
    fi
    ;;
  encrypt-file)
    if [ -z "$FILE" ] || [ -z "$PASS" ]; then
        echo "Error: Need file path and passphrase" >&2
        exit 1
    fi
    gpg --batch --passphrase "$PASS" --symmetric --armor "$FILE" 2>/dev/null
    ;;
  decrypt-file)
    if [ -z "$FILE" ] || [ -z "$PASS" ]; then
        echo "Error: Need file path and passphrase" >&2
        exit 1
    fi
    gpg --batch --passphrase "$PASS" --decrypt "$FILE" 2>/dev/null
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

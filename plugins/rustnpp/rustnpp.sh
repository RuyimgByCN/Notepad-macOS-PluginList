#!/bin/bash
# rustnpp — macOS native plugin for NotepadMac
# Run/build Rust cargo projects

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

if ! command -v cargo &> /dev/null; then
    echo "Error: cargo is not installed. Install Rust: https://rustup.rs" >&2
    exit 1
fi

case "$COMMAND" in
  cargo-run)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        # Check if we're in a cargo project
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo run 2>&1
        else
            # Try parent directories
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo run 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo run 2>&1
    fi
    ;;
  cargo-build)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo build 2>&1
        else
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo build 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo build 2>&1
    fi
    ;;
  cargo-test)
    if [ -n "$FILE" ]; then
        DIR="$(dirname "$FILE")"
        if [ -f "$DIR/Cargo.toml" ]; then
            cd "$DIR" && cargo test 2>&1
        else
            PARENT="$(cd "$DIR/.." && pwd)"
            if [ -f "$PARENT/Cargo.toml" ]; then
                cd "$PARENT" && cargo test 2>&1
            else
                echo "Error: No Cargo.toml found" >&2
                exit 1
            fi
        fi
    else
        cargo test 2>&1
    fi
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

#!/bin/bash
# Linter++ — macOS native plugin for NotepadMac
# Runs external linters on the current file or selection

COMMAND="$1"
FILE="${NOTEPAD_MAC_EDIT_SCRIPT_FILE:-}"

case "$COMMAND" in
  lint-file)
    if [ -z "$FILE" ]; then
        echo "Error: No file path available" >&2
        exit 1
    fi

    # Determine linter based on file extension
    EXT="${FILE##*.}"
    case "$EXT" in
      js|jsx|ts|tsx|mjs)
        LINTER="eslint"
        ;;
      py|pyw)
        LINTER="pylint"
        ;;
      sh|bash)
        LINTER="shellcheck"
        ;;
      css|scss)
        LINTER="stylelint"
        ;;
      rb)
        LINTER="rubocop"
        ;;
      go)
        LINTER="golint"
        ;;
      *)
        LINTER="generic"
        ;;
    esac

    if [ "$LINTER" = "generic" ]; then
        echo "No specific linter for .$EXT files. Available: eslint, pylint, shellcheck, stylelint, rubocop" >&2
        exit 0
    fi

    if ! command -v "$LINTER" &> /dev/null; then
        echo "Error: $LINTER is not installed. Install it to enable linting." >&2
        exit 1
    fi

    "$LINTER" "$FILE" 2>&1
    ;;
  lint-selection)
    # Lint the selected text (stdin)
    if [ -z "$FILE" ]; then
        echo "Error: No file context available" >&2
        exit 1
    fi
    # Write selection to temp file and lint it
    TMPFILE=$(mktemp /tmp/npp-lint-XXXXXX."${FILE##*.}")
    cat > "$TMPFILE"
    EXT="${FILE##*.}"
    case "$EXT" in
      js|jsx|ts|tsx|mjs)
        LINTER="eslint"
        ;;
      py|pyw)
        LINTER="pylint"
        ;;
      sh|bash)
        LINTER="shellcheck"
        ;;
      *)
        LINTER="echo"
        ;;
    esac

    if command -v "$LINTER" &> /dev/null && [ "$LINTER" != "echo" ]; then
        "$LINTER" "$TMPFILE" 2>&1
    else
        echo "No linter available for .$EXT" >&2
    fi
    rm -f "$TMPFILE"
    ;;
  *)
    echo "Unknown command: $COMMAND" >&2
    exit 1
    ;;
esac

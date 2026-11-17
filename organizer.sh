#!/usr/bin/env bash
# Archive the current grades.csv and replace it with a new empty file.

set -u

SOURCE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

# The source file must exist before archiving.
if [[ ! -f "$SOURCE" ]]; then
    echo "Error: source file '$SOURCE' does not exist." >&2
    exit 1
fi

# Create the archive directory when it is missing.
if ! mkdir -p "$ARCHIVE_DIR"; then
    echo "Error: could not create archive directory '$ARCHIVE_DIR'." >&2
    exit 1
fi

# Never overwrite an existing archive with the same timestamp.
if [[ -e "$ARCHIVED_PATH" ]]; then
    echo "Error: archive file '$ARCHIVED_PATH' already exists; not overwriting." >&2
    exit 1
fi

# Move the existing CSV into the archive.
if ! mv -- "$SOURCE" "$ARCHIVED_PATH"; then
    echo "Error: failed to move '$SOURCE' to '$ARCHIVED_PATH'." >&2
    exit 1
fi

# Create a new, completely empty replacement CSV (zero bytes).
if ! : > "$SOURCE"; then
    echo "Error: failed to create empty replacement file '$SOURCE'." >&2
    exit 1
fi

# Append a log entry, preserving previous entries.
if ! printf '%s | original=%s | archived=%s\n' "$TIMESTAMP" "$SOURCE" "$ARCHIVED_PATH" >> "$LOG_FILE"; then
    echo "Error: failed to append to '$LOG_FILE'." >&2
    exit 1
fi

echo "Archived '$SOURCE' to '$ARCHIVED_PATH' and created an empty '$SOURCE'."

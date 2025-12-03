# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================
LOG_FILE="logs/preprocessed.logs"
PYTHON_SCRIPT="src/preprocessed.py"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message "================================"
log_message "=== Starting data preprocessing ==="
log_message "================================"
log_message "Python script: $PYTHON_SCRIPT"

# run and capture stdout and stderr - and also add timestamps to python outputs
if python3 "$PYTHON_SCRIPT" 2>&1 | while IFS= read -r line; do
    log_message "$line"
done; then
    log_message "  SUCCESS: Data preprocessing completed!"
    log_message "=== Preprocessing completed ==="
    log_message "==============================="
    log_message ""
    exit 0
else
    EXIT_CODE=$?
    log_message "  ERROR  : Data preprocessing failed! Exit code: $EXIT_CODE"
    log_message "=== Preprocessing failed ==="
    log_message "============================"
    log_message ""
    exit $EXIT_CODE
fi

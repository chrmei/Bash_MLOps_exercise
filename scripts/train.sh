# -----------------------------------------------------------------------------
# This script train.sh runs the Python program src/train.py.
# This program trains a prediction model and saves the final model
# in the model/ directory. The script also logs all execution details
# in the file logs/train.logs.
# -----------------------------------------------------------------------------
LOG_FILE="logs/train.logs"
PYTHON_SCRIPT="src/train.py"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message "================================"
log_message "=== Starting model training ==="
log_message "================================"
log_message "Python script: $PYTHON_SCRIPT"

# run and capture stdout and stderr - and also add timestamps to python outputs
if python3 "$PYTHON_SCRIPT" 2>&1 | while IFS= read -r line; do
    log_message "$line"
done; then
    log_message "  SUCCESS: Model training completed!"
    log_message "=== Training completed ==="
    log_message "==============================="
    log_message ""
    exit 0
else
    EXIT_CODE=$?
    log_message "  ERROR  : Model training failed! Exit code: $EXIT_CODE"
    log_message "=== Training failed ==="
    log_message "============================"
    log_message ""
    exit $EXIT_CODE
fi

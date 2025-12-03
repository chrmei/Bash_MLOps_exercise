# ==============================================================================
# Script: collect.sh
# Description:
#   This script queries an API to retrieve sales data for the following graphics card models:
#     - rtx3060
#     - rtx3070
#     - rtx3080
#     - rtx3090
#     - rx6700
#
#   The collected data is appended to a copy of the file:
#     data/raw/sales_data.csv
#
#   The output file is saved in the format:
#     data/raw/sales_YYYYMMDD_HHMM.csv
#   with the following columns:
#     timestamp, model, sales
#
#   Collection activity (requests, queried models, results, errors)
#   is recorded in a log file:
#     logs/collect.logs
#
#   The log should be human-readable and must include:
#     - The date and time of each request
#     - The queried models
#     - The retrieved sales data
#     - Any possible errors
# ==============================================================================

API_URL="http:/0.0.0.0:5000/"
LOG_FILE="logs/collect.logs"
DATA_DIR="data/raw"
SOURCE_CSV="$DATA_DIR/sales_data.csv" # given in repository through exam

GRAPHIC_CARDS_MODELS=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")

CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

TIMESTAMP_FILENAME=$(date +"%Y%m%d_%H%M")

OUTPUT_CSV="$DATA_DIR/sales_${TIMESTAMP_FILENAME}.csv"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message "================================"
log_message "=== Starting data collection ==="
log_message "Timestamp: $CURRENT_TIMESTAMP"
log_message "Output file: $OUTPUT_CSV"

# as SOURCE_CSV is given in repository, I do not check if file exists
cp "$SOURCE_CSV" "$OUTPUT_CSV"
log_message "Copied $SOURCE_CSV to $OUTPUT_CSV"

# in a test, last line of OUTPUT_CSV contained an error when appending ( original sales_data.csv ended not witha a newline.)
# so: check if last byte is newline, if yes: append newline to output csv
if [ "$(tail -c 1 "$OUTPUT_CSV" 2>/dev/null | od -An -tx1)" != " 0a " ]; then
log_message "  INFO   : Appending newline to $OUTPUT_CSV"
    echo "" >> "$OUTPUT_CSV"
fi

# query API for each model and append to OUTPUT_CSV
for model in "${GRAPHIC_CARDS_MODELS[@]}"; do
    FULL_API_URL="${API_URL}/${model}"
    log_message "Querying API for model: $model with $FULL_API_URL"
    
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    SALES=$(curl -s "$FULL_API_URL" 2>&1)
    CURL_EXIT_CODE=$?

    if [ $CURL_EXIT_CODE -eq 0 ]; then
        # valid number?
        if [[ "$SALES" =~ ^[0-9]+$ ]]; then
            # append
            echo "$TIMESTAMP,$model,$SALES" >> "$OUTPUT_CSV"
            log_message "  SUCCESS: $model: $SALES sales"
        else
            log_message "  ERROR  : Invalid response for $model: '$SALES' - not a number"
        fi
    else
        log_message     "  ERROR  : Failed to query API for $model. Curl exit code: $CURL_EXIT_CODE"
        log_message     "  ERROR  : Response: $SALES"
    fi
done

log_message ""
log_message "================================="
log_message "Total models queried: ${#GRAPHIC_CARDS_MODELS[@]}"
log_message "Output file: $OUTPUT_CSV"
log_message "Log file: $LOG_FILE"
log_message "=== Data collection completed ==="
log_message ""
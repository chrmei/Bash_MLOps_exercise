import pandas as pd
from pathlib import Path
from datetime import datetime
from contextlib import redirect_stdout

# Log directories
LOGS_DIR = Path('logs/tests_logs')
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / 'test_preprocessed.logs'

def get_latest_processed_file():
    """Returns the most recent 'sales_processed_*.csv' file from data/processed."""
    processed_dir = Path('data/processed')
    processed_files = list(processed_dir.glob('sales_processed_*.csv'))

    if not processed_files:
        return None

    return max(processed_files, key=lambda f: f.stat().st_mtime)

def check_timestamp_column(file_path):
    """Returns True if the 'timestamp' column is absent, otherwise False."""
    df = pd.read_csv(file_path)
    return 'timestamp' not in df.columns

def check_integer_columns(file_path):
    """Returns True if all columns (except 'timestamp') are of integer type."""
    df = pd.read_csv(file_path)
    for column in df.columns:
        if column == 'timestamp':
            continue
        if not pd.api.types.is_integer_dtype(df[column]):
            return False
    return True

def test_preprocessed_file():
    log_file_path = LOG_FILE
    with open(log_file_path, "a") as f, redirect_stdout(f):
        print(f"\n=== Test started ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

        latest_file = get_latest_processed_file()
        if latest_file is None:
            print("No preprocessed file found.")
            assert False, "No preprocessed file to test."

        print("Starting structure test for the preprocessed file")
        print(f"Loaded file: {latest_file}")

        no_timestamp = check_timestamp_column(latest_file)
        if no_timestamp:
            print("Timestamp column check: OK (not present)")
        else:
            print("The file contains a 'timestamp' column")
        assert no_timestamp, "The file contains a 'timestamp' column, which is not allowed."

        all_ints = check_integer_columns(latest_file)
        if all_ints:
            print("Integer type check: OK (all columns are integers)")
        else:
            print("The file contains non-integer columns")
        assert all_ints, "The file contains columns that are not of integer type."

        print("Test completed for the preprocessed file.")
        print(f"=== Test ended ===\n")

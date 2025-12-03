"""
-------------------------------------------------------------------------------
This script `preprocessed.py` retrieves data from the latest CSV file created
in the 'data/raw/' directory.

1. It applies preprocessing to the data.

2. The results of the preprocessing are saved in a new CSV file
   in the 'data/processed/' directory, with a name formatted as
   'sales_processed_YYYYMMDD_HHMM.csv'.

3. All preprocessing steps are logged in the
   'logs/preprocessed.logs' file to ensure detailed tracking of the process.

Any errors or anomalies are also logged to ensure traceability.
-------------------------------------------------------------------------------
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime


def find_latest_csv_file(raw_dir: str) -> str:
    files = os.listdir(raw_dir)
    csv_files = [raw_dir / f for f in files if f.endswith(".csv")]
    if not csv_files:
        print("ERROR: No raw CSV files found")
        exit(1)

    ts_files = []
    for f in csv_files:
        # expecting format "sales_YYYYMMDD_HHmm.csv"
        parts = f.name.split("_")
        if (
            len(parts) == 3 and parts[0] == "sales"
        ):  # now also checking for these formats
            ts_parts = "_".join(parts[1:])
            ts = ts_parts.replace(".csv", "")
            if len(ts) == 13 and "_" in ts:
                ts_files.append(f)

    if not ts_files:
        print("  ERROR: No CSV files matching expected pattern found!")
        exit(1)

    latest_ts = ""
    latest_file = None
    for f in ts_files:
        ts = f.name.split("_")[1].replace(".csv", "")
        if ts > latest_ts:
            latest_ts = ts
            latest_file = f

    return latest_file


def load_data(file_path):
    print(f"Loaindg: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Data Loaded: {len(df)} rows, {len(df.columns)} columns")
    return df


if __name__ == "__main__":

    raw_dir = Path("data/raw")

    latest_file = find_latest_csv_file(raw_dir)

    df = load_data(latest_file)

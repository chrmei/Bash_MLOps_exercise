import os
from pathlib import Path
import pandas as pd


def find_latest_csv_file(dir_path: str) -> Path:
    """Find the latest CSV file matching the pattern sales_YYYYMMDD_HHMM.csv"""
    dir_path = Path(dir_path)
    files = os.listdir(dir_path)
    csv_files = [dir_path / f for f in files if f.endswith(".csv")]
    if not csv_files:
        print("  ERROR: No raw CSV files found")
        exit(1)

    ts_files = []
    for f in csv_files:
        # accepts format "sales_YYYYMMDD_HHmm.csv" or "sales_processed_YYYYMMDD_HHmm.csv"
        parts = f.name.split("_")
        if (
            len(parts) in [3, 4] and parts[0] == "sales"
        ):  # now also checking for these formats
            ts_parts = "_".join(parts[-2:])
            ts = ts_parts.replace(".csv", "")
            if len(ts) == 13 and "_" in ts:
                ts_files.append(f)

    if not ts_files:
        print("  ERROR: No CSV files matching expected pattern found!")
        exit(1)

    latest_ts = ""
    latest_file = None
    for f in ts_files:
        ts = "_".join(f.name.split("_")[-2:])
        ts = ts.replace(".csv", "")
        if ts > latest_ts:
            latest_ts = ts
            latest_file = f

    return latest_file


def load_data(file_path: Path):
    """Load CSV data and return dataframe"""
    print(f"  Loading: {file_path}")
    df = pd.read_csv(file_path)
    print(f"  Data Loaded: {len(df)} rows, {len(df.columns)} columns")
    return df

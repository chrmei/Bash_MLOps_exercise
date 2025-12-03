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
from sklearn.preprocessing import LabelEncoder


def find_latest_csv_file(raw_dir: str) -> str:
    """Find the latest CSV file matching the pattern sales_YYYYMMDD_HHMM.csv"""
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
    """Load CSV data and return dataframe"""
    print(f"Loading: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Data Loaded: {len(df)} rows, {len(df.columns)} columns")
    return df


def convert_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Convert timestamp column to datetime and remove invalid entries"""
    print("Converting timestamp column...")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    invalid_count = df["timestamp"].isna().sum()

    if invalid_count > 0:
        print(f"Removing {invalid_count} rows with invalid timestamps")
        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
    else:
        print("No invalid timestamps found!")
    print("Timestamps successfully converted.")

    return df


def extract_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract hour, day_of_week, day_of_month, and month from timestamp"""
    print("Extracting temporal features...")
    df["hour"] = df["timestamp"].dt.hour.astype(int)
    df["day_of_week"] = df["timestamp"].dt.dayofweek.astype(int)
    df["day_of_month"] = df["timestamp"].dt.day.astype(int)
    df["month"] = df["timestamp"].dt.month.astype(int)
    return df


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with negative sales values"""
    print("Cleaning sales data...")
    negative_count = (df["sales"] < 0).sum()

    if negative_count > 0:
        print(f"Removing {negative_count} rows with negative sales")
        df = df[df["sales"] >= 0].reset_index(drop=True)

    return df


def encode_model_column(df: pd.DataFrame) -> pd.DataFrame:
    """Encode model column using LabelEncoder"""
    print("Encoding model column...")
    le = LabelEncoder()
    df["model_encoded"] = le.fit_transform(df["model"]).astype(int)

    mapping = {cls: int(code) for cls, code in zip(le.classes_, le.transform(le.classes_))}

    print(f"Model encoding: {mapping}")
    return df


if __name__ == "__main__":

    raw_dir = Path("data/raw")

    latest_file = find_latest_csv_file(raw_dir)

    df = load_data(latest_file)

    df = convert_timestamps(df)

    df = extract_temporal_features(df)

    df = clean_sales_data(df)

    df = encode_model_column(df)

    print("\n", df.head())

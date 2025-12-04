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
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from helper import find_latest_csv_file, load_data


def convert_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Convert timestamp column to datetime and remove invalid entries"""
    print("  Converting timestamp column...")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    invalid_count = df["timestamp"].isna().sum()

    if invalid_count > 0:
        print(f"    Removing {invalid_count} rows with invalid timestamps")
        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
    else:
        print("    No invalid timestamps found!")
    print("  Timestamps successfully converted.")

    return df


def extract_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract hour, day_of_week, day_of_month, and month from timestamp"""
    print("  Extracting temporal features...")
    df["year"] = df["timestamp"].dt.year.astype(int)
    df["hour"] = df["timestamp"].dt.hour.astype(int)
    df["day_of_week"] = df["timestamp"].dt.dayofweek.astype(int)
    df["day_of_month"] = df["timestamp"].dt.day.astype(int)
    df["month"] = df["timestamp"].dt.month.astype(int)
    return df


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with negative sales values"""
    print("  Cleaning sales data...")
    negative_count = (df["sales"] < 0).sum()

    if negative_count > 0:
        print(f"Removing {negative_count} rows with negative sales")
        df = df[df["sales"] >= 0].reset_index(drop=True)

    return df


def encode_model_column(df: pd.DataFrame) -> pd.DataFrame:
    """Encode model column using LabelEncoder"""
    print("  Encoding model column...")
    le = LabelEncoder()
    df["model_encoded"] = le.fit_transform(df["model"]).astype(int)

    mapping = {
        cls: int(code) for cls, code in zip(le.classes_, le.transform(le.classes_))
    }

    print(f"    Model encoding: {mapping}")
    return df


def drop_original_columns(df):
    """Drop timestamp and model columns"""
    print("  Dropping original timestamp and model columns...")
    df = df.drop(columns=["timestamp", "model"])
    return df


def reorder_columns(df):
    """Reorder into a meaningful order, target last."""
    print("  Reordering columns...")
    df = df[["model_encoded", "year", "month", "day_of_week", "hour", "sales"]]
    return df


def save_processed_data(
    target_dir: str, df: pd.DataFrame, initial_rows: int, original_path: Path
):
    """Save processed dataframe to CSV file"""
    processed_dir_path = Path(target_dir)

    output_filename = original_path.name.replace("sales_", "sales_processed_")

    output_path = processed_dir_path / output_filename

    df.to_csv(output_path, index=False)

    final_rows = len(df)

    print(f"  Final preprocessed data: {final_rows} rows, {len(df.columns)} columns")
    print(f"  Rows removed: {initial_rows - final_rows}")
    print(f"  Preprocessed data saved to {output_path}")


if __name__ == "__main__":
    raw_dir = "data/raw"
    procseed_dir = "data/processed"

    latest_file = find_latest_csv_file(raw_dir)
    df = load_data(latest_file)
    initial_rows = len(df)

    df = convert_timestamps(df)

    df = extract_temporal_features(df)

    df = clean_sales_data(df)

    df = encode_model_column(df)

    df = drop_original_columns(df)

    df = reorder_columns(df)

    save_processed_data(procseed_dir, df, initial_rows, latest_file)
import os
from pathlib import Path
import pandas as pd


def find_latest_csv_file(dir_path: str) -> Path:
    """Find the latest CSV file matching the pattern sales_YYYYMMDD_HHMM.csv.
    
    Args:
        dir_path: Directory path to search for CSV files
        
    Returns:
        Path to the latest CSV file matching the expected pattern
        
    Raises:
        FileNotFoundError: If directory doesn't exist or no CSV files found
        ValueError: If no files match the expected pattern
    """
    dir_path = Path(dir_path)
    
    # Check if directory exists
    if not dir_path.exists():
        raise FileNotFoundError(
            f"Directory not found: {dir_path}. "
            f"Please ensure the directory exists before running preprocessing/training."
        )
    
    if not dir_path.is_dir():
        raise ValueError(
            f"Path is not a directory: {dir_path}. "
            f"Expected a directory path containing CSV files."
        )
    
    try:
        files = os.listdir(dir_path)
    except PermissionError as e:
        raise PermissionError(
            f"Permission denied accessing directory {dir_path}. "
            f"Please check directory permissions. Original error: {e}"
        )
    
    csv_files = [dir_path / f for f in files if f.endswith(".csv")]
    if not csv_files:
        available_files = [f for f in files if not f.startswith('.')][:5]  # Show first 5 non-hidden files
        raise FileNotFoundError(
            f"No CSV files found in directory: {dir_path}. "
            f"Expected CSV files matching pattern 'sales_YYYYMMDD_HHMM.csv'. "
            f"Available files (sample): {available_files if available_files else 'none'}. "
            f"Please ensure data collection has been run to generate CSV files."
        )

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
        found_csv_names = [f.name for f in csv_files[:5]]  # Show first 5 CSV files
        raise ValueError(
            f"No CSV files matching expected pattern found in {dir_path}. "
            f"Expected pattern: 'sales_YYYYMMDD_HHMM.csv' or 'sales_processed_YYYYMMDD_HHMM.csv'. "
            f"Found CSV files (sample): {found_csv_names}. "
            f"Please ensure files follow the expected naming convention."
        )

    latest_ts = ""
    latest_file = None
    for f in ts_files:
        ts = "_".join(f.name.split("_")[-2:])
        ts = ts.replace(".csv", "")
        if ts > latest_ts:
            latest_ts = ts
            latest_file = f

    return latest_file


def load_data(file_path: Path) -> pd.DataFrame:
    """Load CSV data and return dataframe.
    
    Args:
        file_path: Path to the CSV file to load
        
    Returns:
        Loaded dataframe
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
        pd.errors.ParserError: If the file cannot be parsed as CSV
    """
    print(f"  Loading: {file_path}")
    
    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}. "
            f"Please ensure the file exists and the path is correct."
        )
    
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(
            f"CSV file is empty: {file_path}. "
            f"Please ensure the file contains data before processing."
        )
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(
            f"Failed to parse CSV file: {file_path}. "
            f"The file may be corrupted or not in valid CSV format. "
            f"Original error: {e}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error loading CSV file: {file_path}. "
            f"Original error: {type(e).__name__}: {e}"
        )
    
    if df.empty:
        raise ValueError(
            f"Loaded CSV file is empty (0 rows): {file_path}. "
            f"Please ensure the file contains data before processing."
        )
    
    print(f"  Data Loaded: {len(df)} rows, {len(df.columns)} columns")
    return df

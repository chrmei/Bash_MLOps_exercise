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

raw_dir = Path("data/raw")
files = os.listdir(raw_dir)
csv_files = [raw_dir / f for f in files if f.endswith(".csv")]
if not csv_files:
    print("ERROR: No raw CSV files found")
    exit(1)

print(csv_files)

latest_stamp = ""
for f in csv_files:
    # expecting format "sales_YYYYMMDD_HHmm.csv"
    ts = f.name.split("_")[1].replace(".csv","") # --> YYYYMMDD_HHmm
    if ts > latest_stamp: # good old string comparison
        latest_stamp = ts
        latest_file = f

print(f"Loading: {latest_file}")

# Load data
df = pd.read_csv(latest_file)
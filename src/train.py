"""
-------------------------------------------------------------------------------
This script runs the training of an XGBoost model to predict graphics card sales
from the preprocessed data.

1. It starts by searching for the latest preprocessed CSV file in the 'data/processed/' directory.
2. If a standard model (model.pkl) does not exist, it loads the data, splits it into training and test sets, trains a model on this data, evaluates it, and then saves it as 'model/model.pkl'.
3. If a standard model already exists, it trains a new model on the latest data, evaluates it, and saves the model in the 'model/' folder in the format: model_YYYYMMDD_HHMM.pkl.
4. Performance metrics (RMSE, MAE, R²) are displayed and saved in the log file.
5. Any errors are handled and reported in the logs.

The models are saved in the 'model/' folder with the name 'model.pkl' for the standard model and with a timestamp for later versions.
The model metrics are recorded in the script’s log files.
-------------------------------------------------------------------------------
"""
import os 
from helper import find_latest_csv_file, load_data
from datetime import datetime
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score


def check_model_exists(model_path: str) -> bool:
    model_exists = os.path.exists(model_path)
    if model_exists:
        print("    Standard model available!")
    else:
        print("    Standard model not available!")
    return model_exists


def prepare_data(df: pd.DataFrame):
    """ Data splitting into features and target. """
    X = df.drop(columns=["sales"])
    y = df["sales"]
    return X, y


def split_train_test(X: pd.DataFrame, y: pd.DataFrame, test_size=0.2, random_state=42) -> tuple:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"    Training set: {len(X_train)} samples")
    print(f"    Test set: {len(X_test)} samples")

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, random_state=42, n_estimators=100, max_depth=6):
    model = xgb.XGBRegressor(
        random_state=random_state,
        n_estimators=n_estimators,
        max_depth=max_depth
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test) -> tuple:
    y_pred = model.predict(X_test)

    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return rmse, mae, r2


def print_metrics(rmse, mae, r2):
    print("  Model Performance Metrics:")
    print(f"    RMSE: {rmse:.4f}")
    print(f"    MAE:  {mae:.4f}")
    print(f"    R²:   {r2:.4f}")


def get_model_filename(model_exists: bool) -> str:
    if not model_exists:
        return "model/model.pkl"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"model/model_{timestamp}.pkl"


def save_model(model, filepath: str):
    with open(filepath, "wb") as f:
        pickle.dump(model, f)
    print(f"    Model saved to {filepath}")


if __name__ == "__main__":
    processed_path = "data/processed"
    standard_model_path = "model/model.pkl"

    try:
        # 1. Get latest preprocessed CSV file in the 'data/processed/' directory.
        print("  Find latest processed CSV file...")
        latest_file = find_latest_csv_file(processed_path)
        df = load_data(latest_file)
        print(f"  Found and loaded latest file {latest_file=}")

        # 2. Standard model (model.pkl) available? 
        print("  Check if standard model exists...")
        model_exists = check_model_exists(standard_model_path)

        # 3. Prep data - Feature & Target
        print("  Seperate data into feature and target...")
        X, y = prepare_data(df)

        # 4. Split
        print("  Split data into train & test...")
        X_train, X_test, y_train, y_test = split_train_test(X, y)

        # 5. Train Model
        print("  Start training of the model...")
        model = train_model(X_train, y_train)

        # 6. Evaluate model
        print("  Evaluating model...")
        rmse, mae, r2 = evaluate_model(model, X_test, y_test)

        # 8. Metrics
        print_metrics(rmse, mae, r2)

        # 9. Save model (logics)
        print("  Saving model...")
        model_filename = get_model_filename(model_exists)
        save_model(model, model_filename)

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        raise

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
from typing import Tuple
from helper import find_latest_csv_file, load_data
from datetime import datetime
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

# Configuration constants
TEST_SIZE = 0.2  # Proportion of data for testing (~80/20 train/test split)
RANDOM_STATE = 42  # Random seed for reproducibility
N_ESTIMATORS = 100  # Number of boosting rounds for XGBoost
MAX_DEPTH = 6  # Maximum tree depth to manage overfitting


def check_model_exists(model_path: str) -> bool:
    model_exists = os.path.exists(model_path)
    if model_exists:
        print("    Standard model available!")
    else:
        print("    Standard model not available!")
    return model_exists


def prepare_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Data splitting into features and target.
    
    Args:
        df: Input dataframe with features and target column 'sales'
        
    Returns:
        Tuple of (X, y) where X is features dataframe and y is target series
    """
    X = df.drop(columns=["sales"])
    y = df["sales"]
    return X, y


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into training and test sets.
    
    Args:
        X: Feature dataframe
        y: Target series
        test_size: Proportion of data to use for testing (default: 0.2 for ~80/20 split)
        random_state: Random seed for reproducibility (default: 42)
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"    Training set: {len(X_train)} samples")
    print(f"    Test set: {len(X_test)} samples")

    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = RANDOM_STATE,
    n_estimators: int = N_ESTIMATORS,
    max_depth: int = MAX_DEPTH,
) -> xgb.XGBRegressor:
    """Train XGBoost model for sales prediction.
    
    XGBoost configuration — tuned for sales prediction:
    - n_estimators: Number of boosting rounds (default: 100)
      Higher values can improve performance but increase training time
    - max_depth: Maximum tree depth to manage overfitting (default: 6)
      Prevents the model from becoming too complex and overfitting to training data
    - random_state: Seed for reproducibility (default: 42)
      Ensures consistent results across runs
    
    Args:
        X_train: Training feature dataframe
        y_train: Training target series
        random_state: Random seed for reproducibility
        n_estimators: Number of boosting rounds
        max_depth: Maximum tree depth
        
    Returns:
        Trained XGBoost regressor model
    """
    model = xgb.XGBRegressor(
        random_state=random_state, n_estimators=n_estimators, max_depth=max_depth
    )
    model.fit(X_train, y_train)
    return model


def check_model_metrics_quality(rmse: float, mae: float, r2: float) -> None:
    """Check model metrics for potential issues and warn if needed.
    
    Args:
        rmse: Root Mean Squared Error
        mae: Mean Absolute Error
        r2: R-squared score
    """
    # Warn on very low R² (poor model fit)
    if r2 < 0.0:
        print(
            f"  WARNING: Negative R² score ({r2:.4f}) indicates model performs worse "
            f"than a simple mean baseline. Model may need retraining or feature engineering."
        )
    elif r2 < 0.3:
        print(
            f"  WARNING: Low R² score ({r2:.4f}) suggests weak model performance. "
            f"Consider feature engineering or hyperparameter tuning."
        )
    
    # Warn on very high RMSE relative to MAE (indicates high variance)
    if mae > 0:
        rmse_mae_ratio = rmse / mae
        if rmse_mae_ratio > 2.0:
            print(
                f"  WARNING: High RMSE/MAE ratio ({rmse_mae_ratio:.2f}) suggests "
                f"model has high prediction variance. Consider regularization."
            )


def evaluate_model(
    model: xgb.XGBRegressor, X_test: pd.DataFrame, y_test: pd.Series
) -> Tuple[float, float, float]:
    """Evaluate model performance on test data.
    
    Args:
        model: Trained XGBoost model
        X_test: Test feature dataframe
        y_test: Test target series
        
    Returns:
        Tuple of (rmse, mae, r2) metrics
    """
    y_pred = model.predict(X_test)

    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Check metrics quality
    check_model_metrics_quality(rmse, mae, r2)
    
    return rmse, mae, r2


def print_metrics(rmse: float, mae: float, r2: float) -> None:
    """Print model performance metrics.
    
    Args:
        rmse: Root Mean Squared Error
        mae: Mean Absolute Error
        r2: R-squared score
    """
    print("  Model Performance Metrics:")
    print(f"    RMSE: {rmse:.4f}")
    print(f"    MAE:  {mae:.4f}")
    print(f"    R²:   {r2:.4f}")


def get_model_filename(model_exists: bool) -> str:
    """Generate model filename based on whether standard model exists.
    
    Args:
        model_exists: Whether the standard model.pkl file exists
        
    Returns:
        Filename path for the model
    """
    if not model_exists:
        return "model/model.pkl"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"model/model_{timestamp}.pkl"


def save_model(model: xgb.XGBRegressor, filepath: str) -> None:
    """Save trained model to pickle file.
    
    Args:
        model: Trained XGBoost model to save
        filepath: Path where model should be saved
    """
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
        if not latest_file:
            raise ValueError(
                f"No processed CSV files found in {processed_path}. "
                f"Please ensure preprocessing has been run and files exist in the directory."
            )
        if not latest_file.exists():
            raise FileNotFoundError(
                f"Processed CSV file not found at {latest_file}. "
                f"The file path was identified but does not exist on disk."
            )
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

    except FileNotFoundError as e:
        print(f"  ERROR: File not found during training - {str(e)}")
        raise
    except ValueError as e:
        print(f"  ERROR: Validation error in training - {str(e)}")
        raise
    except Exception as e:
        print(
            f"  ERROR: Unexpected error during model training. "
            f"Operation: training XGBoost model on data from {processed_path}. "
            f"Error type: {type(e).__name__}. "
            f"Details: {str(e)}"
        )
        raise

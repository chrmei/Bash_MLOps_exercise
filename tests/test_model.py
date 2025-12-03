from pathlib import Path
from datetime import datetime
from contextlib import redirect_stdout

# Log file configuration
LOG_FILE = Path("logs/tests_logs/test_model.logs")
MODEL_PATH = Path("model/model.pkl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """Appends a timestamped message to the log file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{now},000 - {level} - {message}\n")

def test_model_file_exists():
    """Test to check if the model file exists."""
    with open(LOG_FILE, "a") as f, redirect_stdout(f):
        print(f"\n=== Test started ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
        print("Starting test for model file presence")
        
        if MODEL_PATH.is_file():
            log(f"Model found: {MODEL_PATH}")
            print("Test passed: The model file exists.")
        else:
            log(f"The model '{MODEL_PATH}' was not found in model/", level="ERROR")
            log("Test failed with error: Unable to find the model file.", level="ERROR")
            print("Test failed: The model file is missing.")
            assert False, "Model file is missing"
        
        print(f"=== Test completed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")

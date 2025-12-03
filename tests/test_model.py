<<<<<<< HEAD
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
=======
from pathlib import Path
from datetime import datetime
from contextlib import redirect_stdout

# Configuration du fichier de log
LOG_FILE = Path("logs/tests_logs/test_model.logs")
MODEL_PATH = Path("model/model.pkl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """Ajoute un message horodaté dans le fichier de log."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{now},000 - {level} - {message}\n")

def test_model_file_exists():
    """Test de la présence du fichier modèle"""
    with open(LOG_FILE, "a") as f, redirect_stdout(f):
        print(f"\n=== Début des tests ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
        print("Début du test de présence du fichier modèle")
        
        if MODEL_PATH.is_file():
            log(f"Modèle trouvé : {MODEL_PATH}")
            print("Test réussi : le fichier modèle existe.")
        else:
            log(f"Le modèle '{MODEL_PATH}' est introuvable dans model/", level="ERROR")
            log("Test échoué avec l'erreur: Impossible de trouver le fichier modèle.", level="ERROR")
            print("Test échoué : Le fichier modèle est manquant.")
            assert False, "Fichier modèle manquant"
        
        print(f"=== Fin des tests ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
>>>>>>> main

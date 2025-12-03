<<<<<<< HEAD
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
=======
"""
-------------------------------------------------------------------------------
Ce script exécute l'entraînement d'un modèle XGBoost pour prédire les ventes de 
cartes graphiques à partir des données prétraitées.

1. Il commence par rechercher le dernier fichier CSV prétraité dans le dossier 
   'data/processed/'.
2. Si un modèle standard (model.pkl) n'existe pas, il charge les données, les 
   divise en ensembles d'entraînement et de test, entraîne un modèle sur ces 
   données, l'évalue, puis le sauvegarde dans 'model/model.pkl'.
3. Si un modèle standard existe déjà, il entraîne un nouveau modèle sur les 
   données les plus récentes, l'évalue, puis sauvegarde le modèle dans le dossier 
   'model/' sous formats : model_YYYYMMDD_HHMM.pkl.
4. Les métriques de performance (RMSE, MAE, R²) sont affichées et sauvegardées dans 
   le fichier de log.
5. Des erreurs éventuelles sont gérées et signalées dans les logs.

Les modèles sont sauvegardés dans le dossier 'model/' avec le nom 'model.pkl' pour 
le modèle standard et avec un horodatage pour les versions ultérieures.
Les métriques du modèle sont enregistrées dans les logs du script.
-------------------------------------------------------------------------------
"""
>>>>>>> main

import mlflow
import subprocess


subprocess.Popen(["mlflow", "models", "serve", "-m", "https://github.com/Edsondev21/Projet_7/tree/main/mlflow_model"])



   # "mlflow models serve -m https://github.com/Edsondev21/Projet_7/tree/main/mlflow_model", shell = True, bufsize = 0, stdout = subprocess.PIPE)
  #
#mlflow models serve -m mlflow_model/

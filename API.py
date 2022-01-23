import mlflow
import subprocess
import streamlit as st
import os

os.environ["AWS_ACCESS_KEY_ID"]=st.secrets["AWS_ACCESS_KEY_ID"] 
os.environ["AWS_SECRET_ACCESS_KEY"]=st.secrets["AWS_SECRET_ACCESS_KEY"] 

#subprocess.Popen(["mlflow", "models", "serve", "-m", "s3://mlflowmodel/mlflow_model/"])

mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=5.0

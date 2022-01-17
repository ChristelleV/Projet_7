import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
import json
import App1
import App2
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import subprocess


subprocess.Popen("mlflow", "models", "serve", "-m", "runs:/mlflow_model/C:/Users/sonas/Desktop/Projet 7")


st.sidebar.title('Tableau de bord pour prédiction de crédit ')
st.sidebar.subheader("Navigation")

PAGES = {"Vue Générale": App1,
         "Prédiction client": App2}

selection = st.sidebar.radio("Aller à", list(PAGES.keys()))
page = PAGES[selection]
page.app()





# Préparation des données
df = get_data()      
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df.loc[:5000]

dt = df.drop(['TARGET'], axis=1)
Y = df['TARGET']

X = pd.read_csv(r"C:\Users\sonas\Desktop\Projet 7\X_scal.csv")
X.drop(['Unnamed: 0'], axis=1, inplace=True)
X = X.loc[:5000]

#####################################

# Fonction de prediction via l'API
def request_prediction(data):
    headers = {"Content-Type": "application/json"}
    #data_json = {'data': data}
    response = requests.request(
        method='POST', headers=headers, url='http://127.0.0.1:5000/invocations', json=data)
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))
    return response

def request_pred(data):
    url = "http://127.0.0.1:5000/invocations"
    dat = data.to_json(orient='split')
# headers de la requête
    headers = {'Content-type': 'application/json'}
# la requête
    r = requests.post("http://127.0.0.1:5000/invocations", data=json.dumps(dat), headers=headers)
    if r.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(r.status_code, r.text))

    return r

mlflow_url = 'http://127.0.0.1:5000/invocations'




############################################################################






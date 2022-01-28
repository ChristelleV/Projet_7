import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
import json
import App1
import App2
#import API_Flask
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import subprocess
from subprocess import Popen, PIPE
import os

###################################################################################


#############################################################################

st.sidebar.title('Tableau de bord pour prédiction de crédit ')
st.sidebar.subheader("Navigation")

PAGES = {"Vue Générale": App1,
         "Prédiction client": App2}

selection = st.sidebar.radio("Aller à", list(PAGES.keys()))
page = PAGES[selection]
page.app()



#####################################


# Préparation des données
df = pd.read_csv('https://raw.githubusercontent.com/Edsondev21/Projet_7/main/data2.csv')    
df.drop(['Unnamed: 0'], axis=1, inplace=True)

dt = df.drop(['TARGET'], axis=1)
Y = df['TARGET']

X = pd.read_csv("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/X_scaled.csv")
X.drop(['Unnamed: 0'], axis=1, inplace=True)



app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)


if __name__ == '__main__':
    modelfile = 'final_prediction.pickle'
    model = p.load(open(modelfile, 'rb'))
    app.run(host='127.0.0.1') --no-reload


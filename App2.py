# app2.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import mlflow
import numpy as np
import lightgbm
from lightgbm import LGBMClassifier
import lime
from lime import lime_tabular
import pickle
import joblib
import streamlit.components.v1 as components
from flask import Flask, request, redirect, url_for, flash, jsonify
import subprocess
import sys
#import API_Flask


# Run Flask API as a subprocess
subprocess.Popen([f"{sys.executable}", "API_Flask.py"])
# ---------------------------------------------------------------


df = pd.read_csv("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/data2.csv")
df.drop(['Unnamed: 0'], axis=1, inplace=True)

dt = df.drop(['TARGET'], axis = 1)
X = pd.read_csv("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/X_scaled.csv")
X.drop(['Unnamed: 0'], axis=1, inplace=True)

Y = df['TARGET']

#model = joblib.load("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/mdl.pkl")
#model = pickle.load(open("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/mdl.pkl", 'rb'))
model = open('mdl.pkl', 'wb')



 ############################################### API Mlflow ###########################################
    
    
def request_pred(data):
 
    headers = {"Content-Type": "application/json"}
    r = requests.post("http://127.0.0.1:5000/invocations", data=data, headers=headers)    # #"https://share.streamlit.io/edsondev21/projet_7/main/API.py"
    if r.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(r.status_code, r.text))
    return r.json()

####################################################### API Flask ##########################################


def request_flask(data):
    #url =  'http://0.0.0.0:5000/api/'   #'https://share.streamlit.io/edsondev21/projet_7/main/API_Flask.py'  # 'http://127.0.0.1:5000/api/'
    LOGIN_URL = 'https://share.streamlit.io/edsondev21/projet_7/main/API_Flask.py'
    request = requests.session()
    request.get(LOGIN_URL)
    csrftoken = request.cookies['csrftoken']
    j_data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    r1 = requests.post(LOGIN_URL, data=j_data, headers=headers)
    new_csrftoken = r1.cookies['csrftoken']
    payload = {'csrfmiddlewaretoken': new_csrftoken,'data':data }
    try :
       r2 = request.post('http://127.0.0.1:8000/myview/myview', data=payload, headers={'X-CSRFToken': r1.cookies['crsftoken']})
    except :
       print('error expected')
    
    if r1.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(r.status_code, r.text))
    return r2.json()

############################################

def req_flask(data):
    url = 'http://127.0.0.1:5000/api/'                             #'http://127.0.0.1:5000/api/'
    j_data = json.dumps(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=j_data, headers=headers)
    if r.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(r.status_code, r.text))
    return r.json()


#################################

def app():
    st.title('Prédiction client')
    st.subheader("Bienvenue sur l'outil de prédiction")
    client = st.selectbox("Choisissez le numéro d'un client", dt['SK_ID_CURR'].index)

    # Afficher caractéristiques du client choisi
    st.write("Tableau de données du client choisi")

    st.dataframe(dt[dt['SK_ID_CURR'].index == client])

    st.write('')

    ################################################## Visualisation des informations client ##################################

    choix = st.radio("Que voulez vous faire ?", ["Visualiser les informations du client", "Prédiction"])

    if choix == "Visualiser les informations du client":

        def countPlotclient(feature):
            fig = plt.figure(figsize=(6, 4))
            sns.countplot(x=feature, data=df, hue='TARGET', palette=['green', "red"])
            plt.axvline(x=df[df['SK_ID_CURR'] == client][feature].name, linewidth=5)
            st.pyplot(fig)

        def kde_client(feature, xlab, titre):
            fig2 = plt.figure(figsize=(6, 4))
            sns.kdeplot(df.loc[df['TARGET'] == 0, feature], label='target == 0', color='green', linewidth=3)
            sns.kdeplot(df.loc[df['TARGET'] == 1, feature], label='target == 1', color='red', linewidth=3)
            plt.xlabel(xlab, size=13)
            plt.ylabel('Densité', size=13)
            plt.title(titre, size=16)
            plt.axvline(x= df[df['SK_ID_CURR'].index == client][feature].values, ymin=0, ymax=1, linewidth=5)
            plt.legend(labels=["Target 0", "Target 1"])
            st.pyplot(fig2)

        st.write('Position du client')

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        st.set_option('deprecation.showPyplotGlobalUse', False)
        with col1:
            st.write(countPlotclient('CODE_GENDER'))
        with col2:
            st.write(kde_client('Age', '', 'Age du client'))
        with col3:
            st.write(kde_client('Annee_travail', '', "Années d'experience professionnel"))
        with col4:
            st.write(kde_client('AMT_INCOME_TOTAL', '', 'Revenu total'))
        with col5:
            st.write(kde_client('AMT_CREDIT', '', 'Montant du crédit'))
        with col6:
            st.write(kde_client('EXT_SOURCE_3', '', 'Source exterieure'))


        st.write("Voulez vous visualiser d'autres variables ?")
        
        dv= dt.drop(['SK_ID_CURR', 'CODE_GENDER', 'Annee_travail', 'Age', 'AMT_INCOME_TOTAL',
                     'AMT_CREDIT', 'EXT_SOURCE_3', 'FLAG_DOCUMENT_3', 'FLAG_MOBIL','FLAG_EMP_PHONE','FLAG_WORK_PHONE',
                   'FLAG_CONT_MOBILE','FLAG_PHONE','FLAG_EMAIL', 'CNT_FAM_MEMBERS'], axis=1)
        
        variable = st.selectbox("Choisissez la variable à visualiser", dv.columns)
        cat = ['NAME_CONTRACT_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE',
               'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS']
        
        if variable in cat :
            st.write(countPlotclient(variable))
        else:
            st.write(kde_client(variable, '', ''))


########################################################### Prediction ###############################################


    else:
        pred_btn = st.button('Prédire', client)
        if pred_btn:

            b = (X[X.index == client]).to_json(orient='split')

            pred = req_flask(X[X.index == client].to_json(orient='split'))

            explainer = lime_tabular.LimeTabularExplainer(training_data=np.array(X),
                                                      feature_names=X.columns,
                                                      class_names=['0', '1'],
                                                      mode='classification')


            exp = explainer.explain_instance(data_row= X.iloc[client],  predict_fn=model.predict_proba,
                                             num_features=10, labels = (1, 0))
            taux = (model.predict_proba(X[X.index == client])[0][0])*100

            if pred == [1.0]:

                st.markdown(
                    f'<h1 style="text-align: center; color:red;font-size:24px;">{"Le crédit est malheureusement refusé"}</h1>',
                    unsafe_allow_html=True)

                latest_iteration = st.empty()
                bar = st.progress(0)
                latest_iteration.text(f" Les probabilitées de remboursement sont de {int(taux)}% ")
                bar.progress(int(taux))
                st.markdown(
                """
                <style>
                    .stProgress > div > div > div > div {
                        background-color: red;
                    }
                </style>""",  unsafe_allow_html=True,)
            else:
                st.markdown(f'<h1 style="text-align: center; color:green;font-size:24px;'
                            f'">{"Felicitations le crédit est accordé"}</h1>',
                            unsafe_allow_html=True)
                st.write('')

                latest_iteration = st.empty()
                bar = st.progress(0)
                latest_iteration.text(f" Les probabilitées de remboursement sont de {int(taux)}% ")
                bar.progress(int(taux))
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: green;      }
                    </style>""", unsafe_allow_html=True, )
            st.write('')
            st.markdown(f'<h1 style="text-align: center; color:black;font-size:18px;'
                        f'">{"Ci dessous les 10 variables les plus importantes influant sur la décision"}</h1>',
                        unsafe_allow_html=True)

            st.write('')
            st.write(exp.as_pyplot_figure(label = 0))

            st.write("Ci-dessus vous pouvez voir les variables qui corrèlent à la classe 0, proportionnelle à leur apport. "
                     "En vert celles qui apportent une contribution positive et en rouge celles apportant une contribution négative. "
                     "En face de chaque variable il y a la valeur seuil expliquant la contribution positive ou négative ")

            st.write('')
            with st.expander("Plus d'informations"):
                exp1 = explainer.explain_instance(data_row=X.iloc[client], predict_fn=model.predict_proba,
                                                 num_features=10)
                components.html(exp1.as_html(show_predicted_value=False),
                                width=900, height=1000, scrolling=True)





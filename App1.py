# app1.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Préparation des données
df = pd.read_csv("https://raw.githubusercontent.com/Edsondev21/Projet_7/main/data2.csv")
df.drop(['Unnamed: 0'], axis=1, inplace=True)

dt = df.drop(['TARGET'], axis = 1)

# Fonctions affichage de graphiques
def countPlot(feature, hu, titre):
  fig = plt.figure(figsize=(6, 4))
  sns.countplot(x = feature, data = df, hue = hu, palette=['green',"red"])
  plt.title(titre)
  st.pyplot(fig)

def kde(feature, xlab, titre):
  fig2 = plt.figure(figsize = (6, 4))
  sns.kdeplot(df.loc[df['TARGET'] == 0, feature], label = 'target == 0', color = 'green', linewidth=3)
  sns.kdeplot(df.loc[df['TARGET'] == 1, feature], label = 'target == 1', color = 'red', linewidth=3)
  plt.xlabel(xlab, size = 13)
  plt.ylabel('Densité', size = 13)
  plt.title(titre, size =16)
  plt.legend(labels=["Target 0","Target 1"])
  st.pyplot(fig2)

def app():
    st.title('Vue Générale')
    st.write('Présentation des données')
    st.dataframe(df)

    st.write('')
    st.write('Données graphiques des variables principales')
    st.write('')
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    st.set_option('deprecation.showPyplotGlobalUse', False)
    with col1:
        st.write(fig=countPlot("CODE_GENDER", "TARGET", 'Distribution du sexe'), use_container_width=True)
    with col2:
        st.write(kde('Age', 'Age (en année)', "Distribution de l'âge"), use_container_width=True)
    with col3:
        st.write(kde('Annee_travail', 'Experience professionnel', "Distribution de l'experience professionnel"),
                 use_container_width=True)
    with col4:
        st.write(fig=countPlot("TARGET", None, ""), use_container_width=False)
    with col5:
        st.write(kde('AMT_GOODS_PRICE', 'Prix du bien', ""), use_container_width=True)
    with col6:
        st.write(kde('EXT_SOURCE_3', 'Source exterieur', ""), use_container_width=True)


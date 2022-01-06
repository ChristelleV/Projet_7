
# Project 7: Implémenter un modèle de scoring

Le but du projet est de mettre en œuvre un outil de “scoring crédit” pour calculer la probabilité qu’un client rembourse son crédit à travers 
le développement d'un algorithme de classification 


Le modèle devra ensuite être utilisé pour développer un dashboard interactif 
permettant l'exploration des informations personnelles et l'explication 
des décisions d’octroi de crédit


## Données

Les données sont issus de la compétition kaggle: : "Home Credit Default Risk" de laquelle seul le fichier 'application_train.csv' a été utilisé 
## Features

- Données personnelles (âge, sexe, éducation, foyer...)
- Données bancaires (revenu, montant du crédit, montant du bien...)
- Données sur les comportements d'achat (de dernière voiture, téléphone...)
- Scores issus de données externes


## Modèle et déploiement API


### Preprocessing

Les données ont été partagées entre 80% pour l'entrainement et 20% pour la validation. Les valeures manquantes ont été imputé par la médiane de chaque colonne. 
Les valeures numériques ont été standardisé par StandardScaler et les valeurs catégorielles encodé par OneHotEncoder

### Modélisation

L'entrainement d'un RandomForestClassifier étant trop lente et le fbeta_score trop mauvais c'est le modèle LightGBM qui a été selectionné. 
Le AUC du modèle est de 76% et son fbeta_score de 83%

### Déploiement API

Le modèle a été déployé via Mlflow Models 

## Tableau de bord


Le tableau de bord devra contenir au minimum les fonctionnalités suivantes :
- Permettre de visualiser le score et l’interprétation de ce score pour chaque client 
- Permettre de visualiser des informations descriptives relatives à un client (via un système de filtre)
- Permettre de comparer les informations descriptives relatives à un client à l’ensemble des clients


Le projet a été conçu avec Streamlit.
N'étant pas en local (mais sur colab) il faudra passer par un localtunnel pour obtenir le lien vers celui-ci

Pour cela, dans la cellule de code, il faudra taper:

```bash
  !streamlit run app.py & npx localtunnel --port 8501
```
## Authors

- [@SonaSukiasyan](https://github.com/Edsondev21)


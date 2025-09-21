

# Package ETL

![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![GitHub stars](https://img.shields.io/github/stars/<votre-username>/<votre-repo>?style=social)

Un package Python modulaire pour créer des pipelines ETL (**Extraction, Transformation, Chargement**) sur des données tabulaires.

---

## Installation

Vous pouvez installer le package depuis PyPI ou localement via pip :

```bash
# Depuis PyPI (si publié)
pip install etl-package

# Depuis un dépôt local
pip install /chemin/vers/le/dossier/etl_package 
```


# Fonctionnalités
Le package fournit plusieurs modules :

Extraction

ExtractionData : extraction de données depuis web .

Exploration / QA

ValeurDouble, ValeurManquante : détection des doublons et valeurs manquantes.

Imputation

Imputateur, ImputateurML : imputation simple ou supervisée.

Normalisation

NormaliserColonne : normalisation Min-Max.

Remplacement

RemplacementColonne : remplacement de valeurs ou sous-chaînes.

Feature Engineering

FeatureEngineering : création de colonnes dérivées (ratios, différences, moyennes glissantes…)

Gestion des anomalies

ZScoreAnomalie, GestionOutliers : détection et traitement des valeurs aberrantes.

Encodage

EncodeurCategoriel : encodage des variables catégorielles.

Chargement

Loader : chargement dans base de données ou fichiers.

# Exemple d'utilisation


import pandas as pd
from etl_package import ExtractionData,Imputateur, NormaliserColonne, GestionOutliers

from etl_package import ExtractionData 

url = "https://content.codecademy.com/courses/beautifulsoup/cacao/index.html"

colonnes = ["Company", "Origin", "Rating", "CocoaPercent"]
noms_final = ["Company", "Origine spécifique du haricot", "Rating", "CocoaPercentage"]

df = ExtractionData.extract_webscrapping(
    url, 
    columns_to_extract=colonnes, 
    rename_columns=noms_final
)


## Imputation des valeurs manquantes
df['age'] = Imputateur.imputer_colonne(df, 'age', strategie="moyenne")

## Normalisation
df = NormaliserColonne.normaliser_colonne_choisie(df, 'revenu')

## Gestion des outliers
df = GestionOutliers.gerer_outliers(df, 'age', strategie='median')

# Licence
MIT License

# Auteur
Mozart Codjo (codjomozart@gmail.com)

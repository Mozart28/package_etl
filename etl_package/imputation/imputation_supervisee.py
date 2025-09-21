

import pandas as pd
from sklearn.base import BaseEstimator

class ImputateurML:
    """
    Classe permettant d'imputer une colonne contenant des NaN
    à l'aide d'un modèle de ML fourni par l'utilisateur.
    """

    @staticmethod
    def imputer_colonne_ml(
        df: pd.DataFrame,
        colonne_cible: str,
        modele: BaseEstimator
    ) -> pd.DataFrame:
        """
        Impute les valeurs manquantes d'une colonne avec un modèle ML.
        Affiche toujours un message sur l'état de l'imputation.

        Paramètres
        ----------
        df : pd.DataFrame
            Jeu de données.
        colonne_cible : str
            Colonne à imputer.
        modele : BaseEstimator
            Modèle scikit-learn déjà instancié (ex: RandomForestRegressor).

        Retour
        ------
        pd.DataFrame
            Colonne imputée.
        """


        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un DataFrame pandas.")
        

        if colonne_cible not in df.columns:
            raise ValueError(f"La colonne '{colonne_cible}' est absente du DataFrame.")
        

        if not isinstance(modele, BaseEstimator):
            raise TypeError("Le modèle doit être un objet scikit-learn (BaseEstimator).")


        s = df[colonne_cible]

       
        if s.isna().sum() == 0:
            print(f" Colonne '{colonne_cible}' ne contient aucun NaN → aucune imputation nécessaire.")
            return s

      
        X = df.drop(columns=[colonne_cible])
        X_train = X[s.notna()]
        y_train = s[s.notna()]
        X_pred = X[s.isna()]

        if X_train.empty:
            print("Pas de lignes disponibles pour entraîner le modèle. Imputation impossible.")
            return s
        if X_pred.empty:
            print("Aucune valeur à imputer.")
            return s

        try:
            
            modele.fit(X_train, y_train)

            y_pred = modele.predict(X_pred)

           
            s.loc[s.isna()] = y_pred

            print(f"Imputation ML appliquée sur '{colonne_cible}' pour {len(y_pred)} valeurs manquantes.")

            return s

        except Exception as e:
            print(f" Erreur lors de l'imputation ML : {e}")
            return s

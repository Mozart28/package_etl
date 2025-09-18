import pandas as pd
import numpy as np

class ZScoreAnomalie:
    """ 
    Cette classe permet de détecter les anomalies par la méthode du Z-score.
    """
    
    @staticmethod
    def calcul_zscore(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
        """
        Détecte les valeurs aberrantes dans une colonne numérique en utilisant le Z-score.

        Paramètres
        ----------
        df : pd.DataFrame
            La DataFrame contenant les données.
        colonne : str
            Le nom de la colonne à analyser.

        Retour
        ------
        pd.DataFrame ou None
            - DataFrame contenant la colonne spécfiée uniquement les valeurs aberrantes si elles existent.
            - None si aucune valeur aberrante n'est trouvée (message affiché).
        """
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df doit être un pandas DataFrame")
        
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' n'existe pas dans la DataFrame")
        
        if not pd.api.types.is_numeric_dtype(df[colonne]):
            raise TypeError(f"La colonne '{colonne}' doit être de type numérique (int ou float)")
        
      
        series = df[colonne].dropna()
        
        if series.empty:
            print(f"La colonne '{colonne}' est vide ou ne contient que des NaN.")
            return
        
        mean = series.mean()
        std = series.std()
        
        if std == 0 or np.isnan(std):
            print(f"La colonne '{colonne}' a une variance nulle, pas de détection possible.")
            return
        
        lim_sup = mean + 3 * std
        lim_inf = mean - 3 * std
        
        val_aber = df.loc[(df[colonne] > lim_sup) | (df[colonne] < lim_inf), colonne]
        nbre = val_aber.shape[0]
        
        if val_aber.empty:
            print(f"Aucune valeur aberrante détectée dans la colonne '{colonne}'.")
            return
        else:
            print(f"La colonne {colonne} contient {nbre} valeurs abérantes")
            return val_aber

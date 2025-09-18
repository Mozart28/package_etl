import pandas as pd

class NormaliserColonne:
    """
    Cette classe permet de normaliser une colonne d'un DataFrame
    entre 0 et 1 avec la méthode Min-Max.
    """

    @staticmethod
    
    def normaliser_colonne_choisie(df: pd.DataFrame, col: str, as_new: str | None = None) -> pd.DataFrame:
        """
        Normalise une colonne d'un DataFrame entre 0 et 1.
        
        Arguments
        ----------
        df : pd.DataFrame 
            Le DataFrame dont on veut normaliser une colonne
        col : str
            Le nom de la colonne à normaliser
        as_new : str | None, default=None
            - Si None : la colonne est remplacée
            - Si str  : la colonne normalisée est stockée sous ce nom
        
        Returns
        -------
        pd.DataFrame
            Le DataFrame avec la colonne normalisée
        """
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df doit être un DataFrame pandas")
        
        if df.empty:
            print("⚠️ Le DataFrame est vide.")
            return df
        
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' n'existe pas dans le DataFrame")
        
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"La colonne '{col}' doit être numérique pour être normalisée.")
        
        df = df.copy()
        
        col_min, col_max = df[col].min(), df[col].max()
        
        if col_min == col_max:
            print(f"Impossible de normaliser : la colonne '{col}' contient une valeur constante ({col_min}).")
            return df
        
        try:
            normalized = (df[col] - col_min) / (col_max - col_min)
            if as_new is None:
                df[col] = normalized
                print(f"La colonne '{col}' a été normalisée entre 0 et 1 (remplacement).")
            else:
                if as_new in df.columns:
                    print(f"Attention : la colonne '{as_new}' existe déjà, elle sera écrasée.")
                df[as_new] = normalized
                print(f"La colonne '{col}' a été normalisée entre 0 et 1 et stockée dans '{as_new}'.")
        except Exception as e:
            raise ValueError(f"Erreur lors de la normalisation de '{col}' : {e}")
        
        return df

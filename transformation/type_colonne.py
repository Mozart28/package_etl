import pandas as pd

class TypeColonne:
    """
    Cette classe permet de changer le type d'une ou plusieurs colonnes d'un DataFrame.
    """

    @staticmethod
    def changer_type_colonne(df: pd.DataFrame, cols, type_, inplace: bool = False) -> pd.DataFrame:
        """
        Change le type d'une ou plusieurs colonnes d'un DataFrame.
        
        Arguments
        ----------
        df : pd.DataFrame 
            Le DataFrame dont on veut modifier une ou plusieurs colonnes
        cols : str ou list
            Le(s) nom(s) de colonne(s) à modifier
        type_ : type ou str
            Le nouveau type de données (ex: int, float, str ou 'category')
        inplace : bool, default=False
            - True : modifie le DataFrame original
            - False : renvoie une copie modifiée
        
        Returns
        -------
        pd.DataFrame
            Le DataFrame avec les colonnes converties au nouveau type
        """
        
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame pandas")
        
        if df.empty:
            print("⚠️ Le DataFrame est vide.")
            return df
        
      
        if isinstance(cols, str):
            cols = [cols]
        elif not isinstance(cols, list):
            raise ValueError("cols doit être une chaîne (colonne unique) ou une liste de colonnes")
       
        missing_cols = [c for c in cols if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Colonnes inexistantes dans le DataFrame: {missing_cols}")
        
      
        target_df = df if inplace else df.copy()
        
        for col in cols:
            try:
                target_df[col] = target_df[col].astype(type_)

                print(f"La colonne '{col}' a été convertie en {target_df[col].dtype}")

            except Exception as e:
                print(f"Erreur lors de la conversion de '{col}' en {type_} : {e}")
        
        return None if inplace else target_df

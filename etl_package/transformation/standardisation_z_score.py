

import pandas as pd
import numpy as np
from typing import Union, List, Optional


class Standardisation:
    """
    Classe pour appliquer une standardisation z-score sur une ou plusieurs colonnes d'un DataFrame.
    """

    @staticmethod
    
    def zscore(
        df: pd.DataFrame,
        colonnes: Union[str, List[str]],
        inplace: bool = False,
        prefix: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Applique la standardisation z-score (centrage-réduction) sur les colonnes spécifiées.

        Paramètres
        ----------
        df : pd.DataFrame
            Le DataFrame contenant les données.
        colonnes : str ou list de str
            Colonne(s) numérique(s) à standardiser.
        inplace : bool, default=False
            Si True, modifie directement df. Sinon, retourne une copie.
        prefix : str ou None
            Préfixe pour nommer la nouvelle colonne (ex: "std_"). 
            Si None et inplace=False, on remplace les colonnes originales.

        Retour
        ------
        pd.DataFrame
            DataFrame avec colonnes standardisées.
        """
        if isinstance(colonnes, str):
            colonnes = [colonnes]

        if inplace:
            df_out = df
        else:
            df_out = df.copy()

        for col in colonnes:
            if col not in df_out.columns:
                raise ValueError(f"La colonne '{col}' est absente du DataFrame.")
            if not np.issubdtype(df_out[col].dtype, np.number):
                raise TypeError(f"La colonne '{col}' doit être numérique.")

            mean = df_out[col].mean()
            std = df_out[col].std(ddof=0)  

            z = (df_out[col] - mean) / std

            if inplace:
                df_out[col] = z
            else:
                new_col = f"{prefix}{col}" if prefix else col
                df_out[new_col] = z

        return df_out

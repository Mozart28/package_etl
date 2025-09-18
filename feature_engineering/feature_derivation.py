import pandas as pd
import numpy as np
from typing import Literal, Optional


class FeatureEngineering:
    """
    Classe pour créer des features dérivés génériques (ratios, différences, moyennes mobiles, etc.)
    """

    Strategy = Literal["ratio", "difference", "rolling_mean", "rolling_std", "lag"]

    @staticmethod
    def creer_feature(
        df: pd.DataFrame,
        methode: Strategy,
        col1: str,
        col2: Optional[str] = None,
        *,
        window: Optional[int] = None,
        periods: int = 1,
        new_col: Optional[str] = None,
        inplace: bool = False,
    ) -> pd.DataFrame:
        """
        Crée une nouvelle feature dérivée selon la méthode choisie.

        Paramètres
        ----------
        df : pd.DataFrame
            Le DataFrame contenant les données.
        methode : {"ratio", "difference", "rolling_mean", "rolling_std", "lag"}
            Méthode de création de la feature.
        col1 : str
            Première colonne (ou la seule pour rolling/lag).
        col2 : str, optionnel
            Deuxième colonne (utile pour ratio et difference).
        window : int, optionnel
            Fenêtre pour les méthodes rolling.
        periods : int, default=1
            Décalage pour la méthode lag.
        new_col : str, optionnel
            Nom de la nouvelle colonne. Si None, un nom par défaut est généré.
        inplace : bool, default=False
            Si True, modifie directement df. Sinon, retourne une copie.

        Retour
        ------
        pd.DataFrame
            DataFrame avec la feature créée.
        """
        if col1 not in df.columns:
            raise ValueError(f"La colonne '{col1}' est absente du DataFrame.")
        if col2 and col2 not in df.columns:
            raise ValueError(f"La colonne '{col2}' est absente du DataFrame.")

        df_out = df if inplace else df.copy()

        if methode == "ratio":
            if not col2:
                raise ValueError("La méthode 'ratio' nécessite col2.")
            col_name = new_col or f"{col1}_over_{col2}"
            df_out[col_name] = df_out[col1] / df_out[col2].replace(0, np.nan)

        elif methode == "difference":
            if not col2:
                raise ValueError("La méthode 'difference' nécessite col2.")
            col_name = new_col or f"{col1}_minus_{col2}"
            df_out[col_name] = df_out[col1] - df_out[col2]

        elif methode == "rolling_mean":
            if not window:
                raise ValueError("La méthode 'rolling_mean' nécessite un paramètre window.")
            col_name = new_col or f"{col1}_rolling_mean_{window}"
            df_out[col_name] = df_out[col1].rolling(window=window, min_periods=1).mean()

        elif methode == "rolling_std":
            if not window:
                raise ValueError("La méthode 'rolling_std' nécessite un paramètre window.")
            col_name = new_col or f"{col1}_rolling_std_{window}"
            df_out[col_name] = df_out[col1].rolling(window=window, min_periods=1).std()

        elif methode == "lag":
            col_name = new_col or f"{col1}_lag_{periods}"
            df_out[col_name] = df_out[col1].shift(periods=periods)

        else:
            raise ValueError(f"Méthode '{methode}' non supportée.")

        return df_out

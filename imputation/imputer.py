

import pandas as pd
import numpy as np
from typing import Literal, Any


class Imputateur:
    """
    Classe permettant d'imputer les valeurs manquantes d'une colonne
    avec la moyenne, la médiane ou le mode.
    """

    Strategy = Literal["moyenne", "mediane", "mode", "mean", "median"]

    @staticmethod
    def imputer_colonne(
        df: pd.DataFrame,
        colonne: str,
        strategie: Strategy = "moyenne",
        *,
        fallback: Any | None = None,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Impute les valeurs manquantes d'une colonne uniquement si elle contient des NaN.

        Paramètres
        ----------
        df : pd.DataFrame
            Jeu de données.
        colonne : str
            Nom de la colonne à imputer.
        strategie : {"moyenne","mediane","mode","mean","median"}
            Stratégie d'imputation.
        fallback : Any | None, default None
            Valeur de repli si la statistique est indisponible (colonne entièrement NaN).
        verbose : bool, default False
            Si True, affiche la valeur utilisée pour l’imputation.

        Retour
        ------
        pd.DataFrame
            Colonne imputée si NaN existants, sinon renvoie la colonne originale avec un message.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas.DataFrame.")

        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' est absente du DataFrame.")

        s = df[colonne]

       
        if s.isna().sum() == 0:
            if verbose:
                print(f" Colonne '{colonne}' ne contient aucun NaN → aucune imputation nécessaire.")
            else:
                print(f" Colonne '{colonne}' ne contient aucun NaN → aucune imputation nécessaire.")
            return s 

        strat = strategie.lower()

        if strat in ("moyenne", "mean", "mediane", "median"):
            if not pd.api.types.is_numeric_dtype(s):
                raise TypeError(
                    f"La stratégie '{strat}' requiert une colonne numérique. "
                    f"Colonne '{colonne}' est de type {s.dtype}."
                )

       
        if strat in ("moyenne", "mean"):
            val = s.mean()
        elif strat in ("mediane", "median"):
            val = s.median()
        elif strat == "mode":
            m = s.mode(dropna=True)
            val = m.iat[0] if not m.empty else np.nan
        else:
            raise ValueError("Stratégie invalide : choisir 'moyenne', 'mediane' ou 'mode'.")

       
        out_col = s.fillna(val)
        if pd.isna(val) and fallback is not None:
            out_col = out_col.fillna(fallback)
            val = fallback
            out_col_df = out_col.to_frame()

        if verbose:
            print(f" Imputation appliquée sur '{colonne}' avec la valeur : {val}")

        return out_col_df

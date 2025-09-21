

import pandas as pd
import numpy as np
from typing import Literal


class GestionOutliers:
    Strategy = Literal["remove", "winsorize", "median", "mean", "log", "flag"]

    @staticmethod

    def gerer_outliers(
        df: pd.DataFrame,
        colonne: str,
        strategie: Strategy = "remove",
        *,
        inplace: bool = False,
        seuil: float = 1.5,
    ) -> pd.DataFrame:
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas.DataFrame.")
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' est absente du DataFrame.")
        if not np.issubdtype(df[colonne].dtype, np.number):
            raise TypeError(f"La colonne '{colonne}' doit être numérique.")

       
        if inplace:
            df_out = df
        else:
            df_out = df.copy()

       
        Q1 = df_out[colonne].quantile(0.25)
        Q3 = df_out[colonne].quantile(0.75)
        IQR = Q3 - Q1
        borne_inf = Q1 - seuil * IQR
        borne_sup = Q3 + seuil * IQR

       
        is_outlier = (df_out[colonne] < borne_inf) | (df_out[colonne] > borne_sup)
        n_outliers = int(is_outlier.sum())

        if strategie == "remove":
            if inplace:
                if n_outliers > 0:
                    
                    indices = df_out.index[is_outlier]
                    df.drop(index=indices, inplace=True)
                    print(f"{colonne}: outliers supprimés (n={n_outliers}).")
                else:
                    print(f"{colonne}: aucun outlier à supprimer.")
                return df  
            else:
                df_filtered = df_out.loc[~is_outlier].copy()
                print(f"{colonne}: outliers supprimés (n={n_outliers}).")
                return df_filtered

        elif strategie == "winsorize":
            df_out[colonne] = np.where(
                df_out[colonne] > borne_sup,
                borne_sup,
                np.where(df_out[colonne] < borne_inf, borne_inf, df_out[colonne]),
            )
            print(f"{colonne}: valeurs extrêmes winsorisées (n={n_outliers}).")
            return df_out

        elif strategie == "median":
            median = df_out[colonne].median()
            df_out[colonne] = np.where(is_outlier, median, df_out[colonne])
            print(f"{colonne}: outliers remplacés par la médiane (n={n_outliers}).")
            return df_out

        elif strategie == "mean":
            mean = df_out[colonne].mean()
            df_out[colonne] = np.where(is_outlier, mean, df_out[colonne])
            print(f" {colonne}: outliers remplacés par la moyenne (n={n_outliers}).")
            return df_out

        elif strategie == "log":
           
            df_out[colonne] = np.log1p(df_out[colonne].clip(lower=0))
            print(f"{colonne}: transformation log appliquée.")
            return df_out

        elif strategie == "flag":
            flag_col = f"{colonne}_outlier_flag"
            df_out[flag_col] = is_outlier.astype(int)
            print(f"{colonne}: indicateur binaire '{flag_col}' ajouté (n={n_outliers}).")
            return df_out

        else:
            raise ValueError("Stratégie invalide. Choisir: remove, winsorize, median, mean, log, flag.")

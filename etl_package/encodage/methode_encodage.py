
import pandas as pd
from typing import Literal, Optional

class EncodeurCategoriel:
    """
    Classe permettant d'encoder une colonne catégorielle
    avec différentes stratégies : one-hot, ordinal ou fréquence.
    
    """

    Strategy = Literal["onehot", "ordinal", "frequence"]

    @staticmethod

    def encoder_colonne(
        df: pd.DataFrame,
        colonne: str,
        strategie: Strategy = "onehot",
        *,
        mapping: Optional[dict] = None,
        prefix: Optional[str] = None,
        inplace: bool = False,
    ) -> pd.DataFrame:
        """
        Encode une colonne catégorielle selon la stratégie choisie.

        Paramètres
        ----------
        df : pd.DataFrame
            Le DataFrame contenant la colonne à encoder.
        colonne : str
            Le nom de la colonne à encoder.
        strategie : {"onehot", "ordinal", "frequence"}, default="onehot"
            Stratégie d’encodage.
        mapping : dict, optionnel
            Mapping {valeur: entier} requis si `strategie="ordinal"`.
        prefix : str, optionnel
            Préfixe pour les colonnes générées en one-hot encoding.
        inplace : bool, default=False
            Si True, modifie `df` directement. Sinon, retourne une copie.

        Retour
        ------
        pd.DataFrame
            DataFrame avec la colonne encodée.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas.DataFrame.")
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' est absente du DataFrame.")

        if inplace:
            df_out = df
        else:
            df_out = df.copy()

        if strategie == "onehot":
            prefix = prefix or colonne
            dummies = pd.get_dummies(df_out[colonne], prefix=prefix, dummy_na=False)
            df_out = pd.concat([df_out.drop(columns=[colonne]), dummies], axis=1)
            print(f"Colonne '{colonne}' encodée en one-hot ({dummies.shape[1]} colonnes).")

        elif strategie == "ordinal":
            if mapping is None:
                raise ValueError("Un mapping {valeur: entier} est requis pour l'encodage ordinal.")
            df_out[colonne] = df_out[colonne].map(mapping)
            print(f"Colonne '{colonne}' encodée en ordinal avec le mapping fourni.")

        elif strategie == "frequence":
            freq_map = df_out[colonne].value_counts(normalize=True).to_dict()
            df_out[colonne] = df_out[colonne].map(freq_map)
            print(f"Colonne '{colonne}' encodée par fréquence.")

        else:
            raise ValueError("Stratégie invalide : choisir 'onehot', 'ordinal' ou 'frequence'.")

        return df_out

import pandas as pd
from typing import Union, Dict

class RemplacementColonne:
    """
    Classe permettant de remplacer des valeurs ou sous-chaînes
    dans une colonne d'un DataFrame, avec option de division par 100.
    """

    @staticmethod
    def remplacer_valeurs(
        df: pd.DataFrame,
        colonne: str,
        remplacement: Union[Dict[str, str], tuple, list],
        *,
        inplace: bool = False,
        divide: bool = True,
    ) -> pd.DataFrame:
        """
        Remplace des valeurs ou sous-chaînes dans une colonne,
        puis optionnellement divise les valeurs par 100.

        Paramètres
        ----------
        df : pd.DataFrame
            Le DataFrame contenant la colonne.
        colonne : str
            Nom de la colonne à modifier.
        remplacement : dict ou tuple ou list
            - Si dict : mapping {ancien: nouveau}.
            - Si tuple/list de 2 éléments : (ancien, nouveau).
        inplace : bool, default=False
            Si True, modifie directement df. Sinon, retourne une copie.
        divide : bool, default=True
            Si True, divise les valeurs de la colonne par 100.

        Retour
        ------
        pd.DataFrame
            DataFrame avec les valeurs remplacées (et divisées par 100 si demandé).
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas.DataFrame.")
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' est absente du DataFrame.")

        df_out = df if inplace else df.copy()

       
        if isinstance(remplacement, (tuple, list)) and len(remplacement) == 2:
            remplacement = {remplacement[0]: remplacement[1]}

        if not isinstance(remplacement, dict):
            raise ValueError("`remplacement` doit être un dict ou un tuple/list de 2 éléments.")

        try:
           
            df_out[colonne] = df_out[colonne].astype(str).replace(remplacement, regex=True)

            
            df_out[colonne] = pd.to_numeric(df_out[colonne], errors="coerce")

            if divide:
                df_out[colonne] = df_out[colonne] / 100
                print(f" Remplacement effectué et colonne '{colonne}' divisée par 100.")
            else:
                print(f" Remplacement effectué dans la colonne '{colonne}' (sans division).")
        except Exception as e:
            raise ValueError(f"Erreur lors du traitement de '{colonne}' : {e}")

        return df_out

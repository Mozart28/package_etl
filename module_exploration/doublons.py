import pandas as pd

class ValeurDouble:
    """
    Cette classe permet de calculer le nombre de doublons dans un DataFrame.



    """

    @staticmethod
    def calcul_valeur_double(df: pd.DataFrame, return_rows: bool = False, keep: str = 'first'):
        
        """
        Cette fonction permet de détecter les doublons dans un dataframe pandas
        et retourner le nombre de doublons.
            -------------
       Paramètres :
         ------------ df : pd.DataFrame La base de données à étudier.
         return_rows : bool, optionnel 
         Si True, retourne les lignes dupliquées au lieu du nombre. 
         keep : str, optionnel Paramètre pour df.duplicated() : 
         'first', 'last' ou False Retour :
         -------- int ou pd.DataFrame 
         - Si return_rows=False : nombre de doublons ou 0 si aucun. 
         - Si return_rows=True : DataFrame contenant uniquement les lignes en double (vide si aucune valeur dupliquée).
        
        """
        try:
            if not isinstance(df, pd.DataFrame):
                raise TypeError("df doit être un pandas DataFrame")

            if df.empty:
                if return_rows:
                    print("Aucune ligne à retourner, DataFrame vide.")
                    return pd.DataFrame()
                else:
                    print("La DataFrame est vide.")
                    return 0

            duplicates_mask = df.duplicated(keep=keep)
            n_duplicates = int(duplicates_mask.sum())

            if n_duplicates == 0:
                if return_rows:
                    print("Pas de lignes à retourner, aucune valeur dupliquée.")
                else:
                    print("Il n'y a pas de valeurs doublons dans la DataFrame.")
                return
            else:
                if return_rows:
                    return df[duplicates_mask]
                else:
                    return n_duplicates

        except Exception as e:

            print(f" Une erreur est survenue : {e}")

            return

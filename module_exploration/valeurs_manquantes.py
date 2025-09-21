
import pandas as pd

class ValeurManquante:
    """
    cette classe permet de calculer le nbre de valeurs manquantes.
    """

    @staticmethod
    def calcul_valeur_manquante(df:pd.DataFrame):
        """
        Cette fonction calcule le nbre de valeurs manquantes
        Arguments
        ----------
        df:(pd.DataFrame), la base de données de l'étude

        return:
        res: (int), le nbre de valeurs manquantes.
       
       
        """
        if not isinstance(df,pd.DataFrame):
            raise ValueError("df doit etre un dataframe pandas")
        
        if df.empty:
            print("La dataframe spécifiée est nulle")
            return pd.DataFrame()
        
        res = df.isnull().sum()


        return res
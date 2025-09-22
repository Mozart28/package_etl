import pandas as pd

class ValeurManquante:
    """
    Classe pour calculer les valeurs manquantes dans un DataFrame.
    """

    @staticmethod
    def calcul_valeur_manquante(df: pd.DataFrame, detail: bool = False):
        """
        Calcule le nombre de valeurs manquantes.

        Paramètres
        ----------
        df : pd.DataFrame
            Jeu de données.
        detail : bool, default False
            - False : renvoie le total des valeurs manquantes.
            - True  : renvoie un DataFrame avec le détail par colonne.

        Retour
        ------
        int | pd.DataFrame
            Résultat selon le paramètre `detail`.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df doit être un DataFrame pandas")

        if df.empty:
            print("Le DataFrame spécifié est vide")
            return pd.DataFrame()

        if detail:
            res = df.isnull().sum().reset_index()
            res.columns = ["colonne", "nbre_valeurs_manquantes"]
            return res[res["nbre_valeurs_manquantes"] > 0]

        total = int(df.isnull().sum().sum())
        if total == 0:
            print("Le DataFrame ne contient pas de valeurs manquantes")
        return total

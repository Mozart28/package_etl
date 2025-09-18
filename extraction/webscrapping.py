import requests
import pandas as pd
from bs4 import BeautifulSoup

class ExtractionData:
    """
    Cette classe permet d'extraire des données depuis un site web 
    à partir d'un webscrapping.
    """

    @staticmethod
    def extract_webscrapping(url: str, columns_to_extract: list = None, rename_columns: list = None) -> pd.DataFrame:
        """
        Extrait des données d'un site web et retourne un DataFrame pandas.
        
        ----------
        Paramètres :
        url : str
            L'URL du site sur lequel l'extraction va être faite.
        columns_to_extract : list (optionnel)
            Liste des classes HTML à extraire (ex: ["Company", "Rating"]).
            Si None → toutes les colonnes disponibles seront extraites.
        rename_columns : list (optionnel)
            Liste des nouveaux noms de colonnes pour le DataFrame.
            Doit avoir la même taille que columns_to_extract.
        
        Retour :
        pandas.DataFrame
        """
        try:
            # Requête HTTP
            pageweb = requests.get(url, timeout=10)
            pageweb.raise_for_status()
            
            # Parsing HTML
            soup = BeautifulSoup(pageweb.content, "html.parser")

            # Trouver toutes les colonnes disponibles
            available_columns = [tag["class"][0] for tag in soup.find_all(attrs={"class": True})]
            available_columns = list(dict.fromkeys(available_columns))  # unique + garder l'ordre

            # Si aucune colonne spécifiée, prendre toutes
            if columns_to_extract is None:
                columns_to_extract = available_columns

            # Extraction des données
            data = {}
            for col in columns_to_extract:
                tags = soup.find_all(attrs={"class": col})
                values = [tag.get_text(strip=True) for tag in tags[1:]]  # ignorer en-tête
                data[col] = values

            # Conversion en DataFrame
            df = pd.DataFrame(data)

            # Renommer les colonnes si demandé
            if rename_columns and len(rename_columns) == len(df.columns):
                df.columns = rename_columns

            # Nettoyage spécifique : convertir CocoaPercent si présent
            if "CocoaPercent" in df.columns:
                df["CocoaPercent"] = df["CocoaPercent"].str.replace("%", "").astype(float)

            return df

        except Exception as e:
            print(f"❌ Erreur lors de l'extraction : {e}")
            return pd.DataFrame(columns=columns_to_extract if columns_to_extract else [])

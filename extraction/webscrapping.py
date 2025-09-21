import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

class ExtractionData:
    """
    Classe pour extraire des données depuis un site web via webscraping.
    Supporte les tableaux HTML ou l'extraction par classes CSS.
    Les entêtes sont automatiquement nettoyées.
    """

    @staticmethod
    def _nettoyer_colonnes(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les noms de colonnes : supprime \n, espaces multiples et trim."""
        new_cols = []
        for col in df.columns:
            col = col.replace("\n", " ")          # remplacer les sauts de ligne
            col = re.sub(r"\s+", " ", col)       # réduire les espaces multiples
            col = col.strip()                     # supprimer espaces début/fin
            new_cols.append(col)
        df.columns = new_cols
        return df

    @staticmethod
    def extract_webscrapping(url: str, columns_to_extract: list = None, rename_columns: list = None) -> pd.DataFrame:
        try:
            pageweb = requests.get(url, timeout=10)
            pageweb.raise_for_status()
            soup = BeautifulSoup(pageweb.content, "html.parser")

            # ✅ Mode tableau HTML
            if columns_to_extract is None:
                tables = soup.find_all("table")
                if not tables or len(tables) < 2:
                    raise ValueError("Impossible de trouver le tableau de données.")

                table = tables[1]  # prendre le 2ème tableau

                all_rows = table.find_all("tr")
                # Première ligne = en-têtes
                headers = [td.get_text(" ", strip=True) for td in all_rows[0].find_all("td")]

                # Lignes suivantes = données
                rows = []
                for tr in all_rows[1:]:
                    cells = [td.get_text(" ",strip=True) for td in tr.find_all("td")]
                    if cells:
                        rows.append(cells)

                df = pd.DataFrame(rows, columns=headers)
                #df = ExtractionData._nettoyer_colonnes(df)  # nettoyage automatique
                return df

            # ✅ Mode extraction par classes CSS
            data = {}
            for col in columns_to_extract:
                tags = soup.find_all(attrs={"class": col})
                values = [tag.get_text(strip=True) for tag in tags[1:]]
                data[col] = values

            df = pd.DataFrame(data)
            if rename_columns and len(rename_columns) == len(df.columns):
                df.columns = rename_columns

            #df = ExtractionData._nettoyer_colonnes(df)  # nettoyage automatique
            return df

        except Exception as e:
            print(f"Erreur lors de l'extraction : {e}")
            return pd.DataFrame(columns=columns_to_extract if columns_to_extract else [])

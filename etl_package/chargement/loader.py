

import pandas as pd
from typing import Optional, Union
import os





class Loader:
    """
    Classe pour charger un DataFrame pandas vers différents supports :
    - CSV
    - Excel
    - Base SQL (via SQLAlchemy engine)
    - MongoDB (via pymongo collection)

    Chaque méthode est statique et peut être appelée sans instancier la classe.
    """

    @staticmethod

    def vers_csv(
        df: pd.DataFrame,
        chemin: str,
        sep: str = ",",
        index: bool = False,
        mode: str = "w",
        verbose: bool = True
    ) -> None:
        """
        Sauvegarde un DataFrame au format CSV.

        Paramètres
        ----------
        df : pd.DataFrame
            DataFrame à sauvegarder.
        chemin : str
            Chemin complet du fichier CSV de sortie.
        sep : str, default=','
            Séparateur de colonnes (ex: ',', ';', '\t').
        index : bool, default=False
            Si True, inclut l’index du DataFrame dans le fichier.
        mode : str, default='w'
            Mode d’écriture : 'w' pour écraser, 'a' pour ajouter.
        verbose : bool, default=True
            Si True, affiche un message de confirmation.
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas DataFrame")
        try:
            df.to_csv(chemin, sep=sep, index=index, mode=mode)
            if verbose:
                print(f"DataFrame sauvegardé en CSV : {chemin}")
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture CSV : {e}")

    @staticmethod

    def vers_excel(
        df: pd.DataFrame,
        chemin: str,
        sheet_name: str = "Sheet1",
        index: bool = False,
        verbose: bool = True
    ) -> None:
        """
        Sauvegarde un DataFrame au format Excel.

        Paramètres
        ----------
        df : pd.DataFrame
            DataFrame à sauvegarder.
        chemin : str
            Chemin complet du fichier Excel de sortie.
        sheet_name : str, default='Sheet1'
            Nom de la feuille Excel.
        index : bool, default=False
            Si True, inclut l’index du DataFrame dans le fichier.
        verbose : bool, default=True
            Si True, affiche un message de confirmation.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas DataFrame")
        try:
            df.to_excel(chemin, sheet_name=sheet_name, index=index)
            if verbose:
                print(f"DataFrame sauvegardé en Excel : {chemin}")
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture Excel : {e}")

    @staticmethod

    def vers_sql(
        df: pd.DataFrame,
        table_name: str,
        engine,
        if_exists: str = "replace",
        index: bool = False,
        verbose: bool = True
    ) -> None:
        """
        Sauvegarde un DataFrame dans une base SQL via un SQLAlchemy engine.

        Paramètres
        ----------
        df : pd.DataFrame
            DataFrame à sauvegarder.
        table_name : str
            Nom de la table SQL dans laquelle écrire les données.
        engine : SQLAlchemy engine
            Objet SQLAlchemy créé via `create_engine`.
        if_exists : str, default='replace'
            Comportement si la table existe déjà :
            - 'fail' : lève une erreur
            - 'replace' : supprime la table existante et crée la nouvelle
            - 'append' : ajoute les données à la table existante
        index : bool, default=False
            Si True, inclut l’index du DataFrame dans la table.
        verbose : bool, default=True
            Si True, affiche un message de confirmation.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas DataFrame")
        try:
            df.to_sql(table_name, engine, if_exists=if_exists, index=index)
            if verbose:
                print(f"DataFrame chargé dans la table SQL : {table_name}")
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture SQL : {e}")

    @staticmethod
    
    def vers_mongodb(
        df: pd.DataFrame,
        collection,
        verbose: bool = True
    ) -> None:
        """
        Sauvegarde un DataFrame dans une collection MongoDB.

        Paramètres
        ----------
        df : pd.DataFrame
            DataFrame à sauvegarder.
        collection : pymongo collection
            Objet collection créé via `pymongo.MongoClient()['nom_db']['nom_collection']`.
        verbose : bool, default=True
            Si True, affiche un message de confirmation.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("`df` doit être un pandas DataFrame")
        try:
            records = df.to_dict(orient="records")
            collection.insert_many(records)
            if verbose:
                print(f"DataFrame inséré dans MongoDB (n={len(df)})")
        except Exception as e:
            raise IOError(f"Erreur lors de l'écriture MongoDB : {e}")

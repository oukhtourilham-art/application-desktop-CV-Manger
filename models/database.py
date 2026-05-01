#C'est le fichier qui fait le pont entre Python et ta base de données SQLite. Il lit le schema.sql et crée la base automatiquement au premier lancement.
import sqlite3
import os
from config import DATABASE_PATH, BASE_DIR

class Database:
    _instance = None   # Pattern Singleton

    def __init__(self):
        self.db_path = DATABASE_PATH
        self.connection = None
        self._initialiser()

    @classmethod
    def get_instance(cls):
        """Retourne toujours la meme instance (Singleton) """
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance
    
    def _intialiser(self):
        """Crée la base de donnée si elle n'existe pas encore"""
        #Créer le dossier data/ si nécessaire
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        #Lire et exécuter le schema.sql
        schema_path = os.path.join(BASE_DIR, "data", "schema.sql")
        with self.connecter() as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescipt(f.read())

    def connecter(self):
        """Ouvre et retourne une connexion SQLite"""
        return sqlite3.connect(self.db_path)
    
    def executer(self, query, params=()):
        """Exécute une requete INSERT / UPDATE / DELETE"""
        with self.connecter() as conn:
            curseur = conn.cursor()
            curseur.execute(query, params)
            conn.commit()
            return curseur.lastrowid
        
    def recuperer_un(self, query, params=()):
        """Retourne une seule ligne"""
        with self.connecter() as conn:
            conn.row_factory = sqlite3.Row
            curseur = conn.cursor()
            curseur.execute(query, params)
            return curseur.fetchone()
        
    def recuperer_tous(self, query, params=()):
        """Returne toutes les lignes"""
        with self.connecter() as conn:
            conn.row_factory = sqlite3.Row
            curseur = conn.cursor()
            curseur.execute(query, params)
            return curseur.fetchall()
        
# Explication des concepts importants
# Le pattern Singleton (get_instance)
# Garantit qu'il n'y a qu'une seule connexion à la base dans toute l'app
# sqlite3.Row
# Permet d'accéder aux colonnes par leur nom au lieu de leur index
# Exemple : row["username"] au lieu de row[1] → code plus lisible
# with self.connecter() as conn
# Le with ferme la connexion automatiquement après chaque opération .Évite les fuites de mémoire
# executescript()
# Exécute plusieurs requêtes SQL d'un coup (tout le contenu de schema.sql)
#
#
#

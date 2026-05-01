import os  # os  bibliothèque intégrée à Python, qui permet à mon programme de communiquer avec le système d'exploitation

#Répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Base de données
DATABASE_PATH = os.path.join(BASE_DIR, "data", "cv_manager.bd")

#Dossier pour stocker les CV uploadés
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")

#Parametres de l'application
APP_NAME = "CV Manger"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

#Domaines de compétences reconnus
SkILL_DOMAINS = [
    "IT",
    "Finance",
    "Marketing",
    "Mangement",
    "Langues",
    "Autre"
]

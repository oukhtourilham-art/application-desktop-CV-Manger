import os
import shutil
import fitz #PyMuPDF
from config import UPLOAD_FOLDER

class FileService:

    @staticmethod
    def sauvegarder_fichier(filepath_source, user_id):
        """
        Copier le fichier CV dans le dossier uploads de l'app
        Returne le neuveau chemin et le nom du fichier 
        """
        #Créer un sous-dossier par utilisateur
        dossier_user = os.path.join(UPLOAD_FOLDER, str(user_id))
        os.makedirs(dossier_user, exist_ok=True)

        # Garder le nom original du fichier
        nom_fichier = os.path.basename(filepath_source)
        chemin_destination = os.path.join(dossier_user, nom_fichier)

        #Copier le fichier
        shutil.copy2(filepath_source, nom_fichier)

        return chemin_destination, nom_fichier
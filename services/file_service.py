#ce fichier file_service.py c'est le service qui lit 
#les fichiers CV uploadés par les étudiant et en extarait
#le texte brut . c'est le première étape avant l'analyse NLP

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
    
    @staticmethod
    def extraire_texte(filepath):
        """
        Extrait le texte brut d'un fichier PDF ou TXT
        Retourne une chaie de caractères
        """
        extension = os.path.splitext(filepath)[1].lower()

        if extension == ".pdf":
            return FileService._lire_pdf(filepath)
        elif extension == ".txt":
            return FileService._lire_txt(filepath)
        else:
            raise ValueError(f"Format non supporté : {extension}")
        
    @staticmethod
    def _lire_pdf(filepath):
        """Extraite le texte d'un fichier PDF page par page"""
        texte = ""
        try:
            document = fitz.open(filepath)
            for page in document:
                texte += page.get_text()
            document.close()
        except Exception as e:
            raise RuntimeError(f"Erreur lecture EDF : {e}")
        return texte.strip()
    
    @staticmethod
    def _lire_txt(filepath):
        """Lit un fichier texte brut"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except UnicodeDecodeError:
            #si UTF-8 échoue, essayer latin-1
            with open(filepath, "r", encoding="latin-1") as f:
                return f.read().strip()

    @staticmethod
    def est_valide(filepath):
        """
        Vérifier si le fichier est valide avant de le traiter
        Returne (True, "") ou (False, "massage d'erreur")
        """    
        # pour vérifier si le fichier existe
        if not os.path.exists(filepath):
            return False, "Le fichier n'existe pas"
        
        #pour verifier l'extension
        extension = os.path.splitext(filepath)[1].lower()
        if extension not in [".pdf", ".txt"]:
            return False, "Format non supporté. Utilizer PDF ou TXT."

        #pour vérifier la taille (max 5 Mo)
        taille = os.path.getsize(filepath)
        if taille > 5 * 1024 * 1024:
            return False, "Fichier trop volumineux (max 5 Mo)"
        
        # pour vérifier que le fichier n'est pas vide
        if taille == 0:
            return False, "Le fichier est vide"
        
        return True, ""
    
#Explication des points importants
#sauvegarder_fichier() : Crée un dossier séparé pour chaque utilisateur : uploads/1/, uploads/2/... 
#Evite les conflits si deux étudiants ont un CV avec le meme nom
#extraire_texte() : C'est le point d'entrée principal , il détecte automatiquement le format (PDF ou TXT) et appelle la bonne méthode
#Principe de délégation : une fonction centrale qui redirige vers les spécialistes
#_lire_pdf() : Utilise PyMuPDF (fitz) pour lire page par page
#Le _ au début du nom signifie que c'est une méthode privée 
#_lire_txt() avec double encodage : 
#D'abord essaie UTF-8 (encodage moderne)
#Si ça échoue, essaie latin-1 (encodage ancien, fréquent sur Windows)
#Évite les erreurs sur les CV avec des caractères spéciaux (é, à, ç...)
#est_valide() :Vérifie 4 choses avant de traiter : existence, extension, taille, contenu
#Retourne un tuple (booléen, message) - très pratique pour afficher le bon message d'erreur dans l'interface

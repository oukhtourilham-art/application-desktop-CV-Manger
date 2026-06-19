from models.cv import CV
from models.skill import Skill
from services.file_service import FileService
from services.nlp_service import NLPService
from services.score_service import ScoreService
from controllers.auth_controller import AuthController

class CVController:

    @staticmethod
    def uploader_cv(filepath_source):
        """
        Processus complet d'upload et d'analyse d'un CV.
        Retourne (True, details) ou (False, message_erreur)
        """
        #Etape 1 : Vérifion le fichier
        valide, message = FileService.est_valide(filepath_source)
        if not valide:
            return False, message
        
        #Etape 2 : Récupérer l'utilisateur connecté
        user = AuthController.get_utilisateur()
        if user is None:
            return False, "Aucun utilisateur connecté."
        
        #Etape 3 :Sauvegarder le fichier 
        chemin, nom_fichier = FileService.sauvegarder_fichier(filepath_source, user.id)
        
        #Etape 4: Enregister le CV en base
        cv_id = CV.creer(user.id, nom_fichier, chemin)

        #Etape 5 : Extraire le texte
        texte = FileService.extraire_texte(chemin)
        if not texte:
            return False, "Impossible d'extraire le texte du fichier."
        
        #Etape 6: Analyse avec NLP
        competences = NLPService.analyser(texte)

        #Etape 7: Sauvegarder les compétences
        Skill.creer_plusieurs(cv_id, competences)

        #Etape 8: Calculer et sauvegarder le score 
        details = ScoreService.calculer_details(competences)
        CV.mettre_a_jour_score(cv_id, details["score"])

        return True , {
            "cv_id"    : cv_id,
            "nom_fichier"  : nom_fichier,
            "competences"  : competences,
            "details"    : details
        }
    
    @staticmethod
    def get_cvs_etudiant():
        """Retourne tous les CV de l'étudiant connecté"""
        user = AuthController.get_utilisateur()
        if user is None:
            return []
        
        return CV.trouver_par_utilisateur(user.id)
    
    @staticmethod
    def get_details_cv(cv_id):
        """
        Retourne le CV + ses compétences + détails du score.
        """
        cv = CV.trouver_par_id(cv_id)
        if cv is None:
            return None
        
        competences = Skill.trouver_par_cv(cv_id)
        groupes = NLPService.grouper_par_domaine(
            [{"name": s.name, "domain": s.domain} for s in competences]
        )
        niveau = ScoreService.get_niveau(cv.score)
        couleur = ScoreService.get_couleur(cv.score)

        return {
            "cv"   : cv,
            "competences"   : competences,
            "groupes"   : groupes,
            "niveau"    : niveau,
            "couleur"   : couleur
        }
         
        
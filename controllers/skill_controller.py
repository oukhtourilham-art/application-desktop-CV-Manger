from models.skill import Skill
from services.nlp_service import NLPService

class SkillController:

    @staticmethod
    def get_skills_par_cv(cv_id):
        """Retourne toutes les compétences d'un CV"""
        return Skill.trouver_par_cv(cv_id)
    
    @staticmethod
    def get_skills_groupes(cv_id):
        """
        Retourne les compétences regroupées par domaine.
        Utile pour l'affichage dans l'interface.
        """
        skills = Skill.trouver_par_cv(cv_id)
        return NLPService.grouper_par_domaine(
            [{"name": s.name, "domain": s.domain} for s in skills]
        )
    
    @staticmethod
    def get_domaines_disponibles():
        """
        Retourne les domaines qui ont au moins un CV.
        Utilisé pour peupler le filtre du dashboard RH.
        """
        return Skill.domaines_disponibles()
    
    @staticmethod
    def reanalyer_cv(cv_id, texte):
        """
        Ré-analyse un CV existant (supprime et recrée les compétences).
        Utile si le dictionnaire NLP a été enrichi.
        """
        from models.cv import CV
        from services.score_service import ScoreService

        #Supprimer les anciennes compétences
        Skill.supprimer_par_cv(cv_id)

        #Relancer l'analyse
        competences = NLPService.analyser(texte)
        Skill.creer_plusieurs(cv_id, competences)

        #Recalculer le score
        nouveau_score = ScoreService.calculer(competences)
        CV.mettre_a_jour_score(cv_id, nouveau_score)

        return competences, nouveau_score
    
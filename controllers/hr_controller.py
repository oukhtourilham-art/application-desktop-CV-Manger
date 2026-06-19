from models.cv import CV
from models.user import User
from models.skill import Skill
from services.score_service import ScoreService

class HRController:

    @staticmethod
    def get_tous_les_cvs():
        cvs = CV.tous()
        resultats = []
        for cv in cvs:
            user   = User.trouver_par_id(cv.user_id)
            skills = Skill.trouver_par_cv(cv.id)
            resultats.append({
                "cv"       : cv,
                "candidat" : user.username if user else "Inconnu",
                "nb_skills": len(skills),
                "niveau"   : ScoreService.get_niveau(cv.score),
                "couleur"  : ScoreService.get_couleur(cv.score),
            })
        return resultats

    @staticmethod
    def filtrer_par_domaine(domaine):
        from models.database import Database
        db = Database.get_instance()
        rows = db.recuperer_tous("""
            SELECT DISTINCT cvs.*
            FROM cvs
            JOIN skills ON skills.cv_id = cvs.id
            WHERE skills.domain = ?
            ORDER BY cvs.score DESC
        """, (domaine,))

        resultats = []
        for row in rows:
            cv    = CV(row["id"], row["user_id"], row["filename"],
                       row["filepath"], row["score"], row["uploaded_at"])
            user  = User.trouver_par_id(cv.user_id)
            skills = Skill.trouver_par_cv(cv.id)
            resultats.append({
                "cv"       : cv,
                "candidat" : user.username if user else "Inconnu",
                "nb_skills": len(skills),
                "niveau"   : ScoreService.get_niveau(cv.score),
                "couleur"  : ScoreService.get_couleur(cv.score),
            })
        return resultats

    @staticmethod
    def get_statistiques():
        cvs = CV.tous()
        if not cvs:
            return None

        scores    = [cv.score for cv in cvs]
        candidats = [User.trouver_par_id(cv.user_id) for cv in cvs]
        noms      = [u.username if u else "?" for u in candidats]

        niveaux = {"Excellent": 0, "Bon": 0, "Moyen": 0, "Faible": 0}
        for score in scores:
            niveaux[ScoreService.get_niveau(score)] += 1

        return {
            "scores"        : scores,
            "noms"          : noms,
            "niveaux"       : niveaux,
            "score_moyen"   : round(sum(scores) / len(scores), 2),
            "meilleur_score": max(scores),
            "nb_candidats"  : len(cvs),
        }

    @staticmethod
    def get_domaines_disponibles():       
        return Skill.domaines_disponibles()
# CV :  C'est la classe qui représente un CV dans l'application
# Elle gère toutes les opérations liées aux CV : enregistrer,
# récupérer, mettre à jour le score.

from models.database import Database

class CV:
    def __init__(self, id, user_id, filename, filepath, score=0, uploaded_at=None):
        self.id          = id
        self.user_id     = user_id
        self.filename    = filename
        self.filepath    = filepath
        self.score       = score        
        self.uploaded_at = uploaded_at

    #  Méthodes statiques (opérations sur la BD)
    @staticmethod
    def creer(user_id, filename, filepath):
        """Enregister un nouveau CV dans la base"""
        db = Database.get_instance()
        cv_id = db.executer(
            "INSERT INTO cvs (user_id, filename, filepath) VALUES (?, ?, ?)",
            (user_id, filename, filepath)
        )
        return cv_id
        
    @staticmethod
    def trouver_par_id(cv_id):
        """Retourne un CV par son ID"""
        db = Database.get_instance()
        row = db.recuperer_un(
            "SELECT * FROM cvs id = ?",
            (cv_id,)
        )
        if row:
            return CV(row["id"], row["user_id"], row["filename"], row["filepath"], row["score"], row["uploaded_at"])
        return None
    
    @staticmethod
    def trouver_par_utilisateur(user_id):
        """Retourne tous les CV d'un étudiant"""
        db = Database.get_instance()
        rows = db.recuperer_tous(
            "SELECT * FROM cvs WHERE user_id = ? ORDER BY uploaded_at DESC",
            (user_id,)
        )
        return [CV(r["id"], r["user_id"], r["filename"],
                   r["filepath"], r["score"], r["uploaded_at"]) for r in rows]
    
    @staticmethod
    def tous():
        """Retourne tous les CV (utilisé par RH)"""
        db = Database.get_instance()
        rows = db.recuperer_tous(
            "SELECT * FROM cvs ORDER BY score DESC"
        )
        return [CV(r["id"], r["user_id"], r["filename"],
                   r["filepath"], r["score"], r["uploaded_at"]) for r in rows]
    
    @staticmethod
    def mettre_a_jour_score(cv_id, score):
        """Met à jour le score d'un CV après analyse"""
        db = Database.get_instance()
        db.executer(
            "UPDATE cvs SET score = ? WHERE id = ?",
            (score, cv_id)
        )
        

    #  Méthodes utilitaires
    def get_skills(self):
        """Returne toutes les compétences de ce CV"""
        from models.skill import Skill
        return Skill.trouver_par_cv(self.id)
    
    def niveau_score(self):
        """Retourne une appréciation textuelle de score"""
        if self.score >= 80:
            return "Excellent"
        elif self.score >= 60:
            return "Bon"
        elif self.score >= 40:
            return "Faible"
        
    def __repr__(self):
        return f"CV(id={self.id}, fichier={self.filename}, score={self.score})"
    
#  Points importants
#  trouver_par_utilisateur() vs tous()
#  Un étudiant voit seulement ses propres CV
#  Un RH voit tous les CV, triés par score décroissant
#  C'est la gestion des rôles appliquée au niveau des données
#  mettre_a_jour_score()
#  Le score est calculé après l'analyse NLP
#  D'abord on enregistre le CV, ensuite on l'analyse, ensuite on met le score à jour
#  niveau_score()
#  Transforme un chiffre en texte lisible : 85 → "Excellent"
#  Très utile pour l'affichage dans l'interface RH
#  Import circulaire évité
#  L'import de Skill est fait à l'intérieur de la méthode get_skills()
#  Cela évite le problème où cv.py importe skill.py et skill.py importe cv.py
#

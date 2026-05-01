from models.database import Database

class Skill:
    def __init__(self, id, cv_id, name, domain):
        self.id      = id
        self.cv_id   = cv_id
        self.name    = name
        self.domain  = domain

    # Methode statique
    @staticmethod
    def creer(cv_id, name, domain):
        """Enregistre une compétence dans la base"""
        db = Database.get_instance()
        db.executer(
            "INSERT INTO skills (cv_id, name, domain) VALUES (?, ?, ?)",
            (cv_id, name, domain)
        )

    @staticmethod
    def creer_plusieurs(cv_id, liste_skills):
        """
        Enregister plusieurs compétence d'un coup
        liste_skills = [{"name": "python", "domain": "IT"},...]
        """
        for skill in liste_skills:
            Skill.creer(cv_id, skill["name"], skill["domain"])

    @staticmethod
    def trouver_par_cv(cv_id):
        """Retourne toutes les compétences d'un CV"""
        db = Database.get_instance()
        rows = db.recuperer_tous(
            "SELECT * FROM skills WHERE cv_id = ? ORDER BY domain",
            (cv_id,)
        )
        return [Skill(r["id"], r["cv_id"], r["name"], r["domain"]) for r in rows]
    
    @staticmethod
    def trouver_par_domaine(domain):
        """Retourne toutes les compétences d'un domaine donné"""
        db = Database.get_instance()
        rows = db.recuperer_tous(
            "SELECT * FROM skills WHERE domain = ?",
            (domain,)
        )
        return [Skill(r["id"], r["cv_id"], r["name"], r["domain"]) for r in rows]
    
    @staticmethod
    def domaines_disponibles():
        """Retourne la liste des domaines qui ont au moins une compétence"""
        db = Database.get_instance()
        rows = db.recuperer_tous(
            "SELECT DISTINCT domain FROM skills ORDER BY domain"
        )
        return [r["domain"] for r in rows]
    
    # Méthodes utilisateurs
    def __repr__(self):
        return f"Skill(name={self.name}, domain={self.domain})"
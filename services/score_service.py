from config import SkILL_DOMAINS

class ScoreService:
    # les parametres de calcul:
    POINT_PAR_COMPETENCE = 5  # chaque compétence rapporte 5 points
    BONUS_PAR_DOMAINE = 10    # bonnus si au moins 1 compétence par domaine
    SCORE_MAX = 100           # Score max est 100

    @classmethod
    def calculer(cls, competences):
        """
        Calcule le score d'un CV à partir de ses compétences.
        Entrée  : [{"name": "Python", "domain": "IT"}, ...]
        Sortie  : score (float entre 0 et 100)
        """
        if not competences:
            return 0.0
        
        # Etape 1 : Points de base (par compétnce)
        points_base = len(competences) * cls.POINT_PAR_COMPETENCE

        # Etape 2 : Bonus (par domaine couvert)
        domaines_couverts = set(comp["domain"] for comp in competences)
        bonus = len(domaines_couverts) * cls.BONUS_PAR_DOMAINE

        # Etape 3 : Total plafonné a 100
        score = points_base + bonus
        score = min(score, cls.SCORE_MAX) # ne dépasse jamais 100

        return round(float(score), 2)
    
    @classmethod
    def calculer_details(cls, competnces):
        """
        Retourne le score ET le détail du calcul.
        Utile pour afficher l'explication à l'étudiant.
        """
        if not competnces:
            return {
                "score": 0.0,
                "nb_competences": 0,
                "points_base": 0,
                "domaines_couverts": [],
                "nb_domaines": 0,
                "bonus": 0,
                "niveau": "Faible"
            }
        
        nb_competences = len(competnces)
        points_base = nb_competences * cls.POINT_PAR_COMPETENCE
        domaines_couverts = list(set(comp["domain"] for comp in competnces))
        nb_domaines = len(domaines_couverts)
        bonus = nb_domaines * cls.BONUS_PAR_DOMAINE
        score = min(points_base + bonus, cls.SCORE_MAX)

        return {
            "score"           : round(float(score), 2),
            "nb_competences"  : nb_competences,
            "points_base"     : points_base,
            "domaines_couverts": domaines_couverts,
            "nb_domaines"     : nb_domaines,
            "bonus"           : bonus,
            "niveau"          : cls.get_niveau(score)
        }
    
    @classmethod
    def get_niveau(cls, score):
        """Convertit un score numérique en niveau textuel"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Bon"
        elif score >= 40:
            return "Moyen"
        else:
            return "Faible"
        
    @classmethod
    def get_couleur(cls, score):
        """
        Retourne une couleur selon le niveau.
        Utile pour coloriser l'affichage dans l'interface.
        """
        if score >= 80:
            return "#27AE60" 
        elif score >= 60:
            return "#2E86C1"   
        elif score >= 40:
            return "#F39C12"   
        else:
            return "#E74C3C"
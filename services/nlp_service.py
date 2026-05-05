import spacy

#Dictionnaire des compétences classées par domaine 
COMPETENCES = {
    "IT": [
        "python", "java", "javascript", "c++", "c#", "php", "ruby", "swift",
        "sql", "mysql", "postgresql", "mongodb", "sqlite",
        "html", "css", "react", "angular", "vue", "django", "flask", "fastapi",
        "machine learning", "deep learning", "intelligence artificielle",
        "docker", "kubernetes", "linux", "git", "github", "api", "rest",
        "data science", "pandas", "numpy", "tensorflow", "pytorch",
        "réseau", "cybersécurité", "cloud", "aws", "azure",
    ],
    "Finance": [
        "comptabilité", "audit", "fiscalité", "budget", "trésorerie",
        "analyse financière", "bilan", "excel", "sap", "erp",
        "gestion financière", "contrôle de gestion", "reporting",
        "investissement", "finance", "banque", "assurance",
    ],
    "Marketing": [
        "marketing", "seo", "sea", "community management", "réseaux sociaux",
        "photoshop", "illustrator", "indesign", "adobe",
        "communication", "publicité", "brand", "crm", "salesforce",
        "rédaction", "copywriting", "stratégie digitale", "e-commerce",
    ],
    "Management": [
        "management", "leadership", "gestion de projet", "chef de projet",
        "agile", "scrum", "kanban", "prince2", "pmp",
        "ressources humaines", "recrutement", "formation",
        "négociation", "stratégie", "organisation", "planification",
    ],
    "Management": [
        "management", "leadership", "gestion de projet", "chef de projet",
        "agile", "scrum", "kanban", "prince2", "pmp",
        "ressources humaines", "recrutement", "formation",
        "négociation", "stratégie", "organisation", "planification",
    ],
    "Langues": [
        "anglais", "français", "arabe", "espagnol", "allemand",
        "italien", "chinois", "portugais",
        "toefl", "toeic", "ielts", "delf", "dalf",
        "bilingue", "trilingue", "traduction", "interprétation",
    ],
}

class NLPService:
    _modele = None # c'est un singleton pour le modéle spaCy

    @classmethod
    def _charger_modele(cls):
        """Charge le modèle spaCy une seule fois"""
        if cls._modele is None:
            try:
                cls._modele = spacy.load("fr_core_news_sm")
            except OSError:
                # Modèle français non trouvé, utiliser le modèle vide
                cls._modele = spacy.blank("fr")
        return cls._modele
    
    @classmethod
    def analyser(cls, texte):
        """
        Analyse le texte du CV et retourne une liste de compétences.
        Retourne : [{"name": "Python", "domain": "IT"}, ...]
        """
        if not texte or not texte.strip():
            return []
        
        nlp = cls._charger_modele()

        # Normaliser le texte (minuscules, nettoyage)
        doc = nlp(texte_normalise)

        competences_trouvees = []
        competences_vues = set() # pour Éviter les doublons

        # Methode 1 : rechercer directe dans le texte
        for domaine, liste in COMPETENCES.items():
            for competence in liste:
                if competence in texte_normalise:
                    cle = competence.lower()
                    if cle not in competences_vues:
                        competences_vues.add(cle)
                        competences_trouvees.append({
                            "name": competence.title(),
                            "domain": domaine
                        })

        # Methode 2 : Analuse par tokens spacy ()
        for token in doc:
            lemme = token.lemma_.lower()
            for domaine, liste in COMPETENCES.items():
                for competence in liste:
                    # Comparer le lemme avec chaque mot de la compétence
                    if lemme == competence and lemme not in competences_vues:
                        competences_vues.add(lemme)
                        competences_trouvees.append({
                            "name": competence.title(),
                            "domain": domaine
                        })
        return competences_trouvees
    
    @classmethod
    def grouper_par_domaine(cls, competences):
        """
        Regroupe une liste de compétences par domaine.
        Entrée  : [{"name": "Python", "domain": "IT"}, ...]
        Sortie  : {"IT": ["Python", "Sql"], "Finance": [...], ...}
        """
        groupes = {}
        for comp in competences:
            domaine = comp["domain"]
            if domaine not in groupes:
                groupes[domaine] = []
            groupes[domaine].append(comp["name"])
        return groupes
    
    @classmethod
    def domaines_detectes(cls, competences):
        """Retourne la liste des domaines présents dans les compétences"""
        return list(set(comp["domain"] for comp in competences))
        
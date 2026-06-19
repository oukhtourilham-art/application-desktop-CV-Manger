from models.user import User

class AuthController:
    _utilisateur_connecte = None #Session courante

    @classmethod
    def connecter(cls, username, password):
        """
        Vérifie les identifiants et ouvre la session.
        Retourne (True, user) ou (False, message_erreur)
        """
        if not username or not password:
            return False, "Veuillez remplir tous les champs."
        
        user = User.verifier_login(username, password)

        if user is None:
            return False, "Identifiant ou mot de passe incorrect."
        
        cls._utilisateur_connecte = user
        return True, user
    
    @classmethod
    def inscrire(cls, username, password, confirmation):
        """
        Crée un nouveau compte étudiant.
        Retourne (True, "") ou (False, message_erreur)
        """
        #Vérification
        if not username or not password:
            return False, "Veuillez remplir tous les champs."
        
        if password != confirmation:
            return False, "Les mot de passe ne correspondent pas."
        
        if len(password) < 6:
            return False, "Le mot de passe doit contenir au moins 6 caractères."
        
        if len(username) < 3:
            return False, "Le nom d'utilisateur doit contenir au moins 3 caractères."
        
        #Vérification si le nom d'utilisateur existe déja
        from models.database import Database
        db = Database.get_instance()
        existant = db.recuperer_un(
            "SELECT id FROM users WHERE username = ?", (username,)
        )
        if existant:
            return False, "Ce nom d'utilisateur est déjà pris."
        
        #Créer le compte (role étudiant)
        User.creer(username, password, "etudiant")
        return True, ""
    
    @classmethod
    def deconnecter(cls):
         """Ferme la session courante"""
         cls._utilisateur_connecte = None

    @classmethod
    def get_utilisateur(cls):
        """Retourne l'utilisateur actuellement connecté"""
        return cls._utilisateur_connecte
    
    @classmethod
    def est_connecte(cls):
        """Vérifier si une session est active"""
        return cls._utilisateur_connecte is not None
    
    @classmethod
    def est_rh(cls):
        """Vérifie si l'utilisateur connecté est RH"""
        return cls._utilisateur_connecte is not None and  cls._utilisateur_connecte.est_rh()
    
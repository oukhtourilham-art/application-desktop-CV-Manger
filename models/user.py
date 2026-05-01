import hashlib
from models.database import Database

class User:
    def __init__(self, id, username, role, created_at=None):
        self.id         = id
        self.username   = username
        self.role       = role
        self.created_at = created_at

        # Méthodes statiques (opérations sur la BD)
        @staticmethod
        def _hasher_mdp(password):
            """Transforme un mot de passe en hash sécurisé"""
            return hashlib.sha256(password.encode()).hexdigest()
        
        @staticmethod
        def creer(username, password, role):
            """Crée un nouvel utilisateur dans la base"""
            db = Database.get_instance()
            mdp_hach = User._hash_mdp(password)
            db.executer(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
                (username, mdp_hach, role)
            )

        @staticmethod
        def verifier_login(username, password):
          """
          Vérifier les identifications
          retourne un objet User si correct, None sinon
          """ 
          db = Database.get_instance()
          mdp_hash = User._hasher_mdp(password)
          row = db.recuperer_un(
              "SELECT * FROM users WHERE username = ? AND password = ?",
              (username, mdp_hash)
          ) 
          if row:
              return User(row["id"], row["username"], row["role"], row["created_at"])
          return None
        
        @staticmethod
        def trouver_par_id(user_id):
            """Retourne un User par son ID"""
            db = Database.get_instance()
            row = db.recuperer_un(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            )
            if row:
                return User(row["id"], row["username"], row["role"], row["created_at"])
            return None
        
        # Méthodes utilitaires
        def est_rh(self):
            """Retourne True si l'utilisateur est RH"""
            return self.role == "rh"
        
        def est_etudiant(self):
            """Returne True si l'utlisateur est étudiant"""
            return self.role == "etudiant"
        
        def __repr__(self):
            return f"User(id={self.id}, username={self.username}, role={self.role})"
        

# Explication des Points importants
# Le hashage SHA-256 (_hasher_mdp) : algorithme de securité de mot de passe 
# Le mot de passe n'est jamais stocké en clair dans la base
# "rh1234" devient quelque chose comme "a3f5c2..." — impossible à lire
# C'est une vraie bonne pratique de sécurité
# @staticmethod
# Ces méthodes n'ont pas besoin d'un objet User existant pour fonctionner
# On les appelle directement : User.verifier_login("admin", "1234")
# est_rh() / est_etudiant()
#  Des méthodes simples mais très utiles dans les controllers pour gérer les accès  
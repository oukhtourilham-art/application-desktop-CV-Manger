import hashlib
from models.database import Database

class User:
    def __init__(self, id, username, role, created_at=None):
        self.id         = id
        self.username   = username
        self.role       = role
        self.created_at = created_at

    @staticmethod
    def _hasher_mdp(password):
        """Transforme un mot de passe en hash sécurisé"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def creer(username, password, role):
        """Crée un nouvel utilisateur dans la base"""
        db = Database.get_instance()
        mdp_hash = User._hasher_mdp(password)
        db.executer(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, mdp_hash, role)
        )

    @staticmethod
    def verifier_login(username, password):
        """Vérifie les identifiants — retourne User ou None"""
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

    def est_rh(self):
        return self.role == "rh"

    def est_etudiant(self):
        return self.role == "etudiant"

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"
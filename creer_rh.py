from models.database import Database
from models.user import User

# Créer le compte RH
db = Database.get_instance()

# Vérifier si le compte existe déjà
existant = db.recuperer_un(
    "SELECT id FROM users WHERE username = ?", ("admin_rh",)
)

if existant:
    print("Le compte RH existe déjà !")
else:
    User.creer("admin_rh", "rh1234", "rh")
    print("Compte RH créé avec succès !")

# Afficher tous les utilisateurs
tous = db.recuperer_tous("SELECT id, username, role FROM users")
print("\nUtilisateurs dans la base :")
for u in tous:
    print(f"  - {u['username']} ({u['role']})")
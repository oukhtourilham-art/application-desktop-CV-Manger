from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from controllers.auth_controller import AuthController

class LoginView(QWidget):

    # Signaux émis vers la fenêtre principale
    login_reussi = Signal(str) # émet le role("etudiant" / "rh")
    aller_inscription = Signal()

    def __init__(self):
        super().__init__()
        self._construire_ui()
        self._appliquer_styles()

    def _construire_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setSpacing(0)

        # Carte centrale 
        carte = QFrame()
        carte.setObjectName("carte")
        carte.setFixedWidth(420)
        layout_carte = QVBoxLayout(carte)
        layout_carte.setSpacing(16)
        layout_carte.setContentsMargins(40, 40, 40, 40)

        # Titre
        titre = QLabel("CV Manager")
        titre.setObjectName("titre")
        titre.setAlignment(Qt.AlignCenter)

        sous_titre = QLabel("Connectez-vous à votre espace")
        sous_titre.setObjectName("sous_titre")
        sous_titre.setAlignment(Qt.AlignCenter)

        # Champs
        self.champ_username = QLineEdit()
        self.champ_username.setPlaceholderText("Nom d'utilisateur")
        self.champ_username.setObjectName("champ")

        self.champ_password = QLineEdit()
        self.champ_password.setPlaceholderText("Mot de passe")
        self.champ_password.setEchoMode(QLineEdit.Password)
        self.champ_password.setObjectName("champ")
        # Connexion avec la touche Entrée
        self.champ_password.returnPressed.connect(self._connecter)

        # Boutons
        self.btn_connexion = QPushButton("Se connecter")
        self.btn_connexion.setObjectName("btn_principal")
        self.btn_connexion.clicked.connect(self._connecter)
        self.btn_connexion.setCursor(Qt.PointingHandCursor)

        self.btn_inscription = QPushButton("Créer un compte étudiant")
        self.btn_inscription.setObjectName("btn_secondaire")
        self.btn_inscription.clicked.connect(self.aller_inscription.emit)
        self.btn_inscription.setCursor(Qt.PointingHandCursor)

        # Assemblage
        layout_carte.addWidget(titre)
        layout_carte.addWidget(sous_titre)
        layout_carte.addSpacing(16)
        layout_carte.addWidget(QLabel("Nom d'utilisateur"))
        layout_carte.addWidget(self.champ_username)
        layout_carte.addWidget(QLabel("Mot de passe"))
        layout_carte.addWidget(self.champ_password)
        layout_carte.addSpacing(8)
        layout_carte.addWidget(self.btn_connexion)
        layout_carte.addWidget(self.btn_inscription)

        layout_principal.addWidget(carte, alignment=Qt.AlignCenter)

    def _connecter(self):
        username = self.champ_username.text().strip()
        password = self.champ_password.text().strip()

        succes, resultat = AuthController.connecter(username, password)

        if succes:
            self.champ_username.clear()
            self.champ_password.clear()
            self.login_reussi.emit(resultat.role)
        else:
            QMessageBox.warning(self, "Erreur de connexion", resultat)

    def _appliquer_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F4F8;
                font-family: Arial;
            }
            #carte {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
            }
            #titre {
                font-size: 28px;
                font-weight: bold;
                color: #1F4E79;
            }
            #sous_titre {
                font-size: 13px;
                color: #888888;
                margin-bottom: 8px;
            }
            QLabel {
                font-size: 13px;
                color: #444444;
                font-weight: bold;
            }
            #champ {
                padding: 10px 14px;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                font-size: 14px;
                background: #FAFAFA;
            }
            #champ:focus {
                border: 1.5px solid #2E75B6;
                background: white;
            }
            #btn_principal {
                padding: 12px;
                background-color: #2E75B6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            #btn_principal:hover {
                background-color: #1F5A9A;
            }
            #btn_secondaire {
                padding: 10px;
                background-color: transparent;
                color: #2E75B6;
                border: 1.5px solid #2E75B6;
                border-radius: 8px;
                font-size: 13px;
            }
            #btn_secondaire:hover {
                background-color: #EAF2FB;
            }
        """)
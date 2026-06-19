from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from controllers.auth_controller import AuthController

class InscriptionView(QWidget):

    inscription_reussie = Signal()
    retour_login        = Signal()

    def __init__(self):
        super().__init__()
        self._construire_ui()
        self._appliquer_styles()

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        carte = QFrame()
        carte.setObjectName("carte")
        carte.setFixedWidth(420)
        layout_carte = QVBoxLayout(carte)
        layout_carte.setSpacing(14)
        layout_carte.setContentsMargins(40, 40, 40, 40)

        titre = QLabel("Créer un compte")
        titre.setObjectName("titre")
        titre.setAlignment(Qt.AlignCenter)

        sous_titre = QLabel("Espace réservé aux étudiants")
        sous_titre.setObjectName("sous_titre")
        sous_titre.setAlignment(Qt.AlignCenter)

        self.champ_username = QLineEdit()
        self.champ_username.setPlaceholderText("Choisir un nom d'utilisateur")
        self.champ_username.setObjectName("champ")

        self.champ_password = QLineEdit()
        self.champ_password.setPlaceholderText("Choisir un mot de passe")
        self.champ_password.setEchoMode(QLineEdit.Password)
        self.champ_password.setObjectName("champ")

        self.champ_confirmation = QLineEdit()
        self.champ_confirmation.setPlaceholderText("Confirmer le mot de passe")
        self.champ_confirmation.setEchoMode(QLineEdit.Password)
        self.champ_confirmation.setObjectName("champ")

        self.btn_inscrire = QPushButton("Créer le compte")
        self.btn_inscrire.setObjectName("btn_principal")
        self.btn_inscrire.clicked.connect(self._inscrire)
        self.btn_inscrire.setCursor(Qt.PointingHandCursor)

        self.btn_retour = QPushButton("← Retour à la connexion")
        self.btn_retour.setObjectName("btn_secondaire")
        self.btn_retour.clicked.connect(self.retour_login.emit)
        self.btn_retour.setCursor(Qt.PointingHandCursor)

        layout_carte.addWidget(titre)
        layout_carte.addWidget(sous_titre)
        layout_carte.addSpacing(12)
        layout_carte.addWidget(QLabel("Nom d'utilisateur"))
        layout_carte.addWidget(self.champ_username)
        layout_carte.addWidget(QLabel("Mot de passe"))
        layout_carte.addWidget(self.champ_password)
        layout_carte.addWidget(QLabel("Confirmer le mot de passe"))
        layout_carte.addWidget(self.champ_confirmation)
        layout_carte.addSpacing(8)
        layout_carte.addWidget(self.btn_inscrire)
        layout_carte.addWidget(self.btn_retour)

        layout.addWidget(carte, alignment=Qt.AlignCenter)

    def _inscrire(self):
        username     = self.champ_username.text().strip()
        password     = self.champ_password.text().strip()
        confirmation = self.champ_confirmation.text().strip()

        succes, message = AuthController.inscrire(username, password, confirmation)

        if succes:
            QMessageBox.information(self, "Succès",
                "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            self.champ_username.clear()
            self.champ_password.clear()
            self.champ_confirmation.clear()
            self.inscription_reussie.emit()
        else:
            QMessageBox.warning(self, "Erreur", message)

    def _appliquer_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F0F4F8; font-family: Arial; }
            #carte {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E0E0E0;
            }
            #titre { font-size: 26px; font-weight: bold; color: #1F4E79; }
            #sous_titre { font-size: 13px; color: #888888; }
            QLabel { font-size: 13px; color: #444444; font-weight: bold; }
            #champ {
                padding: 10px 14px;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                font-size: 14px;
                background: #FAFAFA;
            }
            #champ:focus { border: 1.5px solid #2E75B6; background: white; }
            #btn_principal {
                padding: 12px; background-color: #2E75B6;
                color: white; border: none; border-radius: 8px;
                font-size: 14px; font-weight: bold;
            }
            #btn_principal:hover { background-color: #1F5A9A; }
            #btn_secondaire {
                padding: 10px; background-color: transparent;
                color: #2E75B6; border: 1.5px solid #2E75B6;
                border-radius: 8px; font-size: 13px;
            }
            #btn_secondaire:hover { background-color: #EAF2FB; }
        """)
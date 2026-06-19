from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt
from views.login_view import LoginView
from views.inscription_view import InscriptionView
from views.student_view import StudentView
from views.hr_view import HRView

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._construire_ui()

    def _construire_ui(self):
        # QStackedWidget = "pile de pages" — une seule visible à la fois
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Créer toutes les vues
        self.login_view       = LoginView()
        self.inscription_view = InscriptionView()
        self.student_view     = StudentView()
        self.hr_view          = HRView()

        # Ajouter à la pile (ordre = index)
        self.stack.addWidget(self.login_view)        # index 0
        self.stack.addWidget(self.inscription_view)  # index 1
        self.stack.addWidget(self.student_view)      # index 2
        self.stack.addWidget(self.hr_view)           # index 3

        #  Connexions des signaux 
        # Login : selon le rôle
        self.login_view.login_reussi.connect(self._apres_login)
        self.login_view.aller_inscription.connect(self._aller_inscription)

        # Inscription : retour login
        self.inscription_view.inscription_reussie.connect(self._aller_login)
        self.inscription_view.retour_login.connect(self._aller_login)

        # Déconnexion : retour login
        self.student_view.deconnexion.connect(self._aller_login)
        self.hr_view.deconnexion.connect(self._aller_login)

        # Démarrer sur la page login
        self.stack.setCurrentIndex(0)

    def _apres_login(self, role):
        """Redirige vers la bonne vue selon le rôle"""
        if role == "rh":
            self.hr_view.actualiser()
            self.stack.setCurrentIndex(3)
        else:
            self.student_view.actualiser()
            self.stack.setCurrentIndex(2)

    def _aller_login(self):
        self.stack.setCurrentIndex(0)

    def _aller_inscription(self):
        self.stack.setCurrentIndex(1)
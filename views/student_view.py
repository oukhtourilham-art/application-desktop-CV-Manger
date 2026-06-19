from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QFrame,
    QHeaderView, QProgressBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from controllers.cv_controller import CVController
from controllers.auth_controller import AuthController
from services.score_service import ScoreService

class StudentView(QWidget):

    deconnexion = Signal()

    def __init__(self):
        super().__init__()
        self._construire_ui()
        self._appliquer_styles()

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Barre du haut 
        barre = QFrame()
        barre.setObjectName("barre")
        barre.setFixedHeight(64)
        layout_barre = QHBoxLayout(barre)
        layout_barre.setContentsMargins(24, 0, 24, 0)

        self.lbl_bienvenue = QLabel("Bienvenue !")
        self.lbl_bienvenue.setObjectName("lbl_bienvenue")

        btn_deconnexion = QPushButton("Déconnexion")
        btn_deconnexion.setObjectName("btn_deconnexion")
        btn_deconnexion.clicked.connect(self._deconnecter)
        btn_deconnexion.setCursor(Qt.PointingHandCursor)

        layout_barre.addWidget(self.lbl_bienvenue)
        layout_barre.addStretch()
        layout_barre.addWidget(btn_deconnexion)

        # Contenu principal 
        contenu = QWidget()
        contenu.setObjectName("contenu")
        layout_contenu = QVBoxLayout(contenu)
        layout_contenu.setContentsMargins(32, 24, 32, 24)
        layout_contenu.setSpacing(20)

        # Zone upload
        zone_upload = QFrame()
        zone_upload.setObjectName("zone_upload")
        layout_upload = QVBoxLayout(zone_upload)
        layout_upload.setAlignment(Qt.AlignCenter)
        layout_upload.setSpacing(12)

        lbl_upload = QLabel("📄 Déposez votre CV ici")
        lbl_upload.setObjectName("lbl_upload")
        lbl_upload.setAlignment(Qt.AlignCenter)

        lbl_formats = QLabel("Formats acceptés : PDF, TXT  —  Taille max : 5 Mo")
        lbl_formats.setObjectName("lbl_formats")
        lbl_formats.setAlignment(Qt.AlignCenter)

        self.btn_upload = QPushButton("Choisir un fichier CV")
        self.btn_upload.setObjectName("btn_upload")
        self.btn_upload.clicked.connect(self._uploader_cv)
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.setFixedWidth(220)

        layout_upload.addWidget(lbl_upload)
        layout_upload.addWidget(lbl_formats)
        layout_upload.addWidget(self.btn_upload, alignment=Qt.AlignCenter)

        # Titre tableau
        lbl_mes_cv = QLabel("Mes CV analysés")
        lbl_mes_cv.setObjectName("lbl_section")

        # Tableau des CV
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)
        self.tableau.setHorizontalHeaderLabels([
            "Fichier", "Score", "Niveau", "Compétences", "Date"
        ])
        self.tableau.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableau.setAlternatingRowColors(True)
        self.tableau.verticalHeader().setVisible(False)

        layout_contenu.addWidget(zone_upload)
        layout_contenu.addWidget(lbl_mes_cv)
        layout_contenu.addWidget(self.tableau)

        layout.addWidget(barre)
        layout.addWidget(contenu)

    def actualiser(self):
        """Appelée à chaque fois que la vue devient active"""
        user = AuthController.get_utilisateur()
        if user:
            self.lbl_bienvenue.setText(f"👤 Bienvenue, {user.username}")
        self._charger_tableau()

    def _charger_tableau(self):
        """Charge les CV de l'étudiant dans le tableau"""
        cvs = CVController.get_cvs_etudiant()
        self.tableau.setRowCount(len(cvs))

        for i, cv in enumerate(cvs):
            skills = cv.get_skills()
            niveau = ScoreService.get_niveau(cv.score)
            couleur = ScoreService.get_couleur(cv.score)

            self.tableau.setItem(i, 0, QTableWidgetItem(cv.filename))
            self.tableau.setItem(i, 1, QTableWidgetItem(f"{cv.score:.1f} / 100"))
            self.tableau.setItem(i, 2, QTableWidgetItem(niveau))
            self.tableau.setItem(i, 3, QTableWidgetItem(str(len(skills))))
            self.tableau.setItem(i, 4, QTableWidgetItem(
                cv.uploaded_at[:10] if cv.uploaded_at else "-"
            ))

            # Coloriser le niveau
            item_niveau = self.tableau.item(i, 2)
            item_niveau.setForeground(QColor(couleur))

    def _uploader_cv(self):
        """Ouvre le dialogue de sélection de fichier"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un CV",
            "",
            "Fichiers CV (*.pdf *.txt)"
        )
        if not filepath:
            return

        self.btn_upload.setText("Analyse en cours...")
        self.btn_upload.setEnabled(False)

        succes, resultat = CVController.uploader_cv(filepath)

        self.btn_upload.setText("Choisir un fichier CV")
        self.btn_upload.setEnabled(True)

        if succes:
            details = resultat["details"]
            msg = (
                f"✅ CV analysé avec succès !\n\n"
                f"Score : {details['score']} / 100\n"
                f"Niveau : {details['niveau']}\n"
                f"Compétences détectées : {details['nb_competences']}\n"
                f"Domaines couverts : {details['nb_domaines']}"
            )
            QMessageBox.information(self, "Analyse terminée", msg)
            self._charger_tableau()
        else:
            QMessageBox.warning(self, "Erreur", resultat)

    def _deconnecter(self):
        AuthController.deconnecter()
        self.deconnexion.emit()

    def _appliquer_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: Arial; background-color: #F0F4F8; }
            #barre {
                background-color: #1F4E79;
            }
            #lbl_bienvenue {
                color: white; font-size: 15px; font-weight: bold;
            }
            #btn_deconnexion {
                color: white; background: transparent;
                border: 1px solid white; border-radius: 6px;
                padding: 6px 14px; font-size: 13px;
            }
            #btn_deconnexion:hover { background: rgba(255,255,255,0.15); }
            #contenu { background-color: #F0F4F8; }
            #zone_upload {
                background: white; border-radius: 12px;
                border: 2px dashed #AACCEE;
                padding: 24px;
            }
            #lbl_upload { font-size: 18px; color: #1F4E79; font-weight: bold; }
            #lbl_formats { font-size: 12px; color: #999999; }
            #btn_upload {
                background-color: #2E75B6; color: white;
                border: none; border-radius: 8px;
                padding: 10px 20px; font-size: 14px; font-weight: bold;
            }
            #btn_upload:hover { background-color: #1F5A9A; }
            #btn_upload:disabled { background-color: #AAAAAA; }
            #lbl_section {
                font-size: 16px; font-weight: bold; color: #1F4E79;
            }
            QTableWidget {
                background: white; border-radius: 8px;
                border: 1px solid #E0E0E0; gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #1F4E79; color: white;
                font-weight: bold; padding: 8px; border: none;
            }
            QTableWidget::item:selected { background-color: #D6E4F0; }
        """)
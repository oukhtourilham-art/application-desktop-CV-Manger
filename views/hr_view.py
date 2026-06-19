from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QFrame, QComboBox, QHeaderView, QSplitter,
    QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from controllers.hr_controller import HRController
from controllers.auth_controller import AuthController

class HRView(QWidget):

    deconnexion = Signal()

    def __init__(self):
        super().__init__()
        self._construire_ui()
        self._appliquer_styles()

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        #  Barre du haut 
        barre = QFrame()
        barre.setObjectName("barre")
        barre.setFixedHeight(64)
        layout_barre = QHBoxLayout(barre)
        layout_barre.setContentsMargins(24, 0, 24, 0)

        lbl_titre = QLabel("📊 Tableau de Bord RH — CV Manager")
        lbl_titre.setObjectName("lbl_bienvenue")

        btn_deconnexion = QPushButton("Déconnexion")
        btn_deconnexion.setObjectName("btn_deconnexion")
        btn_deconnexion.clicked.connect(self._deconnecter)
        btn_deconnexion.setCursor(Qt.PointingHandCursor)

        layout_barre.addWidget(lbl_titre)
        layout_barre.addStretch()
        layout_barre.addWidget(btn_deconnexion)

        #  Barre de filtres 
        barre_filtres = QFrame()
        barre_filtres.setObjectName("barre_filtres")
        layout_filtres = QHBoxLayout(barre_filtres)
        layout_filtres.setContentsMargins(24, 12, 24, 12)

        lbl_filtre = QLabel("Filtrer par domaine :")
        lbl_filtre.setObjectName("lbl_filtre")

        self.combo_domaine = QComboBox()
        self.combo_domaine.setObjectName("combo")
        self.combo_domaine.setFixedWidth(200)
        self.combo_domaine.addItem("Tous les domaines")
        self.combo_domaine.currentIndexChanged.connect(self._filtrer)

        self.lbl_nb_resultats = QLabel("0 candidat(s)")
        self.lbl_nb_resultats.setObjectName("lbl_nb")

        layout_filtres.addWidget(lbl_filtre)
        layout_filtres.addWidget(self.combo_domaine)
        layout_filtres.addSpacing(20)
        layout_filtres.addWidget(self.lbl_nb_resultats)
        layout_filtres.addStretch()

        #  Contenu : tableau + graphique 
        splitter = QSplitter(Qt.Horizontal)

        # Tableau des candidats
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)
        self.tableau.setHorizontalHeaderLabels([
            "Candidat", "Fichier CV", "Score", "Niveau", "Nb Compétences"
        ])
        self.tableau.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableau.setAlternatingRowColors(True)
        self.tableau.verticalHeader().setVisible(False)
        self.tableau.itemSelectionChanged.connect(self._afficher_details)

        # Panneau détails + graphique
        panneau_droite = QWidget()
        layout_droite = QVBoxLayout(panneau_droite)
        layout_droite.setContentsMargins(8, 0, 8, 0)

        lbl_details = QLabel("Détails du candidat")
        lbl_details.setObjectName("lbl_section")

        self.txt_details = QTextEdit()
        self.txt_details.setReadOnly(True)
        self.txt_details.setObjectName("txt_details")
        self.txt_details.setFixedHeight(180)
        self.txt_details.setPlaceholderText(
            "Sélectionnez un candidat pour voir ses compétences..."
        )

        lbl_graph = QLabel("Scores des candidats")
        lbl_graph.setObjectName("lbl_section")

        # Graphique Matplotlib
        self.figure = Figure(figsize=(4, 3), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)

        layout_droite.addWidget(lbl_details)
        layout_droite.addWidget(self.txt_details)
        layout_droite.addWidget(lbl_graph)
        layout_droite.addWidget(self.canvas)

        splitter.addWidget(self.tableau)
        splitter.addWidget(panneau_droite)
        splitter.setSizes([600, 400])

        layout.addWidget(barre)
        layout.addWidget(barre_filtres)
        layout.addWidget(splitter)

    def actualiser(self):
        """Appelée à chaque fois que la vue devient active"""
        self._charger_domaines()
        self._charger_tableau()
        self._mettre_a_jour_graphique()

    def _charger_domaines(self):
        """Charge les domaines disponibles dans le combobox"""
        self.combo_domaine.blockSignals(True)
        self.combo_domaine.clear()
        self.combo_domaine.addItem("Tous les domaines")
        domaines = HRController.get_domaines_disponibles()
        for d in domaines:
            self.combo_domaine.addItem(d)
        self.combo_domaine.blockSignals(False)

    def _charger_tableau(self, domaine=None):
        """Charge les candidats dans le tableau"""
        if domaine and domaine != "Tous les domaines":
            resultats = HRController.filtrer_par_domaine(domaine)
        else:
            resultats = HRController.get_tous_les_cvs()

        self.tableau.setRowCount(len(resultats))
        self.lbl_nb_resultats.setText(f"{len(resultats)} candidat(s)")

        for i, r in enumerate(resultats):
            self.tableau.setItem(i, 0, QTableWidgetItem(r["candidat"]))
            self.tableau.setItem(i, 1, QTableWidgetItem(r["cv"].filename))
            self.tableau.setItem(i, 2, QTableWidgetItem(
                f"{r['cv'].score:.1f} / 100"
            ))
            self.tableau.setItem(i, 3, QTableWidgetItem(r["niveau"]))
            self.tableau.setItem(i, 4, QTableWidgetItem(str(r["nb_skills"])))

            # Stocker cv_id dans la ligne (colonne cachée)
            item = self.tableau.item(i, 0)
            item.setData(Qt.UserRole, r["cv"].id)

            # Coloriser le niveau
            self.tableau.item(i, 3).setForeground(QColor(r["couleur"]))

    def _filtrer(self):
        """Appelée quand le filtre domaine change"""
        domaine = self.combo_domaine.currentText()
        self._charger_tableau(domaine)
        self._mettre_a_jour_graphique()

    def _afficher_details(self):
        """Affiche les compétences du candidat sélectionné"""
        lignes = self.tableau.selectedItems()
        if not lignes:
            return

        ligne = self.tableau.currentRow()
        item = self.tableau.item(ligne, 0)
        cv_id = item.data(Qt.UserRole)

        from controllers.cv_controller import CVController
        details = CVController.get_details_cv(cv_id)
        if not details:
            return

        # Construire le texte des détails
        texte = f"👤 Candidat : {item.text()}\n"
        texte += f"📄 Fichier  : {details['cv'].filename}\n"
        texte += f"🎯 Score    : {details['cv'].score:.1f} / 100 ({details['niveau']})\n\n"
        texte += "── Compétences par domaine ──\n"

        for domaine, skills in details["groupes"].items():
            texte += f"\n  {domaine} :\n"
            for s in skills:
                texte += f"    • {s}\n"

        self.txt_details.setText(texte)

    def _mettre_a_jour_graphique(self):
        """Dessine le graphique des scores avec Matplotlib"""
        stats = HRController.get_statistiques()
        self.figure.clear()

        if not stats or stats["nb_candidats"] == 0:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "Aucune donnée",
                    ha="center", va="center", fontsize=12, color="gray")
            self.canvas.draw()
            return

        ax = self.figure.add_subplot(111)

        # Couleurs selon les scores
        couleurs = []
        for score in stats["scores"]:
            if score >= 80:   couleurs.append("#27AE60")
            elif score >= 60: couleurs.append("#2E86C1")
            elif score >= 40: couleurs.append("#F39C12")
            else:             couleurs.append("#E74C3C")

        barres = ax.bar(stats["noms"], stats["scores"],
                        color=couleurs, edgecolor="white", linewidth=0.5)

        # Ligne score moyen
        ax.axhline(y=stats["score_moyen"], color="#888888",
                   linestyle="--", linewidth=1,
                   label=f"Moyenne : {stats['score_moyen']}")

        ax.set_ylim(0, 105)
        ax.set_ylabel("Score / 100", fontsize=9)
        ax.set_title("Scores des candidats", fontsize=10, fontweight="bold")
        ax.legend(fontsize=8)
        ax.tick_params(axis='x', labelsize=8, rotation=15)
        ax.tick_params(axis='y', labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.canvas.draw()

    def _deconnecter(self):
        AuthController.deconnecter()
        self.deconnexion.emit()

    def _appliquer_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: Arial; background-color: #F0F4F8; }
            #barre { background-color: #1F4E79; }
            #lbl_bienvenue { color: white; font-size: 15px; font-weight: bold; }
            #btn_deconnexion {
                color: white; background: transparent;
                border: 1px solid white; border-radius: 6px;
                padding: 6px 14px; font-size: 13px;
            }
            #btn_deconnexion:hover { background: rgba(255,255,255,0.15); }
            #barre_filtres {
                background: white;
                border-bottom: 1px solid #E0E0E0;
            }
            #lbl_filtre { font-size: 13px; color: #444444; font-weight: bold; }
            #lbl_nb { font-size: 13px; color: #2E75B6; font-weight: bold; }
            #combo {
                padding: 6px 10px; border: 1px solid #CCCCCC;
                border-radius: 6px; font-size: 13px; background: white;
            }
            QTableWidget {
                background: white; border: 1px solid #E0E0E0;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #1F4E79; color: white;
                font-weight: bold; padding: 8px; border: none;
            }
            QTableWidget::item:selected { background-color: #D6E4F0; }
            #lbl_section {
                font-size: 14px; font-weight: bold;
                color: #1F4E79; margin-top: 8px;
            }
            #txt_details {
                border: 1px solid #E0E0E0; border-radius: 8px;
                background: white; font-size: 13px;
                padding: 8px; color: #333333;
            }
        """)
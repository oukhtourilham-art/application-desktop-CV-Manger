# sys -> bibliothèque python intégrée , nécessaire pour lancer / quitter l'app proprement 
import sys
from PySide6.QtWidgets import QApplication
# QApplication -> c'est le "moteur" de PySide6, obligatoire pour toute app graphique
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from views.main_window import MainWindow

def main():
    #Créer l'application PySide6
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    #Créer et afficher la fenêtre principale
    window = MainWindow()
    window.setWindowTitle(APP_NAME)
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.show()

#Lancer la boucle principale
if __name__ == "__main__":
        main()      # ça sinifier "lance main() seulement si on exécute ce ficher directement"

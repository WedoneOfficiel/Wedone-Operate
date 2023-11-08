import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QInputDialog, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import requests

class WedoneOperateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wedone Operate")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("icon.png"))  # Utilisez votre icône au format .png
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Bienvenue dans Wedone Operate 3.0 ! Bonne aventure !")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #c2e59c; padding: 10px; margin: 0;")
        self.layout.addWidget(self.label)

        self.label = QLabel("Combien d'épreuves souhaitez-vous faire ?")
        self.label.setStyleSheet("font-size: 14px; margin-top: 10px;")
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setStyleSheet("font-size: 14px")
        self.layout.addWidget(self.input)

        self.start_button = QPushButton("Commencer")
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("font-size: 14px; background-color: #64b3f4; color: white; font-weight: bold;")
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game(self):
        try:
            nombre_epreuves = int(self.input.text())
            score = 0

            for i in range(1, nombre_epreuves + 1):
                operation = random.randint(1, 4)
                resultat = 0

                if operation == 1:  # Addition
                    while True:
                        nombre1 = random.randint(1, 100)
                        nombre2 = random.randint(1, 100 - nombre1)
                        if nombre1 != nombre2:
                            break
                    resultat = nombre1 + nombre2
                    operation_str = "+"
                elif operation == 2:  # Soustraction
                    while True:
                        nombre1 = random.randint(1, 100)
                        nombre2 = random.randint(1, nombre1)
                        if nombre1 != nombre2:
                            break
                    resultat = nombre1 - nombre2
                    operation_str = "-"
                elif operation == 3:  # Multiplication
                    while True:
                        nombre1 = random.randint(1, 10)
                        nombre2 = random.randint(1, 10)
                        if nombre1 != nombre2:
                            break
                    resultat = nombre1 * nombre2
                    operation_str = "*"
                else:  # Division
                    while True:
                        nombre1 = random.randint(1, 10)
                        nombre2 = random.randint(2, 10)  # Limite la division par 1
                        if nombre1 != nombre2 and nombre1 % nombre2 == 0:
                            break
                    resultat = nombre1 // nombre2
                    operation_str = "/"

                user_input, ok_pressed = QInputDialog.getInt(self, f"Épreuve {i}", f"{nombre1} {operation_str} {nombre2} = ?")
                if not ok_pressed:
                    return

                if user_input == resultat:
                    score += 1
                    QMessageBox.information(self, "Bonne réponse", "Bonne réponse !")
                else:
                    QMessageBox.information(self, "Mauvaise réponse", f"Mauvaise réponse. La réponse correcte était {resultat}.")

            pourcentage = score * 100 / nombre_epreuves
            message = f"Vous avez réussi {score} épreuves sur {nombre_epreuves}.\nVotre pourcentage de réussite est de {pourcentage:.2f}%."
            QMessageBox.information(self, "Résultat", message)
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un nombre valide pour le nombre d'épreuves.")

def checkForUpdates():
    versionURL = "https://wedoneofficiel.github.io/Boot-projets-Wedone-Officiel/Wedone-Logiciels-Versions/version-wedone-operate.txt"

    try:
        response = requests.get(versionURL)
        if response.status_code == 200:
            latestVersion = response.text.strip()
            if latestVersion > "3.0":
                message = f"<p style='font-size: 16px; font-weight: bold; color: black;'>Une nouvelle version de Wedone Operate est disponible (version {latestVersion}) !</p>\n"
                message += "Nous vous recommandons de mettre à jour l'application pour obtenir les dernières fonctionnalités et correctifs de sécurité."

                update_box = QMessageBox()
                update_box.setWindowIcon(QIcon("icon.png"))
                update_box.setIcon(QMessageBox.Information)
                update_box.setWindowTitle("Mise à jour disponible")
                update_box.setText(message)
                update_box.setTextFormat(Qt.RichText)

                download_button = update_box.addButton("Télécharger", QMessageBox.AcceptRole)
                download_button.setStyleSheet("font-size: 14px; background-color: #64b3f4; color: white; font-weight; bold;")

                ignore_button = update_box.addButton("Ignorer", QMessageBox.RejectRole)

                result = update_box.exec_()
                if result == QMessageBox.AcceptRole:
                    import webbrowser
                    webbrowser.open("https://github.com/WedoneOfficiel/Wedone-Operate/releases")
            else:
                pass
        else:
            print("Impossible de récupérer la version la plus récente.")
    except requests.exceptions.RequestException:
        print("Impossible de récupérer la version la plus récente.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    checkForUpdates()
    window = WedoneOperateApp()
    window.show()
    sys.exit(app.exec_())
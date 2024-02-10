import sys
import random
import requests
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QInputDialog, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class WedoneOperateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wedone Operate")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("Bienvenue dans Wedone Operate 3.2 ! Bonne aventure !", self)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2b2b2b;")
        self.layout.addWidget(self.label)

        self.label = QLabel("Combien d'épreuves souhaitez-vous faire ?", self)
        self.label.setStyleSheet("font-size: 14px; color: #64b3f4; margin-top: 10px;")
        self.layout.addWidget(self.label)

        self.input = QLineEdit(self)
        self.input.setStyleSheet("font-size: 14px; background-color: #f0f0f0; color: #2b2b2b; border: 1px solid #64b3f4; border-radius: 5px;")
        self.layout.addWidget(self.input)

        self.start_button = QPushButton("Commencer", self)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("font-size: 14px; background-color: #64b3f4; color: white; font-weight: bold; border: 1px solid #64b3f4; border-radius: 5px;")
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
            if nombre_epreuves <= 0:
                raise ValueError

            score = 0
            for i in range(1, nombre_epreuves + 1):
                operation, nombre1, nombre2, operation_str, resultat = self.generate_operation()
                
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
            QMessageBox.critical(self, "Erreur", "Veuillez entrer un nombre valide et supérieur à 0 pour le nombre d'épreuves.")

    def generate_operation(self):
        operation = random.randint(1, 4)
        nombre1, nombre2, operation_str, resultat = 0, 0, "", 0

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
                nombre2 = random.randint(2, 10)
                if nombre1 != nombre2 and nombre1 % nombre2 == 0:
                    break
            resultat = nombre1 // nombre2
            operation_str = "/"

        return operation, nombre1, nombre2, operation_str, resultat

class UpdateMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.png"))
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("Mise à jour disponible")
        self.setTextFormat(Qt.PlainText)
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

    def show_update_message(self, latest_version):
        message = f"Une nouvelle version de Wedone Operate est disponible (version {latest_version.strip()}) !\n\n"
        message += "Nous vous recommandons de mettre à jour l'application pour obtenir les dernières fonctionnalités et correctifs de sécurité."

        self.setText(message)
        self.setFont(QFont("Arial", 12))  # Police normale

        download_button = self.addButton("  Télécharger  ", QMessageBox.AcceptRole)
        download_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")

        ignore_button = self.addButton("  Ignorer  ", QMessageBox.RejectRole)
        ignore_button.setStyleSheet("font-size: 14px; background-color: white; color: #3498db; font-weight: bold; border: 1px solid #3498db; border-radius: 5px;")

def check_for_updates():
    version_url = "https://wedoneofficiel.github.io/Boot-projets-Wedone-Officiel/Wedone-Logiciels-Versions/version-wedone-operate.txt"

    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if float(latest_version) > 3.2:  # Comparaison en tant que nombre flottant
                update_box = UpdateMessageBox()
                update_box.show_update_message(latest_version)

                result = update_box.exec_()
                if result == QMessageBox.AcceptRole:
                    webbrowser.open("https://github.com/WedoneOfficiel/Wedone-Operate/releases")
    except requests.exceptions.RequestException:
        print("Impossible de récupérer la version la plus récente.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    check_for_updates()
    window = WedoneOperateApp()
    window.show()
    sys.exit(app.exec_())

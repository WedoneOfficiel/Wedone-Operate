import sys
import random
import requests
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QDialog, QTextEdit, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSlot

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

        self.label = QLabel("Bienvenue dans Wedone Operate 3.4 ! Bonne aventure !", self)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2b2b2b;")
        self.layout.addWidget(self.label)

        self.label = QLabel("Combien d'épreuves souhaitez-vous faire ?", self)
        self.label.setStyleSheet("font-size: 14px; color: #0672BC; margin-top: 10px;")
        self.layout.addWidget(self.label)

        self.input = QLineEdit(self)
        self.input.setStyleSheet("font-size: 14px; background-color: #f0f0f0; color: #2b2b2b; border: 1px solid #0672BC; border-radius: 5px;")
        self.layout.addWidget(self.input)

        self.start_button = QPushButton("Commencer", self)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def start_game(self):
        self.execute_game()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.execute_game()

    def execute_game(self):
        try:
            nombre_epreuves = self.input.text()
            if not nombre_epreuves.isdigit() or int(nombre_epreuves) <= 0:
                raise ValueError("Veuillez entrer un nombre valide et supérieur à 0 pour le nombre d'épreuves.")

            nombre_epreuves = int(nombre_epreuves)

            score = 0
            for i in range(1, nombre_epreuves + 1):
                operation, nombre1, nombre2, operation_str, resultat = self.generate_operation()
                
                dialog = AnswerDialog(f"Épreuve {i}", f"{nombre1} {operation_str} {nombre2} = ?")
                user_input = dialog.get_answer()
                if user_input is None:
                    return

                if user_input == resultat:
                    score += 1
                    message_window = MessageWindow("Bonne réponse", "Bonne réponse !")
                    message_window.exec_()
                else:
                    message_window = MessageWindow("Mauvaise réponse", f"Mauvaise réponse. La réponse correcte était {resultat}.")
                    message_window.exec_()

            pourcentage = score * 100 / nombre_epreuves
            message = f"Vous avez réussi {score} épreuves sur {nombre_epreuves}.\nVotre pourcentage de réussite est de {pourcentage:.2f}%."
            result_window = MessageWindow("Résultat", message)
            result_window.exec_()
        except ValueError as e:
            error_window = InputErrorWindow("Erreur", str(e))
            error_window.exec_()

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

class MessageWindow(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        layout.addWidget(ok_button)

        self.setLayout(layout)

class InputErrorWindow(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        layout.addWidget(ok_button)

        self.setLayout(layout)

class AnswerDialog(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        self.answer_input = QLineEdit()
        self.answer_input.setStyleSheet("font-size: 14px; background-color: #f0f0f0; color: #2b2b2b; border: 1px solid #0672BC; border-radius: 5px;")
        layout.addWidget(self.answer_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_answer(self):
        if self.exec_() == QDialog.Accepted:
            user_input = self.answer_input.text()
            if user_input.strip() == "":
                return None
            return int(user_input)
        return None

class UpdateWindow(QDialog):
    def __init__(self, latest_version):
        super().__init__()
        self.setWindowTitle("Mise à jour disponible")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

        layout = QVBoxLayout(self)

        label = QLabel(f"Une nouvelle version de Wedone Operate est disponible (version {latest_version}) !\n\nNous vous recommandons de mettre à jour l'application pour obtenir les dernières fonctionnalités et correctifs de sécurité.")
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        # Ajout d'un espace blanc entre les boutons Télécharger et Ignorer
        buttons_layout.addStretch()

        ignore_button = QPushButton(" Ignorer ")
        ignore_button.clicked.connect(self.close)
        ignore_button.setStyleSheet("font-size: 14px; background-color: #E7E3E3; color: #2b2b2b; font-weight: bold; border: 1px solid #E7E3E3; border-radius: 5px;")
        buttons_layout.addWidget(ignore_button)

        download_button = QPushButton(" Télécharger ")
        download_button.clicked.connect(self.download_update)
        download_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        buttons_layout.addWidget(download_button)

        self.setLayout(layout)

    def download_update(self):
        webbrowser.open("https://github.com/WedoneOfficiel/Wedone-Operate/releases")

def check_for_updates():
    version_url = "https://wedoneofficiel.github.io/Boot-projets-Wedone-Officiel/Wedone-Logiciels-Versions/version-wedone-operate.txt"

    try:
        response = requests.get(version_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if float(latest_version) > 3.4:  # Comparaison en tant que nombre flottant
                update_window = UpdateWindow(latest_version)
                update_window.exec_()
    except requests.exceptions.RequestException:
        print("Impossible de récupérer la version la plus récente.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    check_for_updates()
    window = WedoneOperateApp()
    window.show()
    sys.exit(app.exec_())

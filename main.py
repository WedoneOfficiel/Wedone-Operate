import sys
import random
import requests
import webbrowser
import json
from PyQt5.QtWidgets import QFrame, QDialogButtonBox, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QDialog, QTextEdit, QDesktopWidget, QStackedLayout, QCheckBox, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QDate

class WedoneOperateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()  # Charger ou créer les paramètres
        self.initUI()
        self.setWindowTitle("Wedone Operate")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

    def load_settings(self):
        default_settings = {
            "auto_update": True,
            "auto_patch": True,
            "addition_enabled": True,
            "subtraction_enabled": True,
            "multiplication_enabled": True,
            "division_enabled": True
        }
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                # Mettre à jour les valeurs par défaut avec les valeurs chargées
                default_settings.update(settings)
        except FileNotFoundError:
            # Si le fichier n'existe pas, créer un nouveau fichier avec les valeurs par défaut
            with open("settings.json", "w") as file:
                json.dump(default_settings, file)
        return default_settings


    def generate_operation(self):
        available_operations = []
        if self.settings['addition_enabled']:
            available_operations.append(1)  # Addition
        if self.settings['subtraction_enabled']:
            available_operations.append(2)  # Soustraction
        if self.settings['multiplication_enabled']:
            available_operations.append(3)  # Multiplication
        if self.settings['division_enabled']:
            available_operations.append(4)  # Division

        if not available_operations:
            raise ValueError("Aucune opération n'est activée. Veuillez activer au moins un type d'opération dans les paramètres.")

        operation = random.choice(available_operations)
        # La logique pour générer l'opération basée sur le type sélectionné continue ici...

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("Bienvenue dans Wedone Operate 4.0 ! Bonne aventure !", self)
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

        self.settings_button = QPushButton("Paramètres", self)
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        self.layout.addWidget(self.settings_button)

        self.setLayout(self.layout)
        self.center()

    def showEvent(self, event):
        super().showEvent(event)
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
        available_operations = []
        settings = self.load_settings()  # Chargement des paramètres actuels
        if settings['addition_enabled']:
            available_operations.append(1)  # Addition
        if settings['subtraction_enabled']:
            available_operations.append(2)  # Soustraction
        if settings['multiplication_enabled']:
            available_operations.append(3)  # Multiplication
        if settings['division_enabled']:
            available_operations.append(4)  # Division

        if not available_operations:
            raise ValueError("Aucune opération n'est activée. Veuillez activer au moins un type d'opération dans les paramètres.")

        operation = random.choice(available_operations)  # Choix aléatoire parmi les opérations activées

        nombre1, nombre2, operation_str, resultat = 0, 0, "", 0
        if operation == 1:  # Addition
            nombre1 = random.randint(1, 100)
            nombre2 = random.randint(1, 100 - nombre1)
            resultat = nombre1 + nombre2
            operation_str = "+"
        elif operation == 2:  # Soustraction
            nombre1 = random.randint(1, 100)
            nombre2 = random.randint(1, nombre1)
            resultat = nombre1 - nombre2
            operation_str = "-"
        elif operation == 3:  # Multiplication
            nombre1 = random.randint(1, 10)
            nombre2 = random.randint(1, 10)
            resultat = nombre1 * nombre2
            operation_str = "*"
        elif operation == 4:  # Division
            nombre1 = random.randint(2, 10)
            nombre2 = random.randint(2, nombre1)
            while nombre1 % nombre2 != 0:
                nombre2 = random.randint(2, nombre1)
            resultat = nombre1 // nombre2
            operation_str = "/"

        return operation, nombre1, nombre2, operation_str, resultat


    @pyqtSlot()
    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.load_settings()
        settings_window.exec_()

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
        ignore_button.setStyleSheet("font-size: 14px; background-color: #E7E3E3; color: #2b2b2b; font-weight: none; border: 1px solid #E7E3E3; border-radius: 5px;")
        buttons_layout.addWidget(ignore_button)

        download_button = QPushButton(" Télécharger ")
        download_button.clicked.connect(self.download_update)
        download_button.setStyleSheet("font-size: 15px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        buttons_layout.addWidget(download_button)

        self.setLayout(layout)

    def download_update(self):
        webbrowser.open("https://github.com/WedoneOfficiel/Wedone-Operate/releases")

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètres")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")
        self.setMinimumSize(400, 200)

        self.initUI()
        self.load_settings()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Liste des sections à gauche
        self.sections_layout = QVBoxLayout()
        self.sections_layout.setSpacing(10)
        self.sections_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(self.sections_layout)

        self.add_section_button(" Options du logiciel ", self.show_options_section)  
        self.add_section_button(" Mises à jour ", self.show_updates_section)
        self.add_section_button(" À propos ", self.show_about_section)  
        # Ajoutez d'autres sections ici si nécessaire

        # Barre verticale
        main_layout.addWidget(QFrame(frameShape=QFrame.VLine, frameShadow=QFrame.Sunken))

        # Contenu des sections à droite
        self.stacked_layout = QStackedLayout()
        main_layout.addLayout(self.stacked_layout)

        # Paramètres de la recherche automatique des mises à jour
        self.updates_section = QWidget()
        self.updates_section.setStyleSheet("background-color: white; font-size: 14px;")
        self.create_updates_section()
        self.stacked_layout.addWidget(self.updates_section)

        # Section "À propos" - Initialisation
        self.about_section = QWidget()
        self.about_section.setStyleSheet("background-color: white; font-size: 14px;")
        self.create_about_section()
        self.stacked_layout.addWidget(self.about_section)

        # Nouvelle section "Options du logiciel" - Initialisation
        self.options_section = QWidget()
        self.options_section.setStyleSheet("background-color: white; font-size: 14px;")
        self.create_options_section()
        self.stacked_layout.addWidget(self.options_section)

        self.setLayout(main_layout)

        # Sélectionner automatiquement l'onglet "Mises à jour"
        self.show_options_section()
    
    def auto_update_changed(self, state):
        self.settings["auto_update"] = state == Qt.Checked
        print("Auto-update set to:", self.settings["auto_update"])
        self.save_settings()

    def auto_patch_changed(self, state):
        self.settings["auto_patch"] = state == Qt.Checked
        print("Auto-patch set to:", self.settings["auto_patch"])
        self.save_settings()

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file)
        print("Settings saved")

    def add_section_button(self, text, callback):
        button = QPushButton(text)
        button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        button.clicked.connect(callback)
        self.sections_layout.addWidget(button)

    def show_updates_section(self):
        self.stacked_layout.setCurrentIndex(0)
        self.highlight_selected_section(" Mises à jour ")

    def show_about_section(self):  # Fonction pour afficher la section "À propos"
        self.stacked_layout.setCurrentIndex(1)
        self.highlight_selected_section(" À propos ")

    def show_options_section(self):  # Fonction pour afficher la section "Options du logiciel"
        self.stacked_layout.setCurrentIndex(2)
        self.highlight_selected_section(" Options du logiciel ")

    def highlight_selected_section(self, section_name):
        for i in range(self.sections_layout.count()):
            button = self.sections_layout.itemAt(i).widget()
            if button.text().strip() == section_name.strip():
                button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
            else:
                button.setStyleSheet("font-size: 14px; background-color: #E7E3E3; color: #2b2b2b; font-weight: bold; border: 1px solid #E7E3E3; border-radius: 5px;")

    def create_updates_section(self):
        layout = QVBoxLayout(self.updates_section)

        self.auto_update_check = QCheckBox("Recherche automatique des mises à jour")
        self.auto_update_check.stateChanged.connect(self.auto_update_changed)
        self.auto_update_check.setStyleSheet("font-size: 14px; color: black;")
        layout.addWidget(self.auto_update_check)

        self.auto_patch_check = QCheckBox("Recherche automatique des patchs")
        self.auto_patch_check.stateChanged.connect(self.auto_patch_changed)
        self.auto_patch_check.setStyleSheet("font-size: 14px; color: black;")
        layout.addWidget(self.auto_patch_check)

        # Bouton de recherche manuelle des mises à jour
        manual_update_button = QPushButton(" Rechercher manuellement les mises à jour ")
        manual_update_button.setStyleSheet("font-size: 14px; background-color: #f0f0f0; color: #2b2b2b; border: 1px solid #0672BC; border-radius: 5px;")
        manual_update_button.clicked.connect(self.manual_update)
        layout.addWidget(manual_update_button)

        # Bouton de recherche manuelle des patchs
        manual_patch_button = QPushButton(" Rechercher manuellement les patchs ")
        manual_patch_button.setStyleSheet("font-size: 14px; background-color: #f0f0f0; color: #2b2b2b; border: 1px solid #0672BC; border-radius: 5px;")
        manual_patch_button.clicked.connect(self.manual_patch)
        layout.addWidget(manual_patch_button)

    def create_about_section(self):  # Fonction pour créer la section "À propos"
        layout = QVBoxLayout(self.about_section)

        # Chargement de l'icône
        icon_label = QLabel()
        pixmap = QPixmap("icon.png")
        pixmap = pixmap.scaledToWidth(50)  # Ajuster la largeur de l'icône à 50 pixels
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Numéro de version
        version_layout = QHBoxLayout()
        version_label = QLabel("Wedone Operate | Version : Stable 4.0")
        version_label.setStyleSheet("font-size: 14px; color: black;")
        version_layout.addWidget(version_label)
        layout.addLayout(version_layout)

        # Licence
        license_label = QLabel('<a href="https://github.com/WedoneOfficiel/Wedone-Operate?tab=Apache-2.0-1-ov-file#readme">Licence Apache 2.0</a>')
        license_label.setOpenExternalLinks(True)
        license_label.setStyleSheet("font-size: 14px; color: blue;")
        layout.addWidget(license_label)

        # Copyright
        current_year = QDate.currentDate().year()
        copyright_label = QLabel(f"Copyright © 2022-{current_year}")
        copyright_label.setStyleSheet("font-size: 14px; color: black;")
        layout.addWidget(copyright_label)

        self.setLayout(layout)

    def create_options_section(self):  # Fonction pour créer la section "Options du logiciel"
        layout = QVBoxLayout(self.options_section)

        version_layout = QHBoxLayout()
        version_label = QLabel("Sélectionnez ici les types d'opérations que <br> vous souhaitez que l'on vous propose :")
        version_label.setStyleSheet("font-size: 14px; color: black;")
        version_layout.addWidget(version_label)
        layout.addLayout(version_layout)

        self.addition_checkbox = QCheckBox("Additions")
        self.addition_checkbox.setChecked(True)  # Sélectionnez par défaut
        self.addition_checkbox.stateChanged.connect(self.addition_changed)
        layout.addWidget(self.addition_checkbox)

        self.subtraction_checkbox = QCheckBox("Soustractions")
        self.subtraction_checkbox.setChecked(True)  # Sélectionnez par défaut
        self.subtraction_checkbox.stateChanged.connect(self.subtraction_changed)
        layout.addWidget(self.subtraction_checkbox)

        self.multiplication_checkbox = QCheckBox("Multiplications")
        self.multiplication_checkbox.setChecked(True)  # Sélectionnez par défaut
        self.multiplication_checkbox.stateChanged.connect(self.multiplication_changed)
        layout.addWidget(self.multiplication_checkbox)

        self.division_checkbox = QCheckBox("Divisions")
        self.division_checkbox.setChecked(True)  # Sélectionnez par défaut
        self.division_checkbox.stateChanged.connect(self.division_changed)
        layout.addWidget(self.division_checkbox)

    def auto_update_changed(self, state):
        print(f"Recherche automatique des mises à jour : {state == Qt.Checked}")

    def auto_patch_changed(self, state):
        print(f"Recherche automatique des patchs : {state == Qt.Checked}")

    def manual_update(self):
        print("Recherche manuelle des mises à jour...")

    def manual_patch(self):
        print("Recherche manuelle des patchs...")

    def addition_changed(self, state):
        print(f"Additions activées : {state == Qt.Checked}")
        self.save_settings()

    def subtraction_changed(self, state):
        print(f"Soustractions activées : {state == Qt.Checked}")
        self.save_settings()
    
    def multiplication_changed(self, state):
        print(f"Multiplications activées : {state == Qt.Checked}")
        self.save_settings()
    
    def division_changed(self, state):
        print(f"Divisions activées : {state == Qt.Checked}")
        self.save_settings()
    


    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.auto_update_check.setChecked(settings.get("auto_update", True))
                self.auto_patch_check.setChecked(settings.get("auto_patch", True))
                self.addition_checkbox.setChecked(settings.get("addition_enabled", True))
                self.subtraction_checkbox.setChecked(settings.get("subtraction_enabled", True))
                self.multiplication_checkbox.setChecked(settings.get("multiplication_enabled", True))
                self.division_checkbox.setChecked(settings.get("division_enabled", True))
        except FileNotFoundError:
            pass


    def save_settings(self):
        settings = {
            "auto_update": self.auto_update_check.isChecked(),
            "auto_patch": self.auto_patch_check.isChecked(),
            "addition_enabled": self.addition_checkbox.isChecked(),
            "subtraction_enabled": self.subtraction_checkbox.isChecked(),
            "multiplication_enabled": self.multiplication_checkbox.isChecked(),
            "division_enabled": self.division_checkbox.isChecked()
        }
        
        with open("settings.json", "w") as file:
            json.dump(settings, file)


    def closeEvent(self, event):
       self.save_settings()
       super().closeEvent(event)


    def auto_update_changed(self, state):
        print(f"Recherche automatique des mises à jour : {'activée' if state == Qt.Checked else 'désactivée'}")
        self.save_settings()

    def auto_patch_changed(self, state):
        if state == Qt.Unchecked:
            confirmation = ConfirmationDialog(self)
            if confirmation.exec_() == QDialog.Accepted:
                print("Recherche automatique des patchs désactivée.")
                self.save_settings()
            else:
                self.auto_patch_check.setChecked(True)  # Rétablir l'état précédent
        else:
            print("Recherche automatique des patchs activée.")
            self.save_settings()

    def manual_update(self):
        check_for_updates(True)

    def manual_patch(self):
        check_for_security_patches(True)

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)


class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")

        layout = QVBoxLayout(self)

        label = QLabel("Êtes-vous sûr de vouloir désactiver la recherche automatique des patchs ?")
        label.setStyleSheet("font-size: 14px; color: #0672BC;")
        layout.addWidget(label)

        explanation_label = QLabel("La recherche automatique des patchs joue un rôle essentiel dans la protection de votre système et du logiciel. <br/>Il est fortement recommandé de la conserver active pour garantir une sécurité optimale.")
        explanation_label.setStyleSheet("font-size: 13px; color: black;")
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)


        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ignore, Qt.Horizontal, self)
        layout.addWidget(button_box)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText(" Annuler ")
        ignore_button = button_box.button(QDialogButtonBox.Ignore)
        ignore_button.setText(" Continuer ")

        cancel_button.setStyleSheet("font-size: 15px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        ignore_button.setStyleSheet("font-size: 14px; background-color: #E7E3E3; color: #2b2b2b; font-weight: none; border: 1px solid #E7E3E3; border-radius: 5px;")

        cancel_button.clicked.connect(self.reject)
        ignore_button.clicked.connect(self.accept)

def check_for_updates(auto_update):
    if auto_update:
        version_url = "https://wedoneofficiel.github.io/Gestion-Mises-A-Jour/Wedone-Operate/version-wedone-operate.txt"

        try:
            response = requests.get(version_url)
            if response.status_code == 200:
                latest_version = response.text.strip()
                if float(latest_version) > 4.0:  # Comparaison en tant que nombre flottant
                    update_window = UpdateWindow(latest_version)
                    update_window.exec_()
        except requests.exceptions.RequestException:
            print("Impossible de récupérer la version la plus récente.")

def check_for_security_patches(auto_patch):
    if auto_patch:
        patch_url = "https://wedoneofficiel.github.io/Gestion-Mises-A-Jour/Wedone-Operate/Patchs/Stable_4-0.txt"

        try:
            response = requests.get(patch_url)
            if response.status_code == 200:
                patch_version = response.text.strip()
                if patch_version == "":
                    patch_version = "4.0"
                if patch_version != "4.0":
                    security_patch_window = SecurityPatchWindow(patch_version)
                    security_patch_window.exec_()
        except requests.exceptions.RequestException:
            print("Impossible de récupérer la version du patch de sécurité.")

class SecurityPatchWindow(QDialog):
    def __init__(self, latest_patch):
        super().__init__()
        self.setWindowTitle("Mise à jour de sécurité disponible")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: white; color: #2b2b2b;")

        layout = QVBoxLayout(self)

        label = QLabel(f"Un nouveau patch de sécurité est disponible pour Wedone Operate (version {latest_patch}) !\n\nIl est impératif de télécharger et d'installer ce patch pour garantir la sécurité et la stabilité de l'application.")
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        # Ajout d'un espace blanc entre les boutons Télécharger et Ignorer
        buttons_layout.addStretch()

        ignore_button = QPushButton(" Annuler ")
        ignore_button.clicked.connect(self.close)
        ignore_button.setStyleSheet("font-size: 14px; background-color: #E7E3E3; color: #2b2b2b; font-weight: bold; border: 1px solid #E7E3E3; border-radius: 5px;")
        buttons_layout.addWidget(ignore_button)

        download_button = QPushButton(" Ignorer ")
        download_button.clicked.connect(self.download_patch)
        download_button.setStyleSheet("font-size: 14px; background-color: #0672BC; color: white; font-weight: bold; border: 1px solid #0672BC; border-radius: 5px;")
        buttons_layout.addWidget(download_button)

        self.setLayout(layout)

    def download_patch(self):
        webbrowser.open("https://github.com/WedoneOfficiel/Wedone-Operate/releases")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    auto_update = False
    auto_patch = False

    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            auto_update = settings["auto_update"]
            auto_patch = settings["auto_patch"]
    except FileNotFoundError:
        pass

    if auto_update:
        check_for_updates(True)

    if auto_patch:
        check_for_security_patches(True)

    window = WedoneOperateApp()
    window.show()
    sys.exit(app.exec_())

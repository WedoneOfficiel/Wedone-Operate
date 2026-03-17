# ui/dialog_update.py — Wedone Operate
import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from constants import APP_VERSION


class UpdateDialog(QDialog):
    def __init__(self, update_info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mise à jour disponible")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumWidth(480)
        self._url = update_info.get("url", "")
        self._build_ui(update_info)

    def _build_ui(self, info: dict):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        title = QLabel("🆕  Mise à jour disponible")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        versions_layout = QHBoxLayout()
        cur_label = QLabel(f"Version actuelle\n{APP_VERSION}")
        cur_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cur_label.setObjectName("subtitle")

        arrow = QLabel("→")
        arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow.setStyleSheet("font-size: 20px;")

        new_label = QLabel(f"Nouvelle version\n{info['version']}")
        new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_label.setStyleSheet("font-weight: bold; color: #2EBD6E;")

        versions_layout.addWidget(cur_label)
        versions_layout.addWidget(arrow)
        versions_layout.addWidget(new_label)
        layout.addLayout(versions_layout)

        changelog_title = QLabel("Notes de version :")
        changelog_title.setStyleSheet("font-weight: bold;")
        layout.addWidget(changelog_title)

        changelog = QTextEdit()
        changelog.setReadOnly(True)
        changelog.setPlainText(info.get("changelog", "Aucune note disponible."))
        changelog.setMaximumHeight(160)
        layout.addWidget(changelog)

        btns = QHBoxLayout()
        ignore_btn = QPushButton("Ignorer")
        ignore_btn.setProperty("class", "secondary")
        ignore_btn.clicked.connect(self.reject)

        download_btn = QPushButton("⬇  Télécharger la mise à jour")
        download_btn.clicked.connect(self._download)

        btns.addWidget(ignore_btn)
        btns.addStretch()
        btns.addWidget(download_btn)
        layout.addLayout(btns)

    def _download(self):
        webbrowser.open(self._url)
        self.accept()

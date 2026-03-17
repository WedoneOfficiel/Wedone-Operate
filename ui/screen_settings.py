# ui/screen_settings.py — Wedone Operate
# Sections filtrées selon le rôle : élève ne voit que Apparence.
# Admin/prof voient aussi Mises à jour et gestion du mot de passe.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QComboBox, QFrame, QStackedWidget, QLineEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import settings as cfg
import database as db
import session
from constants import DIFFICULTY_LEVELS, APP_VERSION, APP_NAME


class SettingsScreen(QWidget):
    go_back       = pyqtSignal()
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = cfg.load()
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        nav = QWidget()
        nav.setFixedWidth(180)
        nav.setStyleSheet("border-right: 1px solid rgba(128,128,128,0.2);")
        nav_l = QVBoxLayout(nav)
        nav_l.setContentsMargins(12, 20, 12, 20)
        nav_l.setSpacing(6)
        nav_l.setAlignment(Qt.AlignmentFlag.AlignTop)

        nav_title = QLabel("Paramètres")
        nav_title.setStyleSheet("font-size: 15px; font-weight: bold; padding-bottom: 8px;")
        nav_l.addWidget(nav_title)

        self._nav_btns = []
        self._sections = [
            ("🎨  Apparence",    0, "all"),
            ("🔄  Mises à jour", 1, "staff"),
            ("🎯  Épreuves",     2, "all"),
            ("🔐  Mot de passe", 3, "staff"),
            ("ℹ️   À propos",    4, "all"),
        ]
        for label, idx, role in self._sections:
            btn = QPushButton(label)
            btn.setProperty("class", "nav")
            btn.clicked.connect(lambda _, i=idx: self._switch(i))
            nav_l.addWidget(btn)
            self._nav_btns.append((btn, role))

        nav_l.addStretch()
        back_btn = QPushButton("← Retour")
        back_btn.setProperty("class", "secondary")
        back_btn.clicked.connect(self.go_back)
        nav_l.addWidget(back_btn)
        root.addWidget(nav)

        # Stack
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_appearance())  # 0
        self.stack.addWidget(self._build_updates())     # 1
        self.stack.addWidget(self._build_epreuves())    # 2
        self.stack.addWidget(self._build_password())    # 3
        self.stack.addWidget(self._build_about())       # 4
        root.addWidget(self.stack)

    def _section_wrapper(self, title):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(30, 24, 30, 24)
        l.setSpacing(14)
        t = QLabel(title)
        t.setStyleSheet("font-size: 17px; font-weight: bold;")
        l.addWidget(t)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        l.addWidget(sep)
        return w, l

    def _build_appearance(self):
        w, l = self._section_wrapper("Apparence")
        l.addWidget(QLabel("Thème :"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Automatique (système)", "Clair", "Sombre"])
        self.theme_combo.setFixedWidth(220)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_change)
        l.addWidget(self.theme_combo)
        l.addStretch()
        return w

    def _build_updates(self):
        w, l = self._section_wrapper("Mises à jour")
        self.auto_update_cb = QCheckBox("Vérifier automatiquement au démarrage")
        self.auto_update_cb.stateChanged.connect(self._save)
        l.addWidget(self.auto_update_cb)
        btn = QPushButton("🔍 Vérifier maintenant")
        btn.setProperty("class", "secondary")
        btn.setFixedWidth(220)
        btn.clicked.connect(self._check_now)
        l.addWidget(btn)
        info = QLabel(f"Version actuelle : {APP_VERSION}")
        info.setObjectName("subtitle")
        l.addWidget(info)
        l.addStretch()
        return w

    def _build_epreuves(self):
        w, l = self._section_wrapper("Épreuves — Valeurs par défaut")
        l.addWidget(QLabel("Niveau par défaut :"))
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(DIFFICULTY_LEVELS)
        self.diff_combo.setFixedWidth(180)
        self.diff_combo.currentTextChanged.connect(self._save)
        l.addWidget(self.diff_combo)
        l.addWidget(QLabel("Opérations par défaut :"))
        self.cb_add = QCheckBox("Addition")
        self.cb_sub = QCheckBox("Soustraction")
        self.cb_mul = QCheckBox("Multiplication")
        self.cb_div = QCheckBox("Division")
        self.cb_timer_def = QCheckBox("Chronomètre activé par défaut")
        for cb in (self.cb_add, self.cb_sub, self.cb_mul, self.cb_div, self.cb_timer_def):
            cb.stateChanged.connect(self._save)
            l.addWidget(cb)
        l.addStretch()
        return w

    def _build_password(self):
        w, l = self._section_wrapper("Changer mon mot de passe")
        self.old_pwd  = QLineEdit(); self.old_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pwd.setPlaceholderText("Mot de passe actuel")
        self.new_pwd  = QLineEdit(); self.new_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pwd.setPlaceholderText("Nouveau mot de passe")
        self.new_pwd2 = QLineEdit(); self.new_pwd2.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pwd2.setPlaceholderText("Confirmer le nouveau mot de passe")
        self.pwd_err = QLabel(""); self.pwd_err.setObjectName("error"); self.pwd_err.hide()
        for widget in (self.old_pwd, self.new_pwd, self.new_pwd2, self.pwd_err):
            l.addWidget(widget)
        btn = QPushButton("Modifier le mot de passe")
        btn.setFixedWidth(220)
        btn.clicked.connect(self._change_password)
        l.addWidget(btn)
        l.addStretch()
        return w

    def _build_about(self):
        w, l = self._section_wrapper("À propos")
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import QDate
        icon_lbl = QLabel()
        pix = QPixmap("icon.png")
        if not pix.isNull():
            icon_lbl.setPixmap(pix.scaledToWidth(56, Qt.TransformationMode.SmoothTransformation))
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.addWidget(icon_lbl)
        for text in [
            f"<b>{APP_NAME}</b>",
            f"Version : {APP_VERSION}",
            f"© 2022–{QDate.currentDate().year()} WedoneOfficiel",
            '<a href="https://github.com/WedoneOfficiel/Wedone-Operate/blob/main/LICENSE">Licence Apache 2.0</a>',
        ]:
            lbl = QLabel(text); lbl.setOpenExternalLinks(True)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.addWidget(lbl)
        l.addStretch()
        return w

    # ── Navigation ─────────────────────────────────────────────────────

    def _switch(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, (btn, _) in enumerate(self._nav_btns):
            btn.setProperty("class", "nav-active" if i == idx else "nav")
            btn.style().unpolish(btn); btn.style().polish(btn)

    def refresh(self):
        """Masquer les sections réservées au staff selon le rôle."""
        s = session.current
        is_staff = s.can_see_updates()
        for i, (btn, role) in enumerate(self._nav_btns):
            btn.setVisible(role == "all" or is_staff)
        self._load_values()
        self._switch(0)

    # ── Données ────────────────────────────────────────────────────────

    def _load_values(self):
        s = self._settings
        theme_map = {"system": 0, "light": 1, "dark": 2}
        self.theme_combo.setCurrentIndex(theme_map.get(s.get("theme", "system"), 0))
        self.auto_update_cb.setChecked(s.get("auto_update", True))
        diff = s.get("difficulty", "Moyen")
        if diff in DIFFICULTY_LEVELS:
            self.diff_combo.setCurrentText(diff)
        self.cb_add.setChecked(s.get("addition_enabled", True))
        self.cb_sub.setChecked(s.get("subtraction_enabled", True))
        self.cb_mul.setChecked(s.get("multiplication_enabled", True))
        self.cb_div.setChecked(s.get("division_enabled", True))
        self.cb_timer_def.setChecked(s.get("timer_enabled", False))

    def _save(self):
        theme_map = {0: "system", 1: "light", 2: "dark"}
        self._settings["theme"]                  = theme_map[self.theme_combo.currentIndex()]
        self._settings["auto_update"]            = self.auto_update_cb.isChecked()
        self._settings["difficulty"]             = self.diff_combo.currentText()
        self._settings["addition_enabled"]       = self.cb_add.isChecked()
        self._settings["subtraction_enabled"]    = self.cb_sub.isChecked()
        self._settings["multiplication_enabled"] = self.cb_mul.isChecked()
        self._settings["division_enabled"]       = self.cb_div.isChecked()
        self._settings["timer_enabled"]          = self.cb_timer_def.isChecked()
        cfg.save(self._settings)

    def _on_theme_change(self, _):
        self._save()
        theme_map = {0: "system", 1: "light", 2: "dark"}
        raw = theme_map[self.theme_combo.currentIndex()]
        effective = cfg.resolve_theme({"theme": raw})
        self.theme_changed.emit(effective)

    def _check_now(self):
        from updater import check_for_update
        result = check_for_update()
        if result:
            from ui.dialog_update import UpdateDialog
            UpdateDialog(result, self).exec()
        else:
            QMessageBox.information(self, "Mises à jour", f"{APP_NAME} {APP_VERSION} est à jour !")

    def _change_password(self):
        old, new, new2 = self.old_pwd.text(), self.new_pwd.text(), self.new_pwd2.text()
        s = session.current
        if s.is_admin():
            ok = db.check_admin_password(old)
        else:
            ok = db.check_teacher_password(s.user_id, old)
        if not ok:
            self.pwd_err.setText("Mot de passe actuel incorrect."); self.pwd_err.show(); return
        if len(new) < 6:
            self.pwd_err.setText("Minimum 6 caractères."); self.pwd_err.show(); return
        if new != new2:
            self.pwd_err.setText("Les mots de passe ne correspondent pas."); self.pwd_err.show(); return
        if s.is_admin():
            db.set_admin_password(new)
        else:
            db.set_teacher_password(s.user_id, new)
        self.pwd_err.hide()
        for f in (self.old_pwd, self.new_pwd, self.new_pwd2):
            f.clear()
        QMessageBox.information(self, "Succès", "Mot de passe modifié.")

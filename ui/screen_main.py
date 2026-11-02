# ui/screen_main.py — Wedone Operate
# Pour les élèves uniquement (admin/prof → dashboard).
# Pré-remplit depuis le modèle du groupe si disponible.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QCheckBox, QFrame, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
import session, database as db
from constants import SCHOOL_LEVELS, TIMER_SECONDS_BY_LEVEL, LEVEL_RANGES


class MainScreen(QWidget):
    session_ready = pyqtSignal(dict)
    open_settings = pyqtSignal()
    open_stats    = pyqtSignal()
    logout        = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings_defaults = {}
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(18)

        header = QHBoxLayout()
        identity = QVBoxLayout()
        identity.setSpacing(3)
        self.welcome_lbl = QLabel("Bienvenue !")
        self.welcome_lbl.setObjectName("title")
        self.info_lbl = QLabel("")
        self.info_lbl.setObjectName("subtitle")
        identity.addWidget(self.welcome_lbl)
        identity.addWidget(self.info_lbl)
        header.addLayout(identity)
        header.addStretch()

        for label, signal in [
            ("Statistiques", self.open_stats),
            ("Paramètres", self.open_settings),
            ("Déconnexion", self.logout),
        ]:
            button = QPushButton(label)
            button.setProperty("class", "secondary")
            button.clicked.connect(signal)
            header.addWidget(button)
        root.addLayout(header)

        self.template_banner = QFrame()
        self.template_banner.setProperty("class", "card-compact")
        banner_layout = QHBoxLayout(self.template_banner)
        banner_layout.setContentsMargins(14, 10, 14, 10)
        self.template_lbl = QLabel("")
        self.template_lbl.setWordWrap(True)
        banner_layout.addWidget(self.template_lbl)
        self.template_banner.hide()
        root.addWidget(self.template_banner)

        content = QHBoxLayout()
        content.setSpacing(16)

        config_card = QFrame()
        config_card.setProperty("class", "card")
        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(20, 20, 20, 20)
        config_layout.setSpacing(14)

        section = QLabel("Préparer une session")
        section.setObjectName("section")
        config_layout.addWidget(section)
        intro = QLabel("Choisissez un niveau et les opérations à travailler.")
        intro.setObjectName("subtitle")
        intro.setWordWrap(True)
        config_layout.addWidget(intro)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)
        form.addWidget(QLabel("Nombre d'épreuves"), 0, 0)
        self.spin = QSpinBox()
        self.spin.setRange(1, 100)
        self.spin.setValue(10)
        self.spin.setMinimumWidth(110)
        form.addWidget(self.spin, 0, 1)
        form.addWidget(QLabel("Niveau scolaire"), 1, 0)
        self.combo_level = QComboBox()
        self.combo_level.addItems(SCHOOL_LEVELS)
        self.combo_level.setCurrentText("CM2")
        self.combo_level.setMinimumWidth(130)
        self.combo_level.currentTextChanged.connect(self._on_level_changed)
        form.addWidget(self.combo_level, 1, 1)
        config_layout.addLayout(form)

        ops_title = QLabel("Opérations")
        ops_title.setStyleSheet("font-weight:700;")
        config_layout.addWidget(ops_title)
        ops_box = QFrame()
        ops_box.setObjectName("opsBox")
        ops_layout = QGridLayout(ops_box)
        ops_layout.setContentsMargins(14, 12, 14, 12)
        ops_layout.setHorizontalSpacing(18)
        ops_layout.setVerticalSpacing(12)
        self.cb_add = QCheckBox("Addition")
        self.cb_sub = QCheckBox("Soustraction")
        self.cb_mul = QCheckBox("Multiplication")
        self.cb_div = QCheckBox("Division")
        for checkbox in (self.cb_add, self.cb_sub, self.cb_mul, self.cb_div):
            checkbox.setChecked(True)
        ops_layout.addWidget(self.cb_add, 0, 0)
        ops_layout.addWidget(self.cb_sub, 0, 1)
        ops_layout.addWidget(self.cb_mul, 1, 0)
        ops_layout.addWidget(self.cb_div, 1, 1)
        config_layout.addWidget(ops_box)

        timer_row = QHBoxLayout()
        self.cb_timer = QCheckBox("Activer le chronomètre")
        self.cb_timer.stateChanged.connect(self._update_timer_info)
        self.timer_info = QLabel("")
        self.timer_info.setObjectName("subtitle")
        timer_row.addWidget(self.cb_timer)
        timer_row.addStretch()
        timer_row.addWidget(self.timer_info)
        config_layout.addLayout(timer_row)
        content.addWidget(config_card, stretch=3)

        guide_card = QFrame()
        guide_card.setProperty("class", "card")
        guide_layout = QVBoxLayout(guide_card)
        guide_layout.setContentsMargins(20, 20, 20, 20)
        guide_layout.setSpacing(12)
        guide_title = QLabel("Un entraînement utile")
        guide_title.setObjectName("section")
        guide_layout.addWidget(guide_title)
        guide_copy = QLabel(
            "Commencez sans pression. Les opérations non adaptées au niveau choisi "
            "sont automatiquement désactivées."
        )
        guide_copy.setWordWrap(True)
        guide_copy.setObjectName("subtitle")
        guide_layout.addWidget(guide_copy)
        guide_layout.addSpacing(6)
        for heading, detail in [
            ("1. S'entraîner", "Des questions générées à chaque session."),
            ("2. Comprendre", "La correction s'affiche après chaque réponse."),
            ("3. Progresser", "Les résultats sont conservés pour les profils élèves."),
        ]:
            item_title = QLabel(heading)
            item_title.setStyleSheet("font-weight:700;")
            item_detail = QLabel(detail)
            item_detail.setObjectName("subtitle")
            item_detail.setWordWrap(True)
            guide_layout.addWidget(item_title)
            guide_layout.addWidget(item_detail)
        guide_layout.addStretch()
        content.addWidget(guide_card, stretch=2)
        root.addLayout(content, stretch=1)

        self.start_btn = QPushButton("Commencer la session")
        self.start_btn.setFixedHeight(48)
        self.start_btn.clicked.connect(self._on_start)
        root.addWidget(self.start_btn)

    def refresh(self):
        s = session.current
        self.welcome_lbl.setText(f"Bonjour, {s.display_name()} !")

        # Niveau du groupe
        legacy_levels = {"Facile": "CE1", "Moyen": "CM2", "Difficile": "3e"}
        guest_level = legacy_levels.get(
            self._settings_defaults.get("difficulty"),
            self._settings_defaults.get("difficulty", "CM2")
        )
        if guest_level not in SCHOOL_LEVELS:
            guest_level = "CM2"
        student_level = db.get_student_level(s.user_id) if s.is_student() and s.user_id else guest_level
        student = db.get_student(s.user_id) if s.is_student() and s.user_id else None
        group = db.get_group(student.get("group_id")) if student and student.get("group_id") else None
        cls = db.get_class(student.get("class_id")) if student and student.get("class_id") else None
        if group:
            placement = f"Groupe : {group['name']}"
        elif cls:
            placement = f"Classe : {cls['name']}"
        else:
            placement = "Mode invité" if s.is_guest() else "Élève"
        self.info_lbl.setText(f"{placement}  ·  Niveau {student_level}")

        self.combo_level.setCurrentText(student_level)

        # Group-specific assignment wins; otherwise use the class-wide assignment.
        template = db.get_student_default_template(s.user_id) if student else None
        if template:
            self.template_lbl.setText(
                f"📋 Votre prof a configuré : « {template['name']} » — "
                "vous pouvez modifier les options ci-dessous."
            )
            self.template_banner.show()
            self._apply_template(template["config"])
        else:
            self.template_banner.hide()
            self._apply_defaults(student_level)

        self._update_available_operations()
        self._update_timer_info()

    def _apply_template(self, config: dict):
        level = config.get("level", "CM2")
        if level in SCHOOL_LEVELS: self.combo_level.setCurrentText(level)
        self.spin.setValue(config.get("nb_epreuves", 10))
        ops = config.get("operations", ["addition","soustraction"])
        self.cb_add.setChecked("addition"       in ops)
        self.cb_sub.setChecked("soustraction"   in ops)
        self.cb_mul.setChecked("multiplication" in ops)
        self.cb_div.setChecked("division"       in ops)
        self.cb_timer.setChecked(config.get("timer_enabled", False))
        self._update_available_operations()

    def _apply_defaults(self, level: str):
        if level in SCHOOL_LEVELS: self.combo_level.setCurrentText(level)
        defaults = self._settings_defaults
        self.spin.setValue(10)
        self.cb_add.setChecked(defaults.get("addition_enabled", True))
        self.cb_sub.setChecked(defaults.get("subtraction_enabled", True))
        self.cb_mul.setChecked(defaults.get("multiplication_enabled", True))
        self.cb_div.setChecked(defaults.get("division_enabled", True))
        self.cb_timer.setChecked(defaults.get("timer_enabled", False))
        self._update_available_operations()

    def load_settings_defaults(self, settings: dict):
        """Apply persisted defaults to guest practice and as student fallbacks."""
        self._settings_defaults = dict(settings or {})

    def _on_level_changed(self, _value=None):
        self._update_available_operations()
        self._update_timer_info()

    def _update_available_operations(self):
        available = set(LEVEL_RANGES.get(self.combo_level.currentText(), {}))
        controls = (
            (self.cb_add, "addition"),
            (self.cb_sub, "soustraction"),
            (self.cb_mul, "multiplication"),
            (self.cb_div, "division"),
        )
        for checkbox, operation in controls:
            enabled = operation in available
            checkbox.setEnabled(enabled)
            if not enabled:
                checkbox.setChecked(False)

    def _update_timer_info(self):
        if self.cb_timer.isChecked():
            level = self.combo_level.currentText()
            secs  = TIMER_SECONDS_BY_LEVEL.get(level, 20)
            self.timer_info.setText(f"— {secs} s par épreuve")
        else:
            self.timer_info.setText("")

    def _on_start(self):
        ops = []
        if self.cb_add.isChecked(): ops.append("addition")
        if self.cb_sub.isChecked(): ops.append("soustraction")
        if self.cb_mul.isChecked(): ops.append("multiplication")
        if self.cb_div.isChecked(): ops.append("division")
        if not ops:
            QMessageBox.warning(self, "Attention", "Sélectionne au moins une opération."); return
        s = session.current
        self.session_ready.emit({
            "student_id":    s.user_id,
            "student_name":  s.display_name(),
            "nb_epreuves":   self.spin.value(),
            "difficulty":    self.combo_level.currentText(),
            "operations":    ops,
            "timer_enabled": self.cb_timer.isChecked(),
        })

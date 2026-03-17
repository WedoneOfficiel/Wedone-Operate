# ui/screen_main.py — Wedone Operate
# Pour les élèves uniquement (admin/prof → dashboard).
# Pré-remplit depuis le modèle du groupe si disponible.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QCheckBox, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import session, database as db
from constants import SCHOOL_LEVELS, TIMER_SECONDS_BY_LEVEL


class MainScreen(QWidget):
    session_ready = pyqtSignal(dict)
    open_settings = pyqtSignal()
    open_stats    = pyqtSignal()
    logout        = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 28, 40, 28); root.setSpacing(18)

        header = QHBoxLayout()
        left = QVBoxLayout(); left.setSpacing(2)
        self.welcome_lbl = QLabel("Bienvenue !")
        self.welcome_lbl.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.info_lbl = QLabel("")
        self.info_lbl.setObjectName("subtitle")
        left.addWidget(self.welcome_lbl); left.addWidget(self.info_lbl)
        header.addLayout(left); header.addStretch()

        for label, signal in [("📊 Stats", self.open_stats),
                               ("⚙ Paramètres", self.open_settings),
                               ("⬅ Déconnexion", self.logout)]:
            btn = QPushButton(label); btn.setProperty("class", "secondary")
            btn.clicked.connect(signal); header.addWidget(btn)
        root.addLayout(header)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); root.addWidget(sep)

        # Bandeau modèle assigné par le prof
        self.template_banner = QFrame()
        self.template_banner.setStyleSheet(
            "QFrame{background:#EBF4FC;border:1px solid #A8D0F0;border-radius:8px;}"
        )
        tb_l = QHBoxLayout(self.template_banner); tb_l.setContentsMargins(12,8,12,8)
        self.template_lbl = QLabel("")
        self.template_lbl.setStyleSheet("color:#0558A0;font-size:13px;background:transparent;border:none;")
        tb_l.addWidget(self.template_lbl); tb_l.addStretch()
        self.template_banner.hide()
        root.addWidget(self.template_banner)

        section = QLabel("Configurer ta session")
        section.setStyleSheet("font-size: 16px; font-weight: bold;")
        root.addWidget(section)

        # Nb épreuves
        row1 = QHBoxLayout(); row1.addWidget(QLabel("Nombre d'épreuves :"))
        self.spin = QSpinBox(); self.spin.setMinimum(1); self.spin.setMaximum(100)
        self.spin.setValue(10); self.spin.setFixedWidth(80)
        row1.addWidget(self.spin); row1.addStretch(); root.addLayout(row1)

        # Niveau scolaire (pré-rempli depuis le groupe)
        row2 = QHBoxLayout(); row2.addWidget(QLabel("Niveau :"))
        self.combo_level = QComboBox(); self.combo_level.addItems(SCHOOL_LEVELS)
        self.combo_level.setCurrentText("CM2"); self.combo_level.setFixedWidth(120)
        self.combo_level.currentTextChanged.connect(self._update_timer_info)
        row2.addWidget(self.combo_level); row2.addStretch(); root.addLayout(row2)

        # Opérations
        ops_box = QFrame(); ops_box.setObjectName("opsBox")
        ops_l = QHBoxLayout(ops_box); ops_l.setContentsMargins(12,10,12,10)
        self.cb_add = QCheckBox("Addition"); self.cb_sub = QCheckBox("Soustraction")
        self.cb_mul = QCheckBox("Multiplication"); self.cb_div = QCheckBox("Division")
        for cb in (self.cb_add, self.cb_sub, self.cb_mul, self.cb_div):
            cb.setChecked(True); ops_l.addWidget(cb)
        ops_l.addStretch(); root.addWidget(ops_box)

        # Chrono
        chrono_row = QHBoxLayout()
        self.cb_timer = QCheckBox("Session chronométrée")
        self.cb_timer.stateChanged.connect(self._update_timer_info)
        self.timer_info = QLabel(""); self.timer_info.setObjectName("subtitle")
        chrono_row.addWidget(self.cb_timer); chrono_row.addWidget(self.timer_info)
        chrono_row.addStretch(); root.addLayout(chrono_row)

        root.addStretch()
        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine); root.addWidget(sep2)

        self.start_btn = QPushButton("▶  Commencer la session")
        self.start_btn.setFixedHeight(46)
        self.start_btn.setStyleSheet("font-size: 16px;")
        self.start_btn.clicked.connect(self._on_start)
        root.addWidget(self.start_btn)

    def refresh(self):
        s = session.current
        self.welcome_lbl.setText(f"Bonjour, {s.display_name()} !")

        # Niveau du groupe
        student_level = db.get_student_level(s.user_id) if s.user_id else "CM2"
        g = db.get_group(db.get_student(s.user_id).get("group_id")) if s.user_id and db.get_student(s.user_id) else None
        group_name = g["name"] if g else ""
        self.info_lbl.setText(f"Groupe : {group_name}  •  Niveau {student_level}" if group_name else f"Niveau {student_level}")

        self.combo_level.setCurrentText(student_level)

        # Modèle assigné par le prof
        group_id = db.get_student(s.user_id).get("group_id") if s.user_id and db.get_student(s.user_id) else None
        template = db.get_group_default_template(group_id) if group_id else None
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

    def _apply_defaults(self, level: str):
        if level in SCHOOL_LEVELS: self.combo_level.setCurrentText(level)
        self.spin.setValue(10)
        for cb in (self.cb_add, self.cb_sub, self.cb_mul, self.cb_div): cb.setChecked(True)
        self.cb_timer.setChecked(False)

    def load_settings_defaults(self, settings: dict):
        pass  # Les defaults viennent du groupe/modèle, pas des settings globaux

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

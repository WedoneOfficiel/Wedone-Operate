# ui/screen_login.py — Wedone Operate
# Connexion en 3 étapes pour les élèves : Classe → Groupe → Profil

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QScrollArea, QStackedWidget, QComboBox,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import database as db
import session
from constants import DEFAULT_ADMIN_PASSWORD_PLAIN


class LoginScreen(QWidget):
    logged_in = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addStretch(1)

        center = QVBoxLayout()
        center.setContentsMargins(80, 0, 80, 0)
        center.setSpacing(0)

        # Logo + titre
        logo_row = QHBoxLayout()
        logo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_lbl = QLabel()
        pix = QPixmap("icon.png")
        if not pix.isNull():
            logo_lbl.setPixmap(pix.scaledToWidth(64, Qt.TransformationMode.SmoothTransformation))
        logo_row.addWidget(logo_lbl)
        center.addLayout(logo_row)
        center.addSpacing(12)

        title = QLabel("Wedone Operate")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        center.addWidget(title)
        sub = QLabel("Entraînement au calcul mental")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setObjectName("subtitle")
        center.addWidget(sub)
        center.addSpacing(28)

        # Onglets
        tabs_row = QHBoxLayout(); tabs_row.setSpacing(0)
        self._tab_btns = []
        for i, label in enumerate(["Admin", "Professeur", "Élève"]):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("class", "tab")
            btn.clicked.connect(lambda _, idx=i: self._switch_tab(idx))
            self._tab_btns.append(btn)
            tabs_row.addWidget(btn)
        center.addLayout(tabs_row)

        self.stack = QStackedWidget()
        self.stack.setMinimumHeight(280)
        self.stack.addWidget(self._build_admin_panel())    # 0
        self.stack.addWidget(self._build_teacher_panel())  # 1
        self.stack.addWidget(self._build_student_panel())  # 2
        center.addWidget(self.stack)

        root.addLayout(center)
        root.addStretch(1)
        self._switch_tab(2)

    # ── Panneaux ──────────────────────────────────────────────────────

    def _build_admin_panel(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 18, 0, 0); l.setSpacing(10)

        self.admin_hint = QFrame()
        self.admin_hint.setStyleSheet(
            "QFrame{background:#FFF8E1;border:1px solid #F0A030;border-radius:6px;}"
        )
        hl = QVBoxLayout(self.admin_hint)
        hl.setContentsMargins(10, 8, 10, 8); hl.setSpacing(2)
        h1 = QLabel(f"🔑  Mot de passe par défaut : <b>{DEFAULT_ADMIN_PASSWORD_PLAIN}</b>")
        h1.setStyleSheet("color:#7A5500;font-size:13px;background:transparent;border:none;")
        h2 = QLabel("Nous vous invitons à le modifier après la première connexion.")
        h2.setStyleSheet("color:#9A6600;font-size:12px;background:transparent;border:none;")
        hl.addWidget(h1); hl.addWidget(h2)
        l.addWidget(self.admin_hint)

        self.admin_pwd = QLineEdit()
        self.admin_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_pwd.setPlaceholderText("Mot de passe administrateur")
        self.admin_pwd.returnPressed.connect(self._login_admin)
        l.addWidget(self.admin_pwd)
        self.admin_err = QLabel(""); self.admin_err.setObjectName("error"); self.admin_err.hide()
        l.addWidget(self.admin_err)
        btn = QPushButton("Se connecter"); btn.setFixedHeight(40)
        btn.clicked.connect(self._login_admin)
        l.addWidget(btn); l.addStretch()
        return w

    def _build_teacher_panel(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 18, 0, 0); l.setSpacing(10)
        l.addWidget(QLabel("Sélectionnez votre compte :"))
        self.teacher_combo = QComboBox(); self.teacher_combo.setFixedHeight(38)
        l.addWidget(self.teacher_combo)
        self.teacher_pwd = QLineEdit()
        self.teacher_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.teacher_pwd.setPlaceholderText("Mot de passe")
        self.teacher_pwd.returnPressed.connect(self._login_teacher)
        l.addWidget(self.teacher_pwd)
        self.teacher_err = QLabel(""); self.teacher_err.setObjectName("error"); self.teacher_err.hide()
        l.addWidget(self.teacher_err)
        btn = QPushButton("Se connecter"); btn.setFixedHeight(40)
        btn.clicked.connect(self._login_teacher)
        l.addWidget(btn); l.addStretch()
        return w

    def _build_student_panel(self):
        """Sélection en 3 étapes : Classe → Groupe → Profil"""
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 14, 0, 0); l.setSpacing(10)

        # Fil d'Ariane
        self.breadcrumb = QLabel("Sélectionnez votre classe")
        self.breadcrumb.setObjectName("subtitle")
        self.breadcrumb.setStyleSheet("font-size: 13px;")
        l.addWidget(self.breadcrumb)

        # Stack des 3 étapes
        self.student_stack = QStackedWidget()
        self.student_stack.addWidget(self._build_class_step())   # 0
        self.student_stack.addWidget(self._build_group_step())   # 1
        self.student_stack.addWidget(self._build_profile_step()) # 2
        l.addWidget(self.student_stack)

        # Bouton retour
        self.back_step_btn = QPushButton("← Retour")
        self.back_step_btn.setProperty("class", "secondary")
        self.back_step_btn.setFixedWidth(100)
        self.back_step_btn.clicked.connect(self._step_back)
        self.back_step_btn.hide()
        l.addWidget(self.back_step_btn)
        return w

    def _build_class_step(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0); l.setSpacing(8)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.class_cards_w = QWidget()
        self.class_cards_l = QHBoxLayout(self.class_cards_w)
        self.class_cards_l.setSpacing(10)
        self.class_cards_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        scroll.setWidget(self.class_cards_w)
        l.addWidget(scroll)
        self.no_class_lbl = QLabel("Aucune classe disponible.")
        self.no_class_lbl.setObjectName("subtitle")
        self.no_class_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_class_lbl.hide()
        l.addWidget(self.no_class_lbl)
        return w

    def _build_group_step(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0); l.setSpacing(8)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.group_cards_w = QWidget()
        self.group_cards_l = QHBoxLayout(self.group_cards_w)
        self.group_cards_l.setSpacing(10)
        self.group_cards_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        scroll.setWidget(self.group_cards_w)
        l.addWidget(scroll)
        self.no_group_lbl = QLabel("Aucun groupe dans cette classe.")
        self.no_group_lbl.setObjectName("subtitle")
        self.no_group_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_group_lbl.hide()
        l.addWidget(self.no_group_lbl)
        return w

    def _build_profile_step(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0); l.setSpacing(8)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.profile_cards_w = QWidget()
        self.profile_cards_l = QHBoxLayout(self.profile_cards_w)
        self.profile_cards_l.setSpacing(10)
        self.profile_cards_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        scroll.setWidget(self.profile_cards_w)
        l.addWidget(scroll)
        self.no_profile_lbl = QLabel("Aucun élève dans ce groupe.")
        self.no_profile_lbl.setObjectName("subtitle")
        self.no_profile_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_profile_lbl.hide()
        l.addWidget(self.no_profile_lbl)
        return w

    # ── Navigation étapes élève ───────────────────────────────────────

    def _go_step(self, idx: int, crumb: str):
        self.student_stack.setCurrentIndex(idx)
        self.breadcrumb.setText(crumb)
        self.back_step_btn.setVisible(idx > 0)

    def _step_back(self):
        idx = self.student_stack.currentIndex()
        if idx == 1:
            self._go_step(0, "Sélectionnez votre classe")
        elif idx == 2:
            self._go_step(1, f"Classe : {self._selected_class['name']}  —  Sélectionnez votre groupe")

    def _on_class_selected(self, cls: dict):
        self._selected_class = cls
        self._refresh_group_cards(cls["id"])
        self._go_step(1, f"Classe : {cls['name']}  —  Sélectionnez votre groupe")

    def _on_group_selected(self, grp: dict):
        self._selected_group = grp
        level = grp.get("level", "")
        level_str = f" ({level})" if level else ""
        self._refresh_profile_cards(grp["id"])
        self._go_step(2, f"{self._selected_class['name']}  ›  {grp['name']}{level_str}  —  Qui êtes-vous ?")

    # ── Refresh cards ─────────────────────────────────────────────────

    def _refresh_class_cards(self):
        self._clear_layout(self.class_cards_l)
        classes = db.get_classes()
        if not classes:
            self.no_class_lbl.show(); return
        self.no_class_lbl.hide()
        for cls in classes:
            nb = len(db.get_groups(class_id=cls["id"]))
            card = self._make_icon_card(
                initiales=cls["name"][:2].upper(),
                label=cls["name"],
                sublabel=f"{nb} groupe{'s' if nb > 1 else ''}",
                color="#0672BC",
                size=(110, 100),
                on_click=lambda _, c=cls: self._on_class_selected(c)
            )
            self.class_cards_l.addWidget(card)

    def _refresh_group_cards(self, class_id: str):
        self._clear_layout(self.group_cards_l)
        groups = db.get_groups(class_id=class_id)
        if not groups:
            self.no_group_lbl.show(); return
        self.no_group_lbl.hide()
        for grp in groups:
            nb = len(db.get_students(group_id=grp["id"]))
            level = grp.get("level", "")
            card = self._make_icon_card(
                initiales=grp["name"][:2].upper(),
                label=grp["name"],
                sublabel=level,
                color="#0F6E56",
                size=(110, 100),
                on_click=lambda _, g=grp: self._on_group_selected(g)
            )
            self.group_cards_l.addWidget(card)

    def _refresh_profile_cards(self, group_id: str):
        self._clear_layout(self.profile_cards_l)
        students = db.get_students(group_id=group_id)
        if not students:
            self.no_profile_lbl.show(); return
        self.no_profile_lbl.hide()
        for s in students:
            initiales = f"{s['prenom'][0]}{s['nom'][0]}".upper()
            card = self._make_icon_card(
                initiales=initiales,
                label=s["prenom"],
                sublabel=s["nom"],
                color="#534AB7",
                size=(100, 95),
                on_click=lambda _, st=s: self._login_student(st)
            )
            self.profile_cards_l.addWidget(card)

    def _make_icon_card(self, initiales, label, sublabel, color, size, on_click) -> QWidget:
        card = QPushButton()
        card.setFixedSize(*size)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"""
            QPushButton {{
                background:#F4F6F9; border:1.5px solid #DDE3EC;
                border-radius:10px; font-size:12px;
            }}
            QPushButton:hover {{ border-color:{color}; background:#EBF4FC; }}
            QPushButton:pressed {{ background:#D6EAF8; }}
        """)
        inner = QVBoxLayout(card)
        inner.setContentsMargins(4, 8, 4, 6); inner.setSpacing(3)

        badge = QLabel(initiales)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedSize(38, 38)
        badge.setStyleSheet(f"background:{color};color:white;border-radius:19px;"
                            "font-size:13px;font-weight:bold;")
        br = QHBoxLayout(); br.setAlignment(Qt.AlignmentFlag.AlignCenter); br.addWidget(badge)

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size:12px;font-weight:bold;background:transparent;")

        sub = QLabel(sublabel)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet("font-size:11px;color:#5A6270;background:transparent;")

        inner.addLayout(br); inner.addWidget(lbl); inner.addWidget(sub)
        card.clicked.connect(on_click)
        return card

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    # ── Switching tabs ────────────────────────────────────────────────

    def _switch_tab(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._tab_btns): btn.setChecked(i == idx)
        if idx == 0: self.admin_hint.setVisible(db.is_admin_first_login())
        elif idx == 1: self._refresh_teacher_combo()
        elif idx == 2:
            self._go_step(0, "Sélectionnez votre classe")
            self._refresh_class_cards()

    def refresh(self):
        self._switch_tab(self.stack.currentIndex())

    def _refresh_teacher_combo(self):
        self.teacher_combo.clear()
        for t in db.get_teachers():
            self.teacher_combo.addItem(f"{t['prenom']} {t['nom']}", userData=t)

    # ── Authentification ──────────────────────────────────────────────

    def _login_admin(self):
        if not db.check_admin_password(self.admin_pwd.text()):
            self.admin_err.setText("Mot de passe incorrect."); self.admin_err.show()
            self.admin_pwd.clear(); return
        self.admin_err.hide(); self.admin_pwd.clear()
        db.mark_admin_logged_in(); session.login_admin(); self.logged_in.emit()

    def _login_teacher(self):
        idx = self.teacher_combo.currentIndex()
        if idx < 0:
            self.teacher_err.setText("Aucun compte disponible."); self.teacher_err.show(); return
        teacher = self.teacher_combo.itemData(idx)
        if not db.check_teacher_password(teacher["id"], self.teacher_pwd.text()):
            self.teacher_err.setText("Mot de passe incorrect."); self.teacher_err.show()
            self.teacher_pwd.clear(); return
        self.teacher_err.hide(); self.teacher_pwd.clear()
        session.login_teacher(teacher); self.logged_in.emit()

    def _login_student(self, student: dict):
        session.login_student(student); self.logged_in.emit()

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
from ui.resources import resource_path


class LoginScreen(QWidget):
    logged_in = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(34, 30, 34, 30)
        root.setSpacing(28)

        # Brand panel: clear introduction and product identity.
        hero = QWidget()
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(8, 12, 8, 12)
        hero_layout.setSpacing(16)
        hero_layout.addStretch(1)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        pix = QPixmap(resource_path("icon.png"))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToWidth(72, Qt.TransformationMode.SmoothTransformation))
        hero_layout.addWidget(logo)

        eyebrow = QLabel("WEDONE  /  APPRENTISSAGE")
        eyebrow.setObjectName("subtitle")
        eyebrow.setStyleSheet("font-size:11px;font-weight:800;letter-spacing:1.5px;")
        hero_layout.addWidget(eyebrow)

        brand = QLabel("Wedone Operate")
        brand.setObjectName("title")
        brand.setStyleSheet("font-size:30px;")
        hero_layout.addWidget(brand)

        headline = QLabel("Le calcul mental,\nà votre rythme.")
        headline.setWordWrap(True)
        headline.setStyleSheet("font-family:'Manrope';font-size:27px;font-weight:800;")
        hero_layout.addWidget(headline)

        description = QLabel(
            "Des entraînements clairs et progressifs, pour s'exercer seul ou suivre "
            "le travail de plusieurs classes."
        )
        description.setObjectName("subtitle")
        description.setWordWrap(True)
        description.setMaximumWidth(360)
        hero_layout.addWidget(description)

        hero_layout.addSpacing(12)
        for label in ("✓  Utilisation locale", "✓  Aucun compte obligatoire", "✓  Groupes facultatifs"):
            item = QLabel(label)
            item.setStyleSheet("font-size:13px;font-weight:600;")
            hero_layout.addWidget(item)
        hero_layout.addStretch(2)
        root.addWidget(hero, stretch=1)

        # Access panel: all entry modes share one consistent surface.
        panel = QFrame()
        panel.setProperty("class", "card")
        panel.setMinimumWidth(390)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(12)

        panel_title = QLabel("Accéder à l'application")
        panel_title.setObjectName("section")
        panel_layout.addWidget(panel_title)
        panel_subtitle = QLabel("Choisissez votre mode d'utilisation.")
        panel_subtitle.setObjectName("subtitle")
        panel_layout.addWidget(panel_subtitle)

        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(6)
        self._tab_btns = []
        for index, label in enumerate(["Invité", "Professeur"]):
            button = QPushButton(label)
            button.setCheckable(True)
            button.setProperty("class", "tab")
            button.setFixedHeight(40)
            button.clicked.connect(lambda _, idx=index: self._switch_tab(idx))
            self._tab_btns.append(button)
            tabs_row.addWidget(button)
        panel_layout.addLayout(tabs_row)

        self.stack = QStackedWidget()
        self.stack.setMinimumHeight(340)
        self.stack.addWidget(self._build_guest_panel())
        self.stack.addWidget(self._build_teacher_panel())
        self.stack.addWidget(self._build_student_panel())
        panel_layout.addWidget(self.stack, stretch=1)

        root.addWidget(panel, stretch=1)
        self._switch_tab(0)

    # ── Panneaux ──────────────────────────────────────────────────────

    def _build_guest_panel(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 24, 0, 0)
        layout.setSpacing(14)
        title = QLabel("Démarrer sans compte")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:700;")
        description = QLabel(
            "Lancez directement un entraînement. Aucun profil, classe ou groupe à créer."
        )
        description.setObjectName("subtitle")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        button = QPushButton("Commencer en mode invité")
        button.setFixedHeight(46)
        button.clicked.connect(self._login_guest)
        layout.addWidget(button)
        layout.addStretch()
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
        l.addWidget(btn)
        create_btn = QPushButton("＋ Créer un profil professeur")
        create_btn.setProperty("class", "secondary")
        create_btn.clicked.connect(self._create_teacher)
        l.addWidget(create_btn)
        student_btn = QPushButton("Accès élèves  →")
        student_btn.setProperty("class", "secondary")
        student_btn.clicked.connect(self._open_student_access)
        l.addWidget(student_btn)
        l.addStretch()
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
        self.student_exit_btn = QPushButton("← Retour aux modes")
        self.student_exit_btn.setProperty("class", "secondary")
        self.student_exit_btn.clicked.connect(lambda: self._switch_tab(1))
        l.addWidget(self.student_exit_btn)
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
        self.no_profile_lbl = QLabel("Aucun élève dans cette sélection.")
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
        self._refresh_profile_cards(group_id=grp["id"])
        self._go_step(2, f"{self._selected_class['name']}  ›  {grp['name']}{level_str}  —  Qui êtes-vous ?")

    def _on_ungrouped_selected(self, class_id: str):
        self._selected_group = None
        students = [
            student for student in db.get_students(class_id=class_id)
            if not student.get("group_id")
        ]
        self._refresh_profile_cards(students=students)
        self._go_step(2, f"{self._selected_class['name']}  ›  Élèves sans groupe  —  Qui êtes-vous ?")

    # ── Refresh cards ─────────────────────────────────────────────────

    def _refresh_class_cards(self):
        self._clear_layout(self.class_cards_l)
        classes = db.get_classes()
        unassigned = db.get_unassigned_students()
        if not classes and not unassigned:
            self.no_class_lbl.show()
            return
        self.no_class_lbl.hide()
        for cls in classes:
            nb = len(db.get_groups(class_id=cls["id"]))
            card = self._make_icon_card(
                initiales=cls["name"][:2].upper(),
                label=cls["name"],
                sublabel=f"{cls.get('level', 'CM2')}  ·  {nb} groupe{'s' if nb != 1 else ''}",
                color="#0879C9",
                size=(110, 100),
                on_click=lambda _, c=cls: self._on_class_selected(c)
            )
            self.class_cards_l.addWidget(card)
        if unassigned:
            card = self._make_icon_card(
                initiales="…",
                label="Sans classe",
                sublabel=f"{len(unassigned)} élève{'s' if len(unassigned) > 1 else ''}",
                color="#79748C",
                size=(110, 100),
                on_click=lambda _: self._on_unassigned_selected()
            )
            self.class_cards_l.addWidget(card)

    def _on_unassigned_selected(self):
        self._selected_class = {"id": None, "name": "Sans classe"}
        self._selected_group = None
        self._refresh_profile_cards(students=db.get_unassigned_students())
        self._go_step(2, "Sans classe  —  Qui êtes-vous ?")

    def _refresh_group_cards(self, class_id: str):
        self._clear_layout(self.group_cards_l)
        groups = db.get_groups(class_id=class_id)
        ungrouped = [s for s in db.get_students(class_id=class_id) if not s.get("group_id")]
        if not groups and not ungrouped:
            self.no_group_lbl.show()
            return
        self.no_group_lbl.hide()
        if ungrouped:
            card = self._make_icon_card(
                initiales="•",
                label="Élèves sans groupe",
                sublabel=f"{len(ungrouped)} élève{'s' if len(ungrouped) > 1 else ''}",
                color="#2998E5",
                size=(130, 100),
                on_click=lambda _, cid=class_id: self._on_ungrouped_selected(cid)
            )
            self.group_cards_l.addWidget(card)
        for grp in groups:
            nb = len(db.get_students(group_id=grp["id"]))
            level = grp.get("level", "")
            card = self._make_icon_card(
                initiales=grp["name"][:2].upper(),
                label=grp["name"],
                sublabel=level,
                color="#269B70",
                size=(110, 100),
                on_click=lambda _, g=grp: self._on_group_selected(g)
            )
            self.group_cards_l.addWidget(card)

    def _refresh_profile_cards(self, group_id=None, class_id=None, students=None):
        self._clear_layout(self.profile_cards_l)
        if students is None:
            students = db.get_students(group_id=group_id) if group_id else db.get_students(class_id=class_id)
        if not students:
            self.no_profile_lbl.show(); return
        self.no_profile_lbl.hide()
        for s in students:
            initiales = f"{s['prenom'][0]}{s['nom'][0]}".upper()
            card = self._make_icon_card(
                initiales=initiales,
                label=s["prenom"],
                sublabel=s["nom"],
                color="#2998E5",
                size=(100, 95),
                on_click=lambda _, st=s: self._login_student(st)
            )
            self.profile_cards_l.addWidget(card)

    def _make_icon_card(self, initiales, label, sublabel, color, size, on_click) -> QWidget:
        card = QPushButton()
        card.setFixedSize(*size)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setProperty("class", "student-card")
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
        sub.setStyleSheet("font-size:11px;background:transparent;")

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
        if idx == 1: self._refresh_teacher_combo()
        elif idx == 2:
            self._go_step(0, "Sélectionnez votre classe")
            self._refresh_class_cards()

    def _open_student_access(self):
        """Student selection is an access path inside the teacher workspace, not a third mode."""
        self._switch_tab(2)

    def refresh(self):
        self._switch_tab(self.stack.currentIndex())

    def _refresh_teacher_combo(self):
        self.teacher_combo.clear()
        for t in db.get_teachers():
            self.teacher_combo.addItem(f"{t['prenom']} {t['nom']}", userData=t)

    def _create_teacher(self):
        # Reuse the existing validated profile-creation dialog.
        from ui.screen_admin import AddTeacherDialog
        dialog = AddTeacherDialog(self)
        if dialog.exec():
            self._refresh_teacher_combo()
            self.teacher_combo.setCurrentIndex(self.teacher_combo.count() - 1)

    # ── Authentification ──────────────────────────────────────────────

    def _login_guest(self):
        session.login_guest()
        self.logged_in.emit()

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

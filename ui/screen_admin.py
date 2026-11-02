# ui/screen_admin.py — Wedone Operate
# Gestion : Classes, Groupes (avec niveau scolaire), Élèves, Profs, Modèles de session.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QDialog, QFrame, QListWidget,
    QListWidgetItem, QMessageBox, QStackedWidget, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import database as db
import session
from constants import SCHOOL_LEVELS, DIFFICULTY_LEVELS


def _wire_enter(dialog, submit_button):
    """Make Enter submit any text field in a form, consistently across dialogs."""
    submit_button.setDefault(True)
    submit_button.setAutoDefault(True)
    for field in dialog.findChildren(QLineEdit):
        field.returnPressed.connect(submit_button.click)


class AdminScreen(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        nav = QWidget(); nav.setFixedWidth(220)
        nav.setProperty("class", "side-nav")
        nl = QVBoxLayout(nav); nl.setContentsMargins(12,20,12,20); nl.setSpacing(6)
        nl.setAlignment(Qt.AlignmentFlag.AlignTop)

        t = QLabel("Gestion"); t.setStyleSheet("font-size:16px;font-weight:bold;padding-bottom:8px;")
        nl.addWidget(t)

        self._nav_btns = []
        self._nav_items = [
            ("👨‍🏫  Professeurs", 0),
            ("🏫  Classes",       1),
            ("👥  Groupes",       2),
            ("🎓  Élèves",        3),
            ("📋  Modèles",       4),
        ]
        for label, idx in self._nav_items:
            btn = QPushButton(label); btn.setProperty("class", "nav")
            btn.clicked.connect(lambda _, i=idx: self._switch(i))
            nl.addWidget(btn); self._nav_btns.append(btn)

        nl.addStretch()
        back_btn = QPushButton("← Retour"); back_btn.setProperty("class", "secondary")
        back_btn.clicked.connect(self.go_back); nl.addWidget(back_btn)
        root.addWidget(nav)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_teachers())  # 0
        self.stack.addWidget(self._build_classes())   # 1
        self.stack.addWidget(self._build_groups())    # 2
        self.stack.addWidget(self._build_students())  # 3
        self.stack.addWidget(self._build_templates()) # 4
        root.addWidget(self.stack)

    def _switch(self, idx):
        if idx == 0 and session.current.is_teacher():
            idx = 1
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._nav_btns):
            btn.setProperty("class", "nav-active" if i == idx else "nav")
            btn.style().unpolish(btn); btn.style().polish(btn)
        refresh_fns = {
            0: self._refresh_teachers,
            1: self._refresh_classes,
            2: self._refresh_groups,
            3: self._refresh_students,
            4: self._refresh_templates,
        }
        fn = refresh_fns.get(idx)
        if fn: fn()
    def refresh(self):
        self._nav_btns[0].setVisible(session.current.is_admin())
        start = 1 if session.current.is_teacher() else 0
        self.stack.setCurrentIndex(start)
        for i, btn in enumerate(self._nav_btns):
            btn.setProperty("class", "nav-active" if i == start else "nav")
            btn.style().unpolish(btn); btn.style().polish(btn)
        if start == 0: self._refresh_teachers()
        else: self._refresh_classes()

    # ── Helpers UI ────────────────────────────────────────────────────

    def _section(self, title, add_label, add_fn):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(28,22,28,22); l.setSpacing(12)
        h = QHBoxLayout()
        t = QLabel(title); t.setStyleSheet("font-size:18px;font-weight:bold;")
        h.addWidget(t); h.addStretch()
        if add_label:
            btn = QPushButton(add_label); btn.clicked.connect(add_fn); h.addWidget(btn)
        l.addLayout(h)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); l.addWidget(sep)
        return w, l

    # ══ PROFS ══════════════════════════════════════════════════════════

    def _build_teachers(self):
        w, l = self._section("Professeurs", "＋ Ajouter", self._add_teacher)
        self.teachers_list = QListWidget(); l.addWidget(self.teachers_list)
        acts = QHBoxLayout()
        edit = QPushButton("✏ Modifier"); edit.setProperty("class", "secondary")
        edit.clicked.connect(self._edit_teacher)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class", "danger")
        d.clicked.connect(self._del_teacher)
        acts.addWidget(edit); acts.addWidget(d); acts.addStretch(); l.addLayout(acts)
        return w

    def _refresh_teachers(self):
        self.teachers_list.clear()
        for t in db.get_teachers():
            nb = len(db.get_groups(owner_id=t["id"]))
            item = QListWidgetItem(f"  {t['prenom']} {t['nom']}  —  {nb} groupe{'s' if nb>1 else ''}")
            item.setData(Qt.ItemDataRole.UserRole, t)
            self.teachers_list.addItem(item)

    def _add_teacher(self):
        dlg = AddTeacherDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_teachers()

    def _edit_teacher(self):
        item = self.teachers_list.currentItem()
        if not item: return
        teacher = item.data(Qt.ItemDataRole.UserRole)
        dlg = EditTeacherDialog(teacher, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._refresh_teachers()

    def _del_teacher(self):
        item = self.teachers_list.currentItem()
        if not item: return
        t = item.data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Confirmer",
            f"Supprimer {t['prenom']} {t['nom']} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            db.remove_teacher(t["id"]); self._refresh_teachers()

    # ══ CLASSES ════════════════════════════════════════════════════════

    def _build_classes(self):
        w, l = self._section("Classes", "＋ Ajouter une classe", self._add_class)
        self.classes_list = QListWidget(); l.addWidget(self.classes_list)
        acts = QHBoxLayout()
        edit = QPushButton("✏ Modifier"); edit.setProperty("class", "secondary")
        edit.clicked.connect(self._edit_class)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_class)
        acts.addWidget(edit); acts.addWidget(d); acts.addStretch(); l.addLayout(acts)
        return w

    def _refresh_classes(self):
        self.classes_list.clear()
        owner_id = None if session.current.is_admin() else session.current.user_id
        for cls in db.get_classes(owner_id=owner_id):
            nb_groups = len(db.get_groups(class_id=cls["id"]))
            nb_students = len(db.get_students(class_id=cls["id"]))
            item = QListWidgetItem(
                f"  {cls['name']}  ·  {cls.get('level', 'CM2')}  ·  "
                f"{nb_students} élève{'s' if nb_students != 1 else ''}  ·  "
                f"{nb_groups} groupe{'s' if nb_groups != 1 else ''}"
            )
            item.setData(Qt.ItemDataRole.UserRole, cls)
            self.classes_list.addItem(item)

    def _add_class(self):
        dlg = AddClassDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            owner_id = session.current.user_id if session.current.is_teacher() else "guest"
            if not db.add_class(dlg.value(), owner_id, dlg.level()):
                QMessageBox.warning(self, "Erreur", "Cette classe existe déjà ou le niveau est invalide.")
            else:
                self._refresh_classes()

    def _edit_class(self):
        item = self.classes_list.currentItem()
        if not item: return
        cls = item.data(Qt.ItemDataRole.UserRole)
        dlg = EditClassDialog(cls, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            if not db.update_class(cls["id"], dlg.value(), dlg.level()):
                QMessageBox.warning(self, "Modification impossible", "Ce nom existe déjà ou les informations sont invalides.")
            self._refresh_classes()

    def _del_class(self):
        item = self.classes_list.currentItem()
        if not item: return
        c = item.data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Confirmer", f"Supprimer la classe « {c['name']} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            db.remove_class(c["id"]); self._refresh_classes()

    # ══ GROUPES ════════════════════════════════════════════════════════

    def _build_groups(self):
        w, l = self._section("Groupes", "＋ Créer un groupe", self._add_group)
        # Filtre par classe
        fr = QHBoxLayout(); fr.addWidget(QLabel("Filtrer :"))
        self.group_class_filter = QComboBox(); self.group_class_filter.setFixedWidth(180)
        self.group_class_filter.currentIndexChanged.connect(self._refresh_groups)
        fr.addWidget(self.group_class_filter); fr.addStretch()
        l.addLayout(fr)
        self.groups_list = QListWidget(); l.addWidget(self.groups_list)
        acts = QHBoxLayout()
        edit_btn = QPushButton("✏ Modifier"); edit_btn.setProperty("class","secondary")
        edit_btn.clicked.connect(self._edit_group)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_group)
        acts.addWidget(edit_btn); acts.addWidget(d); acts.addStretch()
        l.addLayout(acts)
        return w

    def _refresh_groups(self):
        # Filtre classes
        self.group_class_filter.blockSignals(True)
        self.group_class_filter.clear()
        self.group_class_filter.addItem("Toutes les classes", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        for c in db.get_classes(owner_id=owner_id):
            self.group_class_filter.addItem(c["name"], userData=c["id"])
        self.group_class_filter.blockSignals(False)

        class_id = self.group_class_filter.currentData()
        self.groups_list.clear()
        for g in db.get_groups(owner_id=owner_id, class_id=class_id):
            nb = len(db.get_students(group_id=g["id"]))
            cls = db.get_class(g.get("class_id"))
            cls_str = f" [{cls['name']}]" if cls else ""
            item = QListWidgetItem(
                f"  {g['name']}{cls_str}  —  Niveau {g.get('level','?')}  —  {nb} élève{'s' if nb>1 else ''}"
            )
            item.setData(Qt.ItemDataRole.UserRole, g)
            self.groups_list.addItem(item)

    def _add_group(self):
        dlg = AddGroupDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_groups()

    def _edit_group(self):
        item = self.groups_list.currentItem()
        if not item: return
        group = item.data(Qt.ItemDataRole.UserRole)
        dlg = EditGroupDialog(group, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            if not db.update_group(group["id"], name=dlg.name(), level=dlg.level(), class_id=dlg.class_id()):
                QMessageBox.warning(self, "Modification impossible", "Vérifie le nom, la classe et le niveau du groupe.")
            self._refresh_groups()

    def _del_group(self):
        item = self.groups_list.currentItem()
        if not item: return
        g = item.data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Confirmer", f"Supprimer « {g['name']} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            db.remove_group(g["id"]); self._refresh_groups()

    # ══ ÉLÈVES ═════════════════════════════════════════════════════════

    def _build_students(self):
        w, l = self._section("Élèves", "＋ Ajouter un élève", self._add_student)
        fr = QHBoxLayout()
        fr.addWidget(QLabel("Groupe :"))
        self.student_group_filter = QComboBox(); self.student_group_filter.setFixedWidth(200)
        self.student_group_filter.currentIndexChanged.connect(self._refresh_students)
        fr.addWidget(self.student_group_filter); fr.addStretch()
        l.addLayout(fr)
        self.students_list = QListWidget(); l.addWidget(self.students_list)
        acts = QHBoxLayout()
        edit = QPushButton("✏ Modifier"); edit.setProperty("class", "secondary")
        edit.clicked.connect(self._edit_student)
        assign_btn = QPushButton("📂 Assigner groupe"); assign_btn.setProperty("class","secondary")
        assign_btn.clicked.connect(self._assign_group)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_student)
        acts.addWidget(edit); acts.addWidget(assign_btn); acts.addWidget(d); acts.addStretch()
        l.addLayout(acts)
        return w

    def _refresh_students(self):
        owner_id = None if session.current.is_admin() else session.current.user_id
        self.student_group_filter.blockSignals(True)
        self.student_group_filter.clear()
        self.student_group_filter.addItem("Tous les élèves", userData=None)
        for g in db.get_groups(owner_id=owner_id):
            self.student_group_filter.addItem(g["name"], userData=g["id"])
        self.student_group_filter.blockSignals(False)

        group_id = self.student_group_filter.currentData()
        self.students_list.clear()
        for s in db.get_students(teacher_id=owner_id, group_id=group_id):
            g = db.get_group(s.get("group_id"))
            gstr = f" — {g['name']} ({g.get('level','')})" if g else " — Sans groupe"
            item = QListWidgetItem(f"  {s['prenom']} {s['nom']}{gstr}")
            item.setData(Qt.ItemDataRole.UserRole, s)
            self.students_list.addItem(item)

    def _add_student(self):
        dlg = AddStudentDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_students()

    def _edit_student(self):
        item = self.students_list.currentItem()
        if not item: return
        student = item.data(Qt.ItemDataRole.UserRole)
        dlg = EditStudentDialog(student, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            if not db.update_student(student["id"], dlg.prenom(), dlg.nom(), dlg.class_id(), dlg.group_id()):
                QMessageBox.warning(self, "Modification impossible", "Vérifie l'identité et le rattachement de l'élève.")
            self._refresh_students()

    def _del_student(self):
        item = self.students_list.currentItem()
        if not item: return
        s = item.data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Confirmer",
            f"Supprimer {s['prenom']} {s['nom']} et tous ses scores ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            db.remove_student(s["id"]); self._refresh_students()

    def _assign_group(self):
        item = self.students_list.currentItem()
        if not item: return
        s = item.data(Qt.ItemDataRole.UserRole)
        dlg = AssignGroupDialog(s, self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_students()

    # ══ MODÈLES DE SESSION ═════════════════════════════════════════════

    def _build_templates(self):
        w, l = self._section("Modèles de session", "＋ Créer un modèle", self._add_template)
        info = QLabel("Un modèle peut s'appliquer à toute une classe ou seulement à un groupe.\n"
                      "Un modèle de groupe est prioritaire sur celui de la classe.")
        info.setObjectName("subtitle"); info.setWordWrap(True)
        l.addWidget(info)
        self.templates_list = QListWidget(); l.addWidget(self.templates_list)
        acts = QHBoxLayout()
        edit = QPushButton("✏ Modifier"); edit.setProperty("class", "secondary")
        edit.clicked.connect(self._edit_template); acts.addWidget(edit)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_template); acts.addWidget(d); acts.addStretch()
        l.addLayout(acts)
        return w

    def _refresh_templates(self):
        self.templates_list.clear()
        owner_id = session.current.user_id if session.current.is_teacher() else None
        for t in db.get_templates(owner_id=owner_id):
            g = db.get_group(t.get("group_id"))
            cls = db.get_class(t.get("class_id"))
            c = t["config"]
            ops = "+".join({"addition":"+","soustraction":"−","multiplication":"×","division":"÷"}.get(o,o)
                           for o in c.get("operations",[]))
            target = f" → Groupe {g['name']}" if g else (f" → Classe {cls['name']}" if cls else " → Modèle libre")
            item = QListWidgetItem(
                f"  {t['name']}{target}  —  {c.get('nb_epreuves',10)} épr.  {c.get('level','?')}  {ops}"
            )
            item.setData(Qt.ItemDataRole.UserRole, t)
            self.templates_list.addItem(item)

    def _add_template(self):
        dlg = AddTemplateDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_templates()

    def _edit_template(self):
        item = self.templates_list.currentItem()
        if not item: return
        template = item.data(Qt.ItemDataRole.UserRole)
        dlg = AddTemplateDialog(self, template=template)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._refresh_templates()

    def _del_template(self):
        item = self.templates_list.currentItem()
        if not item: return
        t = item.data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Confirmer", f"Supprimer le modèle « {t['name']} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            db.remove_template(t["id"]); self._refresh_templates()


# ══════════════════════════════════════════════════════════════════════
# Dialogues
# ══════════════════════════════════════════════════════════════════════

class EditTeacherDialog(QDialog):
    def __init__(self, teacher, parent=None):
        super().__init__(parent)
        self._teacher = teacher
        self.setWindowTitle("Modifier le professeur")
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self); layout.setSpacing(10); layout.setContentsMargins(22, 20, 22, 20)
        layout.addWidget(QLabel("Prénom"))
        self.prenom = QLineEdit(teacher.get("prenom", "")); layout.addWidget(self.prenom)
        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit(teacher.get("nom", "")); layout.addWidget(self.nom)
        layout.addWidget(QLabel("Nouveau mot de passe (facultatif)"))
        self.password = QLineEdit(); self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Laisser vide pour conserver l'actuel"); layout.addWidget(self.password)
        self.error = QLabel(""); self.error.setObjectName("error"); self.error.hide(); layout.addWidget(self.error)
        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class", "secondary"); cancel.clicked.connect(self.reject)
        save = QPushButton("Enregistrer"); save.clicked.connect(self._save)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)
        _wire_enter(self, save)

    def _save(self):
        password = self.password.text() or None
        if password is not None and len(password) < 6:
            self.error.setText("Le mot de passe doit contenir au moins 6 caractères."); self.error.show(); return
        if not db.update_teacher(self._teacher["id"], self.prenom.text(), self.nom.text(), password):
            self.error.setText("Informations invalides ou nom déjà utilisé."); self.error.show(); return
        self.accept()


class EditClassDialog(QDialog):
    def __init__(self, cls, parent=None):
        super().__init__(parent)
        self._class = cls
        self.setWindowTitle("Modifier la classe")
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self); layout.setSpacing(10); layout.setContentsMargins(22, 20, 22, 20)
        layout.addWidget(QLabel("Nom de la classe"))
        self.name = QLineEdit(cls.get("name", "")); layout.addWidget(self.name)
        layout.addWidget(QLabel("Niveau scolaire"))
        self.level_combo = QComboBox(); self.level_combo.addItems(SCHOOL_LEVELS)
        self.level_combo.setCurrentText(cls.get("level", "CM2")); layout.addWidget(self.level_combo)
        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class", "secondary"); cancel.clicked.connect(self.reject)
        save = QPushButton("Enregistrer"); save.clicked.connect(self.accept)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)
        _wire_enter(self, save)

    def value(self): return self.name.text().strip()
    def level(self): return self.level_combo.currentText()


class EditGroupDialog(QDialog):
    def __init__(self, group, parent=None):
        super().__init__(parent)
        self._group = group
        self.setWindowTitle("Modifier le groupe")
        self.setMinimumWidth(360)
        layout = QVBoxLayout(self); layout.setSpacing(10); layout.setContentsMargins(22, 20, 22, 20)
        layout.addWidget(QLabel("Nom du groupe"))
        self.name_input = QLineEdit(group.get("name", "")); layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Niveau scolaire"))
        self.level_combo = QComboBox(); self.level_combo.addItems(SCHOOL_LEVELS)
        self.level_combo.setCurrentText(group.get("level", "CM2")); layout.addWidget(self.level_combo)
        layout.addWidget(QLabel("Classe (facultatif)"))
        self.class_combo = QComboBox(); self.class_combo.addItem("— Aucune classe —", userData=None)
        owner_id = session.current.user_id if session.current.is_teacher() else group.get("owner_id")
        for cls in db.get_classes(owner_id=owner_id):
            self.class_combo.addItem(cls["name"], userData=cls["id"])
        index = self.class_combo.findData(group.get("class_id"))
        if index >= 0: self.class_combo.setCurrentIndex(index)
        layout.addWidget(self.class_combo)
        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class", "secondary"); cancel.clicked.connect(self.reject)
        save = QPushButton("Enregistrer"); save.clicked.connect(self.accept)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)
        _wire_enter(self, save)

    def name(self): return self.name_input.text().strip()
    def level(self): return self.level_combo.currentText()
    def class_id(self): return self.class_combo.currentData()


class EditStudentDialog(QDialog):
    def __init__(self, student, parent=None):
        super().__init__(parent)
        self._student = student
        self.setWindowTitle("Modifier l'élève")
        self.setMinimumWidth(360)
        layout = QVBoxLayout(self); layout.setSpacing(10); layout.setContentsMargins(22, 20, 22, 20)
        layout.addWidget(QLabel("Prénom"))
        self.prenom_input = QLineEdit(student.get("prenom", "")); layout.addWidget(self.prenom_input)
        layout.addWidget(QLabel("Nom"))
        self.nom_input = QLineEdit(student.get("nom", "")); layout.addWidget(self.nom_input)
        owner_id = session.current.user_id if session.current.is_teacher() else student.get("created_by")
        layout.addWidget(QLabel("Classe"))
        self.class_combo = QComboBox(); self.class_combo.addItem("— Sans classe —", userData=None)
        for cls in db.get_classes(owner_id=owner_id):
            self.class_combo.addItem(f"{cls['name']} · {cls.get('level', 'CM2')}", userData=cls["id"])
        idx = self.class_combo.findData(student.get("class_id"))
        if idx >= 0: self.class_combo.setCurrentIndex(idx)
        layout.addWidget(self.class_combo)
        layout.addWidget(QLabel("Groupe (facultatif)"))
        self.group_combo = QComboBox()
        self._owner_id = owner_id
        self.class_combo.currentIndexChanged.connect(self._refresh_groups)
        self._refresh_groups()
        layout.addWidget(self.group_combo)
        self.error = QLabel(""); self.error.setObjectName("error"); self.error.hide(); layout.addWidget(self.error)
        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class", "secondary"); cancel.clicked.connect(self.reject)
        save = QPushButton("Enregistrer"); save.clicked.connect(self._save)
        buttons.addWidget(cancel); buttons.addWidget(save); layout.addLayout(buttons)
        _wire_enter(self, save)

    def _refresh_groups(self):
        class_id = self.class_combo.currentData()
        previous = self.group_combo.currentData() if self.group_combo.count() else self._student.get("group_id")
        self.group_combo.blockSignals(True)
        self.group_combo.clear()
        self.group_combo.addItem("— Sans groupe —", userData=None)
        for group in db.get_groups(owner_id=self._owner_id):
            if class_id and group.get("class_id") not in (None, class_id):
                continue
            self.group_combo.addItem(f"{group['name']} · {group.get('level', 'CM2')}", userData=group["id"])
        index = self.group_combo.findData(previous)
        if index >= 0: self.group_combo.setCurrentIndex(index)
        self.group_combo.blockSignals(False)

    def prenom(self): return self.prenom_input.text().strip()
    def nom(self): return self.nom_input.text().strip()
    def class_id(self): return self.class_combo.currentData()
    def group_id(self): return self.group_combo.currentData()
    def _save(self):
        if not self.prenom() or not self.nom():
            self.error.setText("Prénom et nom obligatoires."); self.error.show(); return
        self.accept()


class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouvelle classe")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumWidth(340)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(22, 20, 22, 20)

        layout.addWidget(QLabel("Nom de la classe"))
        self._name = QLineEdit()
        self._name.setPlaceholderText("ex. 5ème B")
        layout.addWidget(self._name)

        layout.addWidget(QLabel("Niveau scolaire"))
        self._level = QComboBox()
        self._level.addItems(SCHOOL_LEVELS)
        self._level.setCurrentText("CM2")
        layout.addWidget(self._level)

        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler")
        cancel.setProperty("class", "secondary")
        cancel.clicked.connect(self.reject)
        create = QPushButton("Créer la classe")
        create.clicked.connect(self._ok)
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        layout.addLayout(buttons)
        _wire_enter(self, create)

    def value(self):
        return self._name.text().strip()

    def level(self):
        return self._level.currentText()

    def _ok(self):
        if not self.value():
            QMessageBox.warning(self, "Classe", "Le nom de la classe est obligatoire.")
            return
        self.accept()


class SimpleNameDialog(QDialog):
    def __init__(self, title, label, placeholder, parent=None):
        super().__init__(parent); self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(300)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel(label))
        self._input = QLineEdit(); self._input.setPlaceholderText(placeholder)
        l.addWidget(self._input)
        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)
    def value(self): return self._input.text().strip()
    def _ok(self):
        if not self._input.text().strip():
            self._err.setText("Champ obligatoire."); self._err.show(); return
        self.accept()


class AddTeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Ajouter un professeur")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(340)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        for attr, lbl, ph in [("prenom","Prénom","ex. Marie"), ("nom","Nom","ex. Curie"),
                               ("pwd","Mot de passe provisoire","Min. 6 caractères")]:
            l.addWidget(QLabel(lbl)); inp = QLineEdit(); inp.setPlaceholderText(ph)
            if attr == "pwd": inp.setEchoMode(QLineEdit.EchoMode.Password)
            setattr(self, f"_{attr}", inp); l.addWidget(inp)
        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)
    def _ok(self):
        p, n, pwd = self._prenom.text().strip(), self._nom.text().strip(), self._pwd.text()
        if not p or not n: self._err.setText("Prénom et nom obligatoires."); self._err.show(); return
        if len(pwd) < 6: self._err.setText("Mot de passe trop court."); self._err.show(); return
        if not db.add_teacher(p, n, pwd): self._err.setText("Ce professeur existe déjà."); self._err.show(); return
        self.accept()


class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Créer un groupe")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(340)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel("Nom du groupe"))
        self._name = QLineEdit(); self._name.setPlaceholderText("ex. Groupe A, 6ème renforcé…")
        l.addWidget(self._name)
        l.addWidget(QLabel("Niveau scolaire"))
        self._level = QComboBox(); self._level.addItems(SCHOOL_LEVELS); self._level.setCurrentText("CM2")
        l.addWidget(self._level)
        l.addWidget(QLabel("Classe (optionnel)"))
        self._class = QComboBox(); self._class.addItem("— Aucune classe —", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        for c in db.get_classes(owner_id=owner_id): self._class.addItem(c["name"], userData=c["id"])
        l.addWidget(self._class)
        if session.current.is_admin():
            l.addWidget(QLabel("Propriétaire"))
            self._owner = QComboBox()
            for t in db.get_teachers(): self._owner.addItem(f"{t['prenom']} {t['nom']}", userData=t["id"])
            l.addWidget(self._owner)
        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)
    def _ok(self):
        name = self._name.text().strip()
        if not name: self._err.setText("Nom obligatoire."); self._err.show(); return
        owner_id = (getattr(self, "_owner", None) and self._owner.currentData()) or session.current.user_id
        if not owner_id: self._err.setText("Propriétaire requis."); self._err.show(); return
        if not db.add_group(name, owner_id, self._level.currentText(), self._class.currentData()):
            self._err.setText("Ce groupe existe déjà."); self._err.show(); return
        self.accept()


class EditGroupLevelDialog(QDialog):
    def __init__(self, group, parent=None):
        super().__init__(parent); self.setWindowTitle(f"Modifier — {group['name']}")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(280); self._group = group
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel("Niveau scolaire :"))
        self._level = QComboBox(); self._level.addItems(SCHOOL_LEVELS)
        self._level.setCurrentText(group.get("level","CM2")); l.addWidget(self._level)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Enregistrer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)
    def _ok(self):
        db.update_group(self._group["id"], level=self._level.currentText()); self.accept()


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un élève")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumWidth(360)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(22, 20, 22, 20)

        layout.addWidget(QLabel("Prénom"))
        self._prenom = QLineEdit()
        self._prenom.setPlaceholderText("ex. Lucas")
        layout.addWidget(self._prenom)

        layout.addWidget(QLabel("Nom"))
        self._nom = QLineEdit()
        self._nom.setPlaceholderText("ex. Bernard")
        layout.addWidget(self._nom)

        owner_id = session.current.user_id if session.current.is_teacher() else None
        layout.addWidget(QLabel("Classe (facultatif)"))
        self._class = QComboBox()
        self._class.addItem("— Sans classe —", userData=None)
        for cls in db.get_classes(owner_id=owner_id):
            self._class.addItem(f"{cls['name']} · {cls.get('level', 'CM2')}", userData=cls["id"])
        self._class.currentIndexChanged.connect(self._refresh_groups)
        layout.addWidget(self._class)

        layout.addWidget(QLabel("Groupe (facultatif)"))
        self._group = QComboBox()
        layout.addWidget(self._group)
        self._refresh_groups()

        self._err = QLabel("")
        self._err.setObjectName("error")
        self._err.hide()
        layout.addWidget(self._err)

        buttons = QHBoxLayout()
        cancel = QPushButton("Annuler")
        cancel.setProperty("class", "secondary")
        cancel.clicked.connect(self.reject)
        create = QPushButton("Créer l'élève")
        create.clicked.connect(self._ok)
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        layout.addLayout(buttons)
        _wire_enter(self, create)

    def _refresh_groups(self):
        owner_id = session.current.user_id if session.current.is_teacher() else None
        class_id = self._class.currentData()
        self._group.clear()
        self._group.addItem("— Sans groupe —", userData=None)
        for group in db.get_groups(owner_id=owner_id):
            if class_id and group.get("class_id") not in (None, class_id):
                continue
            self._group.addItem(
                f"{group['name']} ({group.get('level', '')})",
                userData=group["id"]
            )

    def _ok(self):
        prenom, nom = self._prenom.text().strip(), self._nom.text().strip()
        if not prenom or not nom:
            self._err.setText("Prénom et nom obligatoires.")
            self._err.show()
            return
        teacher_id = session.current.user_id if session.current.is_teacher() else "guest"
        student = db.add_student(
            prenom, nom, teacher_id,
            group_id=self._group.currentData(),
            class_id=self._class.currentData()
        )
        if not student:
            self._err.setText("Un élève portant ce nom existe déjà ou le rattachement est invalide.")
            self._err.show()
            return
        self.accept()


class AssignGroupDialog(QDialog):
    def __init__(self, student, parent=None):
        super().__init__(parent); self.setWindowTitle(f"Assigner {student['prenom']}")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(280); self._s = student
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel("Groupe :"))
        self._combo = QComboBox(); self._combo.addItem("— Sans groupe —", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        student_class_id = student.get("class_id")
        for g in db.get_groups(owner_id=owner_id):
            if student_class_id and g.get("class_id") not in (None, student_class_id):
                continue
            self._combo.addItem(f"{g['name']} ({g.get('level','')})", userData=g["id"])
            if g["id"] == student.get("group_id"): self._combo.setCurrentIndex(self._combo.count()-1)
        l.addWidget(self._combo)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Assigner"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)
    def _ok(self): db.assign_student_group(self._s["id"], self._combo.currentData()); self.accept()


class AddTemplateDialog(QDialog):
    def __init__(self, parent=None, template=None):
        super().__init__(parent); self._template = template
        self.setWindowTitle("Modifier le modèle" if template else "Créer un modèle de session")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(380)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)

        l.addWidget(QLabel("Nom du modèle"))
        self._name = QLineEdit(); self._name.setPlaceholderText("ex. Tables de multiplication CM1")
        l.addWidget(self._name)

        self._owner_id = session.current.user_id if session.current.is_teacher() else "guest"
        l.addWidget(QLabel("Classe cible (facultatif)"))
        self._class = QComboBox()
        self._class.addItem("— Modèle libre —", userData=None)
        for cls in db.get_classes(owner_id=self._owner_id):
            self._class.addItem(f"{cls['name']} · {cls.get('level', 'CM2')}", userData=cls["id"])
        self._class.currentIndexChanged.connect(self._refresh_groups)
        l.addWidget(self._class)

        l.addWidget(QLabel("Groupe cible (facultatif, prioritaire sur la classe)"))
        self._group = QComboBox()
        self._group.currentIndexChanged.connect(self._on_group_changed)
        l.addWidget(self._group)
        self._refresh_groups()

        l.addWidget(QLabel("Niveau scolaire"))
        self._level = QComboBox(); self._level.addItems(SCHOOL_LEVELS); self._level.setCurrentText("CM2")
        l.addWidget(self._level)

        l.addWidget(QLabel("Nombre d'épreuves"))
        self._nb = QSpinBox(); self._nb.setMinimum(1); self._nb.setMaximum(100); self._nb.setValue(10)
        l.addWidget(self._nb)

        l.addWidget(QLabel("Opérations"))
        ops_row = QHBoxLayout()
        self._add = QCheckBox("Addition"); self._add.setChecked(True)
        self._sub = QCheckBox("Soustraction"); self._sub.setChecked(True)
        self._mul = QCheckBox("Multiplication"); self._div = QCheckBox("Division")
        for cb in (self._add, self._sub, self._mul, self._div): ops_row.addWidget(cb)
        l.addLayout(ops_row)

        self._timer = QCheckBox("Session chronométrée"); l.addWidget(self._timer)

        if template:
            config = template.get("config", {})
            self._name.setText(template.get("name", ""))
            self._level.setCurrentText(config.get("level", "CM2"))
            self._nb.setValue(max(1, min(100, int(config.get("nb_epreuves", 10)))))
            self._add.setChecked("addition" in config.get("operations", []))
            self._sub.setChecked("soustraction" in config.get("operations", []))
            self._mul.setChecked("multiplication" in config.get("operations", []))
            self._div.setChecked("division" in config.get("operations", []))
            self._timer.setChecked(bool(config.get("timer_enabled", False)))
            class_id = template.get("class_id")
            if not class_id and template.get("group_id"):
                group = db.get_group(template["group_id"])
                class_id = group.get("class_id") if group else None
            class_index = self._class.findData(class_id)
            if class_index >= 0: self._class.setCurrentIndex(class_index)
            self._refresh_groups()
            index = self._group.findData(template.get("group_id"))
            if index >= 0: self._group.setCurrentIndex(index)

        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Enregistrer" if template else "Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
        _wire_enter(self, ok)

    def _refresh_groups(self):
        if not hasattr(self, "_group"):
            return
        class_id = self._class.currentData()
        previous = self._group.currentData() if self._group.count() else (
            self._template.get("group_id") if self._template else None
        )
        self._group.blockSignals(True)
        self._group.clear()
        self._group.addItem("— Aucun groupe —", userData=None)
        for group in db.get_groups(owner_id=self._owner_id):
            if class_id and group.get("class_id") not in (None, class_id):
                continue
            self._group.addItem(f"{group['name']} · {group.get('level', 'CM2')}", userData=group["id"])
        index = self._group.findData(previous)
        if index >= 0: self._group.setCurrentIndex(index)
        self._group.blockSignals(False)

    def _on_group_changed(self):
        group_id = self._group.currentData()
        group = db.get_group(group_id) if group_id else None
        if group and group.get("class_id"):
            index = self._class.findData(group["class_id"])
            if index >= 0 and self._class.currentIndex() != index:
                self._class.setCurrentIndex(index)

    def _ok(self):
        name = self._name.text().strip()
        if not name: self._err.setText("Nom obligatoire."); self._err.show(); return
        ops = [o for cb, o in [(self._add,"addition"),(self._sub,"soustraction"),
                                (self._mul,"multiplication"),(self._div,"division")] if cb.isChecked()]
        if not ops: self._err.setText("Sélectionnez au moins une opération."); self._err.show(); return
        config = {"level": self._level.currentText(), "nb_epreuves": self._nb.value(),
                  "operations": ops, "timer_enabled": self._timer.isChecked()}
        group_id = self._group.currentData()
        class_id = self._class.currentData()
        if self._template:
            ok = db.update_template(self._template["id"], name, config, group_id, class_id)
        else:
            ok = db.save_template(name, self._owner_id, config, group_id, class_id)
        if not ok:
            self._err.setText("Ce nom existe déjà ou le groupe est invalide."); self._err.show(); return
        self.accept()

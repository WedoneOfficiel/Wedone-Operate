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


class AdminScreen(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        nav = QWidget(); nav.setFixedWidth(190)
        nav.setStyleSheet("border-right: 1px solid rgba(128,128,128,0.2);")
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
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger"); d.setFixedWidth(200)
        d.clicked.connect(self._del_teacher); l.addWidget(d)
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
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger"); d.setFixedWidth(200)
        d.clicked.connect(self._del_class); l.addWidget(d)
        return w

    def _refresh_classes(self):
        self.classes_list.clear()
        owner_id = None if session.current.is_admin() else session.current.user_id
        for c in db.get_classes(owner_id=owner_id):
            nb = len(db.get_groups(class_id=c["id"]))
            item = QListWidgetItem(f"  {c['name']}  —  {nb} groupe{'s' if nb>1 else ''}")
            item.setData(Qt.ItemDataRole.UserRole, c)
            self.classes_list.addItem(item)

    def _add_class(self):
        dlg = SimpleNameDialog("Nouvelle classe", "Nom de la classe", "ex. 5ème B", self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            owner_id = session.current.user_id if session.current.is_teacher() else "admin"
            if not db.add_class(dlg.value(), owner_id):
                QMessageBox.warning(self, "Erreur", "Cette classe existe déjà.")
            else: self._refresh_classes()

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
        edit_btn = QPushButton("✏ Modifier le niveau"); edit_btn.setProperty("class","secondary")
        edit_btn.clicked.connect(self._edit_group_level)
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

    def _edit_group_level(self):
        item = self.groups_list.currentItem()
        if not item: return
        g = item.data(Qt.ItemDataRole.UserRole)
        dlg = EditGroupLevelDialog(g, self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_groups()

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
        assign_btn = QPushButton("📂 Assigner groupe"); assign_btn.setProperty("class","secondary")
        assign_btn.clicked.connect(self._assign_group)
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_student)
        acts.addWidget(assign_btn); acts.addWidget(d); acts.addStretch()
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
        info = QLabel("Les modèles définissent une config par défaut pour un groupe.\n"
                      "L'élève peut la modifier avant de lancer sa session.")
        info.setObjectName("subtitle"); info.setWordWrap(True)
        l.addWidget(info)
        self.templates_list = QListWidget(); l.addWidget(self.templates_list)
        acts = QHBoxLayout()
        d = QPushButton("🗑 Supprimer"); d.setProperty("class","danger")
        d.clicked.connect(self._del_template); acts.addWidget(d); acts.addStretch()
        l.addLayout(acts)
        return w

    def _refresh_templates(self):
        self.templates_list.clear()
        owner_id = session.current.user_id if session.current.is_teacher() else None
        for t in db.get_templates(owner_id=owner_id):
            g = db.get_group(t.get("group_id"))
            c = t["config"]
            ops = "+".join({"addition":"+","soustraction":"−","multiplication":"×","division":"÷"}.get(o,o)
                           for o in c.get("operations",[]))
            gname = f" → {g['name']}" if g else ""
            item = QListWidgetItem(
                f"  {t['name']}{gname}  —  {c.get('nb_epreuves',10)} épr.  {c.get('level','?')}  {ops}"
            )
            item.setData(Qt.ItemDataRole.UserRole, t)
            self.templates_list.addItem(item)

    def _add_template(self):
        dlg = AddTemplateDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self._refresh_templates()

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
    def _ok(self):
        db.update_group(self._group["id"], level=self._level.currentText()); self.accept()


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Ajouter un élève")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(320)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel("Prénom"))
        self._prenom = QLineEdit(); self._prenom.setPlaceholderText("ex. Lucas"); l.addWidget(self._prenom)
        l.addWidget(QLabel("Nom"))
        self._nom = QLineEdit(); self._nom.setPlaceholderText("ex. Bernard"); l.addWidget(self._nom)
        l.addWidget(QLabel("Groupe"))
        self._group = QComboBox(); self._group.addItem("— Sans groupe —", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        for g in db.get_groups(owner_id=owner_id):
            self._group.addItem(f"{g['name']} ({g.get('level','')})", userData=g["id"])
        l.addWidget(self._group)
        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
    def _ok(self):
        p, n = self._prenom.text().strip(), self._nom.text().strip()
        if not p or not n: self._err.setText("Prénom et nom obligatoires."); self._err.show(); return
        tid = session.current.user_id if session.current.is_teacher() else "admin"
        if not db.add_student(p, n, tid, self._group.currentData()):
            self._err.setText("Cet élève existe déjà."); self._err.show(); return
        self.accept()


class AssignGroupDialog(QDialog):
    def __init__(self, student, parent=None):
        super().__init__(parent); self.setWindowTitle(f"Assigner {student['prenom']}")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(280); self._s = student
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)
        l.addWidget(QLabel("Groupe :"))
        self._combo = QComboBox(); self._combo.addItem("— Sans groupe —", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        for g in db.get_groups(owner_id=owner_id):
            self._combo.addItem(f"{g['name']} ({g.get('level','')})", userData=g["id"])
            if g["id"] == student.get("group_id"): self._combo.setCurrentIndex(self._combo.count()-1)
        l.addWidget(self._combo)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Assigner"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)
    def _ok(self): db.assign_student_group(self._s["id"], self._combo.currentData()); self.accept()


class AddTemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Créer un modèle de session")
        self.setWindowIcon(QIcon("icon.png")); self.setMinimumWidth(380)
        l = QVBoxLayout(self); l.setSpacing(10); l.setContentsMargins(22,20,22,20)

        l.addWidget(QLabel("Nom du modèle"))
        self._name = QLineEdit(); self._name.setPlaceholderText("ex. Tables de multiplication CM1")
        l.addWidget(self._name)

        l.addWidget(QLabel("Groupe cible"))
        self._group = QComboBox(); self._group.addItem("— Aucun groupe spécifique —", userData=None)
        owner_id = None if session.current.is_admin() else session.current.user_id
        for g in db.get_groups(owner_id=owner_id):
            self._group.addItem(f"{g['name']} ({g.get('level','')})", userData=g["id"])
        l.addWidget(self._group)

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

        self._err = QLabel(""); self._err.setObjectName("error"); self._err.hide(); l.addWidget(self._err)
        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setProperty("class","secondary"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Créer"); ok.clicked.connect(self._ok)
        btns.addWidget(cancel); btns.addWidget(ok); l.addLayout(btns)

    def _ok(self):
        name = self._name.text().strip()
        if not name: self._err.setText("Nom obligatoire."); self._err.show(); return
        ops = [o for cb, o in [(self._add,"addition"),(self._sub,"soustraction"),
                                (self._mul,"multiplication"),(self._div,"division")] if cb.isChecked()]
        if not ops: self._err.setText("Sélectionnez au moins une opération."); self._err.show(); return
        config = {"level": self._level.currentText(), "nb_epreuves": self._nb.value(),
                  "operations": ops, "timer_enabled": self._timer.isChecked()}
        owner_id = session.current.user_id if session.current.is_teacher() else "admin"
        db.save_template(name, owner_id, config, self._group.currentData())
        self.accept()

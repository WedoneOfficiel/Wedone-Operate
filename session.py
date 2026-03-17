# session.py — Wedone Operate
# Singleton léger qui stocke l'utilisateur connecté pour la durée de l'exécution.
# Pas de persistance — la session est réinitialisée à chaque lancement.

from dataclasses import dataclass, field
from typing import Literal

Role = Literal["admin", "teacher", "student"]

@dataclass
class Session:
    role:       Role        = "student"
    user_id:    str | None  = None   # None pour admin, "t_..." ou "s_..."
    prenom:     str         = ""
    nom:        str         = ""
    group_id:   str | None  = None   # groupe de l'élève, ou None

    # ── Helpers ────────────────────────────────────────────────────────
    def is_admin(self)   -> bool: return self.role == "admin"
    def is_teacher(self) -> bool: return self.role == "teacher"
    def is_student(self) -> bool: return self.role == "student"

    def can_see_updates(self)      -> bool: return self.role in ("admin", "teacher")
    def can_manage_students(self)  -> bool: return self.role in ("admin", "teacher")
    def can_manage_teachers(self)  -> bool: return self.role == "admin"
    def can_manage_groups(self)    -> bool: return self.role in ("admin", "teacher")
    def can_see_group_stats(self)  -> bool: return self.role in ("admin", "teacher")
    def can_change_password(self)  -> bool: return self.role in ("admin", "teacher")

    def display_name(self) -> str:
        if self.role == "admin":
            return "Administrateur"
        return f"{self.prenom} {self.nom}"

    def role_label(self) -> str:
        return {"admin": "Admin", "teacher": "Professeur", "student": "Élève"}.get(self.role, "")

    def clear(self):
        self.role     = "student"
        self.user_id  = None
        self.prenom   = ""
        self.nom      = ""
        self.group_id = None


# Instance globale unique — importée depuis tous les modules UI
current = Session()


def login_admin() -> None:
    current.role    = "admin"
    current.user_id = None
    current.prenom  = "Admin"
    current.nom     = ""

def login_teacher(teacher: dict) -> None:
    current.role    = "teacher"
    current.user_id = teacher["id"]
    current.prenom  = teacher["prenom"]
    current.nom     = teacher["nom"]

def login_student(student: dict) -> None:
    current.role    = "student"
    current.user_id = student["id"]
    current.prenom  = student["prenom"]
    current.nom     = student["nom"]
    current.group_id = student.get("group_id")

def logout() -> None:
    current.clear()

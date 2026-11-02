"""Classroom data access with archive-first deletion semantics."""

from __future__ import annotations

from datetime import datetime, timezone
import sqlite3
from uuid import uuid4

from .database import Database
from ..security import hash_password, verify_password


class ClassroomRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_teacher(self, display_name: str, password: str) -> str:
        name = display_name.strip()
        if not name:
            raise ValueError("Le nom du professeur est obligatoire.")
        credential_hash = hash_password(password)
        teacher_id = str(uuid4())
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO teachers(id, display_name, credential_hash) VALUES (?, ?, ?)",
                (teacher_id, name, credential_hash),
            )
        return teacher_id

    def authenticate_teacher(self, teacher_id: str, password: str) -> bool:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT credential_hash FROM teachers WHERE id=? AND archived_at IS NULL",
                (teacher_id,),
            ).fetchone()
        return row is not None and verify_password(password, row["credential_hash"])

    def update_teacher(self, teacher_id: str, display_name: str) -> None:
        name = display_name.strip()
        if not name:
            raise ValueError("Le nom du professeur est obligatoire.")
        with self.database.transaction() as connection:
            cursor = connection.execute(
                "UPDATE teachers SET display_name=? WHERE id=? AND archived_at IS NULL",
                (name, teacher_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Profil professeur introuvable.")

    def create_class(self, name: str, school_year: str | None = None) -> str:
        label = name.strip()
        if not label:
            raise ValueError("Le nom de la classe est obligatoire.")
        class_id = str(uuid4())
        with self.database.transaction() as connection:
            connection.execute(
                "INSERT INTO classes(id, name, school_year) VALUES (?, ?, ?)",
                (class_id, label, school_year),
            )
        return class_id

    def update_class(self, class_id: str, name: str, school_year: str | None = None) -> None:
        label = name.strip()
        if not label:
            raise ValueError("Le nom de la classe est obligatoire.")
        with self.database.transaction() as connection:
            cursor = connection.execute(
                "UPDATE classes SET name=?, school_year=? WHERE id=? AND archived_at IS NULL",
                (label, school_year, class_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Classe introuvable.")

    def create_group(self, class_id: str, name: str) -> str:
        label = name.strip()
        if not label:
            raise ValueError("Le nom du groupe est obligatoire.")
        group_id = str(uuid4())
        with self.database.transaction() as connection:
            exists = connection.execute(
                "SELECT 1 FROM classes WHERE id=? AND archived_at IS NULL", (class_id,)
            ).fetchone()
            if exists is None:
                raise ValueError("Classe introuvable.")
            connection.execute(
                "INSERT INTO groups(id, class_id, name) VALUES (?, ?, ?)",
                (group_id, class_id, label),
            )
        return group_id

    def create_student(self, class_id: str, display_name: str, group_id: str | None = None) -> str:
        name = display_name.strip()
        if not name:
            raise ValueError("Le nom de l'élève est obligatoire.")
        student_id = str(uuid4())
        with self.database.transaction() as connection:
            class_row = connection.execute(
                "SELECT 1 FROM classes WHERE id=? AND archived_at IS NULL", (class_id,)
            ).fetchone()
            if class_row is None:
                raise ValueError("Classe introuvable.")
            if group_id is not None:
                group_row = connection.execute(
                    "SELECT 1 FROM groups WHERE id=? AND class_id=? AND archived_at IS NULL",
                    (group_id, class_id),
                ).fetchone()
                if group_row is None:
                    raise ValueError("Le groupe sélectionné n'appartient pas à cette classe.")
            connection.execute(
                "INSERT INTO students(id, class_id, group_id, display_name) VALUES (?, ?, ?, ?)",
                (student_id, class_id, group_id, name),
            )
        return student_id

    def list_classes(self) -> list[dict]:
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, name, school_year, created_at FROM classes "
                "WHERE archived_at IS NULL ORDER BY name COLLATE NOCASE"
            ).fetchall()
        return [dict(row) for row in rows]

    def list_groups(self, class_id: str) -> list[dict]:
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, class_id, name FROM groups "
                "WHERE class_id=? AND archived_at IS NULL ORDER BY name COLLATE NOCASE",
                (class_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_students(self, class_id: str, group_id: str | None = None) -> list[dict]:
        query = (
            "SELECT id, class_id, group_id, display_name, created_at FROM students "
            "WHERE class_id=? AND archived_at IS NULL"
        )
        parameters: tuple = (class_id,)
        if group_id is not None:
            query += " AND group_id=?"
            parameters += (group_id,)
        query += " ORDER BY display_name COLLATE NOCASE"
        with self.database.connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]

    def archive_student(self, student_id: str) -> None:
        self._archive("students", student_id)

    def archive_group(self, group_id: str) -> None:
        self._archive("groups", group_id)

    def archive_class(self, class_id: str) -> None:
        self._archive("classes", class_id)

    def archive_teacher(self, teacher_id: str) -> None:
        self._archive("teachers", teacher_id)

    def _archive(self, table: str, record_id: str) -> None:
        # Table names are selected only by the fixed internal methods above.
        if table not in {"students", "groups", "classes", "teachers"}:
            raise ValueError("Type d'archive invalide.")
        archived_at = datetime.now(timezone.utc).isoformat()
        with self.database.transaction() as connection:
            cursor = connection.execute(
                f"UPDATE {table} SET archived_at=? WHERE id=? AND archived_at IS NULL",
                (archived_at, record_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Élément introuvable ou déjà archivé.")

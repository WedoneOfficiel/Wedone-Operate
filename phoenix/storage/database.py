"""Small transactional SQLite foundation for Phoenix.

No legacy JSON discovery/import happens here. Callers must opt into migration.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterator
from contextlib import contextmanager

CURRENT_SCHEMA_VERSION = 1


class DatabaseError(RuntimeError):
    """Raised when the Phoenix database cannot be safely opened or migrated."""


_MIGRATIONS = {
    1: """
    CREATE TABLE app_settings (
        key TEXT PRIMARY KEY,
        value_json TEXT NOT NULL,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE teachers (
        id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        credential_hash TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        archived_at TEXT
    );

    CREATE TABLE classes (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        school_year TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        archived_at TEXT
    );

    CREATE TABLE groups (
        id TEXT PRIMARY KEY,
        class_id TEXT NOT NULL REFERENCES classes(id) ON DELETE RESTRICT,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        archived_at TEXT
    );

    CREATE TABLE students (
        id TEXT PRIMARY KEY,
        class_id TEXT NOT NULL REFERENCES classes(id) ON DELETE RESTRICT,
        group_id TEXT REFERENCES groups(id) ON DELETE RESTRICT,
        display_name TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        archived_at TEXT
    );

    CREATE TABLE exercise_plans (
        id TEXT PRIMARY KEY,
        owner_teacher_id TEXT REFERENCES teachers(id) ON DELETE RESTRICT,
        name TEXT NOT NULL,
        configuration_json TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        archived_at TEXT
    );

    CREATE TABLE practice_sessions (
        id TEXT PRIMARY KEY,
        student_id TEXT REFERENCES students(id) ON DELETE RESTRICT,
        mode TEXT NOT NULL CHECK (mode IN ('individual', 'classroom')),
        status TEXT NOT NULL CHECK (status IN ('in_progress', 'completed', 'abandoned')),
        configuration_json TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        correct_count INTEGER NOT NULL DEFAULT 0 CHECK (correct_count >= 0),
        question_count INTEGER NOT NULL DEFAULT 0 CHECK (question_count >= 0)
    );

    CREATE TABLE practice_answers (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL REFERENCES practice_sessions(id) ON DELETE CASCADE,
        position INTEGER NOT NULL CHECK (position >= 0),
        skill_id TEXT NOT NULL,
        prompt TEXT NOT NULL,
        expected_answer TEXT NOT NULL,
        given_answer TEXT,
        is_correct INTEGER CHECK (is_correct IN (0, 1)),
        elapsed_ms INTEGER CHECK (elapsed_ms IS NULL OR elapsed_ms >= 0),
        UNIQUE(session_id, position)
    );

    CREATE INDEX idx_groups_class ON groups(class_id);
    CREATE INDEX idx_students_class ON students(class_id);
    CREATE INDEX idx_students_group ON students(group_id);
    CREATE INDEX idx_sessions_student_date ON practice_sessions(student_id, started_at);
    CREATE INDEX idx_answers_session ON practice_answers(session_id, position);
    """,
}


class Database:
    """Connection-per-operation SQLite database with explicit transactions."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=10.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        try:
            with self.connect() as connection:
                connection.execute("PRAGMA journal_mode = WAL")
                version = int(connection.execute("PRAGMA user_version").fetchone()[0])
                if version > CURRENT_SCHEMA_VERSION:
                    raise DatabaseError(
                        f"Base Phoenix trop récente (version {version}, prise en charge {CURRENT_SCHEMA_VERSION})."
                    )
                for target in range(version + 1, CURRENT_SCHEMA_VERSION + 1):
                    script = _MIGRATIONS.get(target)
                    if script is None:
                        raise DatabaseError(f"Migration manquante : {target}")
                    connection.executescript(
                        "BEGIN IMMEDIATE;\\n" + script + f"\\nPRAGMA user_version = {target};\\nCOMMIT;"
                    )
        except (sqlite3.Error, OSError) as exc:
            if isinstance(exc, DatabaseError):
                raise
            raise DatabaseError(f"Impossible d'initialiser la base Phoenix : {exc}") from exc

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self.connect() as connection:
            try:
                connection.execute("BEGIN IMMEDIATE")
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    def get_setting(self, key: str, default: Any = None) -> Any:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT value_json FROM app_settings WHERE key = ?", (key,)
            ).fetchone()
        return default if row is None else json.loads(row["value_json"])

    def set_setting(self, key: str, value: Any) -> None:
        encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        with self.transaction() as connection:
            connection.execute(
                "INSERT INTO app_settings(key, value_json) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, "
                "updated_at=CURRENT_TIMESTAMP",
                (key, encoded),
            )

    def get_mode(self) -> str | None:
        mode = self.get_setting("usage_mode")
        return mode if mode in ("individual", "classroom") else None

    def set_mode(self, mode: str) -> None:
        if mode not in ("individual", "classroom"):
            raise ValueError("Le mode doit être 'individual' ou 'classroom'.")
        self.set_setting("usage_mode", mode)

    def integrity_check(self) -> bool:
        with self.connect() as connection:
            rows = connection.execute("PRAGMA integrity_check").fetchall()
        return len(rows) == 1 and rows[0][0] == "ok"

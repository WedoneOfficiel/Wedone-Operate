"""Verified SQLite backup and restore helpers."""

from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path

from .database import CURRENT_SCHEMA_VERSION, Database, DatabaseError


def create_backup(database: Database, destination: str | Path) -> Path:
    """Create a consistent SQLite backup using SQLite's online backup API."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        with database.connect() as source:
            backup = sqlite3.connect(temporary)
            try:
                source.backup(backup)
                backup.commit()
            finally:
                backup.close()
        _validate_database(temporary)
        os.replace(temporary, target)
        return target
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def restore_backup(database: Database, source: str | Path, safety_backup: str | Path) -> Path:
    """Validate a backup, preserve the current DB, then atomically replace it."""
    source_path = Path(source)
    if not source_path.is_file():
        raise DatabaseError("Fichier de sauvegarde introuvable.")
    _validate_database(source_path)
    create_backup(database, safety_backup)

    database.path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix="phoenix-restore-", suffix=".sqlite3", dir=database.path.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        restored = sqlite3.connect(source_path)
        target = sqlite3.connect(temporary)
        try:
            restored.backup(target)
            target.commit()
        finally:
            restored.close()
            target.close()
        _validate_database(temporary)
        os.replace(temporary, database.path)
        # SQLite may leave sidecars after a previous WAL-mode connection.
        Path(str(database.path) + "-wal").unlink(missing_ok=True)
        Path(str(database.path) + "-shm").unlink(missing_ok=True)
        return database.path
    finally:
        temporary.unlink(missing_ok=True)


def _validate_database(path: Path) -> None:
    try:
        connection = sqlite3.connect(path)
        try:
            result = connection.execute("PRAGMA integrity_check").fetchone()
            version = int(connection.execute("PRAGMA user_version").fetchone()[0])
        finally:
            connection.close()
        if result is None or result[0] != "ok":
            raise DatabaseError("La sauvegarde est endommagée.")
        if version < 1 or version > CURRENT_SCHEMA_VERSION:
            raise DatabaseError(f"Version de sauvegarde non prise en charge : {version}.")
    except sqlite3.Error as exc:
        raise DatabaseError(f"Fichier SQLite invalide : {exc}") from exc

"""Explicit JSON export/import and safe local-data reset."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import tempfile

from .backup import create_backup
from .database import CURRENT_SCHEMA_VERSION, Database, DatabaseError

EXPORT_FORMAT = "wedone-phoenix-export"
TABLE_ORDER = (
    "teachers",
    "classes",
    "groups",
    "students",
    "exercise_plans",
    "practice_sessions",
    "practice_answers",
    "app_settings",
)
DELETE_ORDER = tuple(reversed(TABLE_ORDER))


def _safety_backup_path(database: Database) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return database.path.parent / "backups" / f"before-change-{stamp}.sqlite3"


def export_json(database: Database, destination: str | Path) -> Path:
    """Export every Phoenix table to a portable, versioned JSON file."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    with database.connect() as connection:
        tables = {}
        for table in TABLE_ORDER:
            rows = connection.execute(f"SELECT * FROM {table}").fetchall()
            tables[table] = [dict(row) for row in rows]
    payload = {
        "format": EXPORT_FORMAT,
        "schema_version": CURRENT_SCHEMA_VERSION,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "tables": tables,
    }
    fd, temporary_name = tempfile.mkstemp(
        prefix="phoenix-export-", suffix=".json", dir=target.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temporary, target)
        return target
    finally:
        temporary.unlink(missing_ok=True)


def import_json(database: Database, source: str | Path) -> Path:
    """Replace local data from a Phoenix export after making a safety backup."""
    source_path = Path(source)
    if not source_path.is_file():
        raise DatabaseError("Fichier d'import introuvable.")
    try:
        payload = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise DatabaseError(f"Fichier JSON invalide : {exc}") from exc
    if not isinstance(payload, dict) or payload.get("format") != EXPORT_FORMAT:
        raise DatabaseError("Ce fichier n'est pas un export Wedone Operate Phoenix.")
    if payload.get("schema_version") != CURRENT_SCHEMA_VERSION:
        raise DatabaseError("La version de cet export n'est pas prise en charge.")
    tables = payload.get("tables")
    if not isinstance(tables, dict) or set(tables) != set(TABLE_ORDER):
        raise DatabaseError("L'export ne contient pas exactement les tables attendues.")

    with database.connect() as connection:
        allowed_columns = {
            table: {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
            for table in TABLE_ORDER
        }
    for table, rows in tables.items():
        if not isinstance(rows, list):
            raise DatabaseError(f"Contenu de table invalide : {table}.")
        for row in rows:
            if not isinstance(row, dict) or not set(row).issubset(allowed_columns[table]):
                raise DatabaseError(f"Enregistrement invalide dans la table {table}.")
            if any(isinstance(value, (dict, list)) for value in row.values()):
                raise DatabaseError(f"Valeur non prise en charge dans la table {table}.")

    safety_backup = _safety_backup_path(database)
    create_backup(database, safety_backup)
    try:
        with database.transaction() as connection:
            for table in DELETE_ORDER:
                connection.execute(f"DELETE FROM {table}")
            for table in TABLE_ORDER:
                for row in tables[table]:
                    if not row:
                        continue
                    columns = tuple(row)
                    placeholders = ", ".join("?" for _ in columns)
                    column_sql = ", ".join(columns)
                    connection.execute(
                        f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
                        tuple(row[column] for column in columns),
                    )
            violations = connection.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise DatabaseError("L'export contient des références entre données invalides.")
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError(f"Import annulé ; les données existantes sont conservées : {exc}") from exc
    return safety_backup


def reset_data(database: Database) -> Path:
    """Clear all Phoenix data only after creating a restorable safety backup."""
    safety_backup = _safety_backup_path(database)
    create_backup(database, safety_backup)
    with database.transaction() as connection:
        for table in DELETE_ORDER:
            connection.execute(f"DELETE FROM {table}")
    return safety_backup

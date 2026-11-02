"""Regression tests for the Phoenix persistence foundation."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from phoenix.storage.backup import create_backup, restore_backup
from phoenix.storage.database import Database, DatabaseError, CURRENT_SCHEMA_VERSION
from phoenix.storage.paths import APP_DATA_DIR_NAME, DATABASE_FILENAME


class PhoenixDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = Database(self.root / "phoenix.sqlite3")
        self.database.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def test_data_location_is_separate_from_legacy_app(self):
        self.assertEqual(APP_DATA_DIR_NAME, "Wedone Operate Phoenix")
        self.assertEqual(DATABASE_FILENAME, "phoenix.sqlite3")

    def test_initializes_current_schema(self):
        with self.database.connect() as connection:
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        self.assertEqual(version, CURRENT_SCHEMA_VERSION)
        self.assertTrue({"app_settings", "students", "practice_sessions", "practice_answers"} <= tables)

    def test_mode_is_persisted_and_validated(self):
        self.assertIsNone(self.database.get_mode())
        self.database.set_mode("individual")
        self.assertEqual(self.database.get_mode(), "individual")
        self.database.set_mode("classroom")
        self.assertEqual(self.database.get_mode(), "classroom")
        with self.assertRaises(ValueError):
            self.database.set_mode("guest")

    def test_transaction_rolls_back_on_error(self):
        with self.assertRaises(RuntimeError):
            with self.database.transaction() as connection:
                connection.execute(
                    "INSERT INTO app_settings(key, value_json) VALUES (?, ?)",
                    ("temporary", '"value"'),
                )
                raise RuntimeError("abort")
        self.assertIsNone(self.database.get_setting("temporary"))

    def test_backup_and_restore_preserve_data(self):
        self.database.set_mode("individual")
        backup = create_backup(self.database, self.root / "backups" / "before.sqlite3")
        self.database.set_mode("classroom")
        safety = self.root / "backups" / "safety.sqlite3"
        restore_backup(self.database, backup, safety)
        self.assertEqual(self.database.get_mode(), "individual")
        self.assertTrue(safety.is_file())
        self.assertTrue(self.database.integrity_check())

    def test_corrupt_backup_is_rejected_without_touching_live_data(self):
        self.database.set_mode("classroom")
        corrupt = self.root / "corrupt.sqlite3"
        corrupt.write_bytes(b"not a sqlite database")
        with self.assertRaises(DatabaseError):
            restore_backup(self.database, corrupt, self.root / "safety.sqlite3")
        self.assertEqual(self.database.get_mode(), "classroom")


if __name__ == "__main__":
    unittest.main()

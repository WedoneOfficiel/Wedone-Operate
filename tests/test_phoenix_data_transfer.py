"""Tests for explicit Phoenix JSON export, import and reset."""

import json
import tempfile
import unittest
from pathlib import Path

from phoenix.storage.data_transfer import export_json, import_json, reset_data
from phoenix.storage.database import Database, DatabaseError


class PhoenixDataTransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = Database(self.root / "phoenix.sqlite3")
        self.database.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def test_export_and_import_round_trip(self):
        self.database.set_mode("individual")
        export_path = export_json(self.database, self.root / "exports" / "backup.json")
        self.database.set_mode("classroom")
        safety_path = import_json(self.database, export_path)
        self.assertEqual(self.database.get_mode(), "individual")
        self.assertTrue(safety_path.is_file())

    def test_invalid_export_does_not_change_existing_data(self):
        self.database.set_mode("classroom")
        invalid = self.root / "invalid.json"
        invalid.write_text(json.dumps({"format": "wrong"}), encoding="utf-8")
        with self.assertRaises(DatabaseError):
            import_json(self.database, invalid)
        self.assertEqual(self.database.get_mode(), "classroom")

    def test_reset_clears_data_and_keeps_safety_backup(self):
        self.database.set_mode("individual")
        safety_path = reset_data(self.database)
        self.assertTrue(safety_path.is_file())
        self.assertIsNone(self.database.get_mode())
        self.assertTrue(self.database.integrity_check())


if __name__ == "__main__":
    unittest.main()

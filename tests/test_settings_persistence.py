import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import settings


class SettingsPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patch = patch.object(settings, "data_file", side_effect=lambda name: self.root / name)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_settings_round_trip(self):
        values = settings.load()
        values["theme"] = "dark"
        settings.save(values)
        self.assertEqual("dark", settings.load()["theme"])

    def test_corrupt_settings_are_preserved(self):
        path = self.root / settings.SETTINGS_FILE
        path.write_text("{invalid", encoding="utf-8")
        loaded = settings.load()
        self.assertEqual("system", loaded["theme"])
        self.assertEqual("{invalid", path.read_text(encoding="utf-8"))

    def test_saved_json_is_complete(self):
        settings.save({"theme": "light", "auto_update": False})
        path = self.root / settings.SETTINGS_FILE
        self.assertEqual(
            {"theme": "light", "auto_update": False},
            json.loads(path.read_text(encoding="utf-8"))
        )


if __name__ == "__main__":
    unittest.main()

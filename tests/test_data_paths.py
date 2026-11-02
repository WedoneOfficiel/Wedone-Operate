import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data_paths

class DataPathsTests(unittest.TestCase):
    def test_linux_uses_xdg_data_home(self):
        with patch.object(data_paths.platform, "system", return_value="Linux"), patch.dict(os.environ, {"XDG_DATA_HOME": "/tmp/wedone-xdg"}):
            self.assertEqual(data_paths.get_data_dir(), Path("/tmp/wedone-xdg/wedone-operate"))

    def test_windows_uses_roaming_appdata(self):
        with patch.object(data_paths.platform, "system", return_value="Windows"), patch.dict(os.environ, {"APPDATA": "/tmp/wedone-roaming"}):
            self.assertEqual(data_paths.get_data_dir(), Path("/tmp/wedone-roaming/Wedone Operate"))

    def test_legacy_file_is_copied_without_deleting_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy_dir, target_dir = root / "legacy", root / "target"
            legacy_dir.mkdir()
            (legacy_dir / "users.json").write_text('{"students": []}', encoding="utf-8")
            with patch.object(data_paths.Path, "cwd", return_value=legacy_dir), patch.object(data_paths, "get_data_dir", return_value=target_dir):
                target = data_paths.data_file("users.json")
            self.assertEqual(target.read_text(encoding="utf-8"), '{"students": []}')
            self.assertTrue((legacy_dir / "users.json").exists())

    def test_existing_destination_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy_dir, target_dir = root / "legacy", root / "target"
            legacy_dir.mkdir()
            target_dir.mkdir()
            (legacy_dir / "users.json").write_text("legacy", encoding="utf-8")
            (target_dir / "users.json").write_text("new", encoding="utf-8")
            with patch.object(data_paths.Path, "cwd", return_value=legacy_dir), patch.object(data_paths, "get_data_dir", return_value=target_dir):
                target = data_paths.data_file("users.json")
            self.assertEqual(target.read_text(encoding="utf-8"), "new")
            self.assertEqual((legacy_dir / "users.json").read_text(encoding="utf-8"), "legacy")

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            data_paths.data_file("../users.json")

if __name__ == "__main__":
    unittest.main()

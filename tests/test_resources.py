import unittest
from pathlib import Path
from unittest.mock import patch

from ui.resources import resource_path


class ResourcePathTests(unittest.TestCase):
    def test_source_resource_resolves_from_project_root(self):
        path = Path(resource_path("icon.png"))
        self.assertEqual(path.name, "icon.png")
        self.assertEqual(path.parent.name, "Wedone-Operate")

    def test_frozen_resource_uses_meipass(self):
        with patch("ui.resources.sys._MEIPASS", "/tmp/wedone-bundle", create=True):
            self.assertEqual(resource_path("icon.png"), "/tmp/wedone-bundle/icon.png")


if __name__ == "__main__":
    unittest.main()

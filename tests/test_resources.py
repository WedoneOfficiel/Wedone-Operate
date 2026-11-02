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
        bundle_dir = Path("/tmp/wedone-bundle")
        with patch("ui.resources.sys._MEIPASS", str(bundle_dir), create=True):
            self.assertEqual(
                Path(resource_path("icon.png")),
                bundle_dir / "icon.png",
            )


if __name__ == "__main__":
    unittest.main()

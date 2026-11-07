"""Platform effect safety tests for headless CI and desktop fallbacks."""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from PySide6.QtCore import QObject

from phoenix.ui.platform_effects import PlatformEffects


class PlatformEffectsTests(unittest.TestCase):
    def test_offscreen_mode_never_calls_native_window_api(self):
        effects = PlatformEffects()
        with patch.dict(os.environ, {"QT_QPA_PLATFORM": "offscreen"}):
            with patch.object(PlatformEffects, "_apply_windows") as windows, patch.object(
                PlatformEffects, "_apply_macos"
            ) as macos:
                effects.applyToWindow(QObject())
        windows.assert_not_called()
        macos.assert_not_called()
        self.assertFalse(effects.nativeBackdropApplied)


if __name__ == "__main__":
    unittest.main()

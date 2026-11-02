import unittest
from unittest.mock import patch

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from ui.screen_admin import AddClassDialog, SimpleNameDialog
from ui.screen_settings import SettingsScreen


class DialogKeyboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_enter_submits_simple_text_dialog(self):
        dialog = SimpleNameDialog("Test", "Nom", "Nom")
        dialog._input.setText("Groupe A")
        dialog.show()
        QTest.keyClick(dialog._input, Qt.Key.Key_Return)
        self.assertEqual(dialog.result(), dialog.DialogCode.Accepted)
        dialog.close()

    def test_enter_submits_class_dialog(self):
        dialog = AddClassDialog()
        dialog._name.setText("CM2 A")
        dialog.show()
        QTest.keyClick(dialog._name, Qt.Key.Key_Return)
        self.assertEqual(dialog.result(), dialog.DialogCode.Accepted)
        dialog.close()

    def test_loading_settings_does_not_save_stale_widget_values(self):
        screen = SettingsScreen()
        screen._settings = {
            "theme": "dark", "auto_update": False, "difficulty": "CE2",
            "addition_enabled": True, "subtraction_enabled": False,
            "multiplication_enabled": True, "division_enabled": False,
            "timer_enabled": True,
        }
        with patch("ui.screen_settings.cfg.save") as save:
            screen._load_values()
        save.assert_not_called()
        self.assertEqual(screen.theme_combo.currentIndex(), 2)
        self.assertEqual(screen.diff_combo.currentText(), "CE2")
        self.assertFalse(screen.cb_sub.isChecked())
        self.assertTrue(screen.cb_timer_def.isChecked())


if __name__ == "__main__":
    unittest.main()

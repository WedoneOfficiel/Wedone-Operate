import unittest

from constants import DARK, LIGHT
from ui.theme import get_stylesheet


class ThemeTests(unittest.TestCase):
    def test_light_and_dark_palettes_have_same_tokens(self):
        self.assertEqual(set(LIGHT), set(DARK))

    def test_wedone_blue_is_the_primary_accent(self):
        self.assertEqual(LIGHT["primary"], "#167CC2")
        self.assertEqual(DARK["primary"], "#3296D8")

    def test_palette_uses_wedone_portal_neutrals(self):
        self.assertEqual(LIGHT["bg"], "#F5F8FC")
        self.assertEqual(LIGHT["text"], "#202B3A")
        self.assertEqual(LIGHT["text_secondary"], "#66768A")
        self.assertNotIn("pink", LIGHT)
        self.assertNotIn("pink", DARK)

    def test_stylesheets_are_generated_for_both_themes(self):
        for theme in ("light", "dark"):
            with self.subTest(theme=theme):
                stylesheet = get_stylesheet(theme)
                self.assertIn("DM Sans", stylesheet)
                self.assertIn("Manrope", stylesheet)
                self.assertIn("QPushButton", stylesheet)
                self.assertIn("QLineEdit", stylesheet)
                self.assertIn("student-card", stylesheet)
                self.assertIn("warning-card", stylesheet)

    def test_unknown_theme_falls_back_to_light(self):
        self.assertEqual(get_stylesheet("unexpected"), get_stylesheet("light"))


if __name__ == "__main__":
    unittest.main()

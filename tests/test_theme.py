import unittest

from constants import DARK, LIGHT
from ui.theme import get_stylesheet


class ThemeTests(unittest.TestCase):
    def test_light_and_dark_palettes_have_same_tokens(self):
        self.assertEqual(set(LIGHT), set(DARK))

    def test_wedone_blue_is_the_primary_accent(self):
        self.assertEqual(LIGHT["primary"], "#0672BC")
        self.assertEqual(DARK["primary"], "#2996D8")

    def test_stylesheets_are_generated_for_both_themes(self):
        for theme in ("light", "dark"):
            with self.subTest(theme=theme):
                stylesheet = get_stylesheet(theme)
                self.assertIn("DM Sans", stylesheet)
                self.assertIn("Manrope", stylesheet)
                self.assertIn("QPushButton", stylesheet)
                self.assertIn("QLineEdit", stylesheet)

    def test_unknown_theme_falls_back_to_light(self):
        self.assertEqual(get_stylesheet("unexpected"), get_stylesheet("light"))


if __name__ == "__main__":
    unittest.main()

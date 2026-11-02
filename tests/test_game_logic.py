import unittest
from unittest.mock import patch

from ui.screen_game import GameScreen


class ArithmeticGenerationTests(unittest.TestCase):
    def test_subtraction_never_requests_an_invalid_random_range(self):
        def checked_randint(low, high):
            self.assertLessEqual(low, high)
            return low

        with patch("ui.screen_game.random.randint", side_effect=checked_randint):
            a, b, result, symbol = GameScreen._make_op(
                "soustraction", (1, 9999, 2, 9998)
            )

        self.assertGreaterEqual(a, 2)
        self.assertGreaterEqual(b, 2)
        self.assertLessEqual(b, a)
        self.assertEqual(result, a - b)
        self.assertEqual(symbol, "−")


if __name__ == "__main__":
    unittest.main()

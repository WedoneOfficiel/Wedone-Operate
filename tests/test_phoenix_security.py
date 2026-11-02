"""Tests for local teacher credential hashing."""

import unittest

from phoenix.security import hash_password, verify_password


class TeacherPasswordTests(unittest.TestCase):
    def test_password_is_salted_and_verifiable(self):
        first = hash_password("CorrectHorseBattery!")
        second = hash_password("CorrectHorseBattery!")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("CorrectHorseBattery!", first))
        self.assertFalse(verify_password("wrong password", first))

    def test_weak_password_is_rejected(self):
        with self.assertRaises(ValueError):
            hash_password("short")

    def test_malformed_hash_is_rejected(self):
        self.assertFalse(verify_password("password", "not-a-hash"))


if __name__ == "__main__":
    unittest.main()

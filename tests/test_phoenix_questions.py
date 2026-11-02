"""Tests for Phoenix curriculum metadata and arithmetic generators."""

import unittest

from phoenix.domain.curriculum import LEVELS, get_skill, skills_for_level
from phoenix.domain.questions import check_answer, generate_question, generate_session


class PhoenixCurriculumTests(unittest.TestCase):
    def test_catalogue_spans_cp_to_terminal(self):
        self.assertEqual(LEVELS[0].id, "CP")
        self.assertEqual(LEVELS[-1].id, "Tle_GT")

    def test_disabled_skills_are_not_offered_by_default(self):
        self.assertEqual(skills_for_level("4e"), ())
        self.assertEqual(len(skills_for_level("4e", include_disabled=True)), 2)

    def test_unknown_level_and_skill_fail_explicitly(self):
        with self.assertRaises(ValueError):
            skills_for_level("CM9")
        with self.assertRaises(ValueError):
            get_skill("unknown.skill")


class PhoenixQuestionTests(unittest.TestCase):
    def test_seeded_question_is_reproducible(self):
        first = generate_question("cp.addition_20", difficulty=2, seed=42)
        second = generate_question("cp.addition_20", difficulty=2, seed=42)
        self.assertEqual(first, second)
        self.assertLessEqual(first.answer, 20)

    def test_arithmetic_operations_are_correct(self):
        cases = [
            ("cp.addition_20", 2),
            ("cp.subtraction_20", 2),
            ("ce2.multiplication_tables", 2),
            ("cm2.division_exact", 2),
            ("college.signed_addition", 4),
            ("college.signed_multiplication", 4),
        ]
        for skill_id, difficulty in cases:
            with self.subTest(skill=skill_id):
                question = generate_question(skill_id, difficulty, seed=17)
                a, b = question.operands
                expected = {
                    "addition": a + b,
                    "subtraction": a - b,
                    "multiplication": a * b,
                    "division": a // b,
                    "signed_addition": a + b,
                    "signed_multiplication": a * b,
                }[question.operation]
                self.assertEqual(question.answer, expected)
                if question.operation == "division":
                    self.assertEqual(a % b, 0)

    def test_session_is_seeded_and_avoids_duplicates(self):
        first = generate_session("ce1.addition_100", 12, difficulty=3, seed=9)
        second = generate_session("ce1.addition_100", 12, difficulty=3, seed=9)
        self.assertEqual(first, second)
        self.assertEqual(len({q.signature for q in first}), 12)

    def test_invalid_counts_and_unsupported_skills_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_session("cp.addition_20", 0)
        with self.assertRaises(ValueError):
            generate_question("college.proportionality", seed=1)

    def test_answer_validation(self):
        question = generate_question("cp.addition_20", seed=2)
        self.assertTrue(check_answer(question, str(question.answer)))
        self.assertFalse(check_answer(question, "not a number"))
        self.assertFalse(check_answer(question, str(question.answer + 1)))


if __name__ == "__main__":
    unittest.main()

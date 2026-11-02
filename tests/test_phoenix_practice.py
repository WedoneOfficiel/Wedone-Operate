"""Integration tests for persisted Phoenix practice sessions."""

import tempfile
import unittest
from pathlib import Path

from phoenix.storage.database import Database
from phoenix.storage.practice_repository import PracticeRepository


class PracticeRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp.name) / "phoenix.sqlite3")
        self.database.initialize()
        self.repository = PracticeRepository(self.database)

    def tearDown(self):
        self.temp.cleanup()

    def test_individual_session_can_be_completed(self):
        session_id = self.repository.start_session(
            "individual", 2, {"skill_id": "cp.addition_20"}
        )
        self.assertTrue(self.repository.record_answer(
            session_id, "cp.addition_20", "2 + 3 = ?", 5, "5", 900
        ))
        self.assertFalse(self.repository.record_answer(
            session_id, "cp.addition_20", "4 + 2 = ?", 6, "7", 1200
        ))
        result = self.repository.finish_session(session_id)
        self.assertEqual(result, {"status": "completed", "answered": 2, "correct": 1})
        saved = self.repository.get_session(session_id)
        self.assertEqual(saved["status"], "completed")
        self.assertEqual(len(saved["answers"]), 2)

    def test_abandoning_keeps_partial_answers(self):
        session_id = self.repository.start_session(
            "individual", 5, {"skill_id": "ce1.addition_100"}
        )
        self.repository.record_answer(
            session_id, "ce1.addition_100", "20 + 10 = ?", 30, "30", 700
        )
        result = self.repository.abandon_session(session_id)
        self.assertEqual(result["status"], "abandoned")
        self.assertEqual(result["answered"], 1)
        saved = self.repository.get_session(session_id)
        self.assertEqual(len(saved["answers"]), 1)
        self.assertEqual(saved["answers"][0]["given_answer"], "30")

    def test_session_cannot_finish_before_all_questions_are_answered(self):
        session_id = self.repository.start_session(
            "individual", 2, {"skill_id": "cp.addition_20"}
        )
        self.repository.record_answer(
            session_id, "cp.addition_20", "1 + 1 = ?", 2, "2"
        )
        with self.assertRaises(ValueError):
            self.repository.finish_session(session_id)

    def test_answering_finished_session_is_rejected(self):
        session_id = self.repository.start_session(
            "individual", 1, {"skill_id": "cp.addition_20"}
        )
        self.repository.record_answer(
            session_id, "cp.addition_20", "1 + 1 = ?", 2, "2"
        )
        self.repository.finish_session(session_id)
        with self.assertRaises(ValueError):
            self.repository.record_answer(
                session_id, "cp.addition_20", "2 + 2 = ?", 4, "4"
            )

    def test_classroom_allows_quick_practice_without_profile(self):
        session_id = self.repository.start_session("classroom", 5, {})
        saved = self.repository.get_session(session_id)
        self.assertEqual(saved["mode"], "classroom")
        self.assertIsNone(saved["student_id"])

    def test_invalid_session_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            self.repository.start_session("guest", 3, {})
        with self.assertRaises(ValueError):
            self.repository.start_session("individual", 0, {})


if __name__ == "__main__":
    unittest.main()

"""Tests for question-weighted student and individual progress."""

import tempfile
import unittest
from pathlib import Path

from phoenix.storage.classroom_repository import ClassroomRepository
from phoenix.storage.database import Database
from phoenix.storage.practice_repository import PracticeRepository
from phoenix.storage.progress_repository import ProgressRepository


class ProgressRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp.name) / "phoenix.sqlite3")
        self.database.initialize()
        self.practice = PracticeRepository(self.database)
        self.classroom = ClassroomRepository(self.database)
        self.progress = ProgressRepository(self.database)

    def tearDown(self):
        self.temp.cleanup()

    def test_individual_accuracy_is_question_weighted(self):
        first = self.practice.start_session("individual", 4, {})
        self.practice.record_answer(first, "cp.addition_20", "1+1", 2, "2", 500)
        self.practice.record_answer(first, "cp.addition_20", "2+2", 4, "3", 700)
        self.practice.abandon_session(first)

        second = self.practice.start_session("individual", 1, {})
        self.practice.record_answer(second, "ce1.addition_100", "10+5", 15, "15", 600)
        self.practice.finish_session(second)

        summary = self.progress.overview("individual")
        self.assertEqual(summary["sessions"], 2)
        self.assertEqual(summary["completed"], 1)
        self.assertEqual(summary["abandoned"], 1)
        self.assertEqual(summary["answered"], 3)
        self.assertEqual(summary["correct"], 2)
        self.assertEqual(summary["accuracy"], 66.7)
        self.assertEqual(summary["elapsed_ms"], 1800)
        self.assertEqual(len(summary["skills"]), 2)

    def test_classroom_progress_is_scoped_to_selected_student(self):
        class_id = self.classroom.create_class("CM1")
        student_a = self.classroom.create_student(class_id, "A")
        student_b = self.classroom.create_student(class_id, "B")
        session = self.practice.start_session("classroom", 1, {}, student_id=student_a)
        self.practice.record_answer(session, "ce1.addition_100", "1+1", 2, "2")
        self.practice.finish_session(session)

        a_summary = self.progress.overview("classroom", student_a)
        b_summary = self.progress.overview("classroom", student_b)
        self.assertEqual(a_summary["answered"], 1)
        self.assertEqual(a_summary["accuracy"], 100.0)
        self.assertEqual(b_summary["answered"], 0)
        self.assertIsNone(b_summary["accuracy"])

    def test_classroom_requires_a_student_for_personal_progress(self):
        with self.assertRaises(ValueError):
            self.progress.overview("classroom")
        with self.assertRaises(ValueError):
            self.progress.overview("unknown")


if __name__ == "__main__":
    unittest.main()

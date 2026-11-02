"""Tests for class, group and student persistence."""

import tempfile
import unittest
from pathlib import Path

from phoenix.storage.classroom_repository import ClassroomRepository
from phoenix.storage.database import Database


class ClassroomRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp.name) / "phoenix.sqlite3")
        self.database.initialize()
        self.repository = ClassroomRepository(self.database)

    def tearDown(self):
        self.temp.cleanup()

    def test_class_group_and_student_creation(self):
        class_id = self.repository.create_class("CM1 A", "2026-2027")
        group_id = self.repository.create_group(class_id, "Groupe bleu")
        student_id = self.repository.create_student(class_id, "Camille", group_id)
        self.assertEqual(self.repository.list_classes()[0]["name"], "CM1 A")
        self.assertEqual(self.repository.list_groups(class_id)[0]["id"], group_id)
        students = self.repository.list_students(class_id, group_id)
        self.assertEqual([student["id"] for student in students], [student_id])

    def test_group_must_belong_to_selected_class(self):
        first = self.repository.create_class("CM1")
        second = self.repository.create_class("CM2")
        group_id = self.repository.create_group(first, "Groupe A")
        with self.assertRaises(ValueError):
            self.repository.create_student(second, "Élève", group_id)

    def test_empty_names_are_rejected(self):
        with self.assertRaises(ValueError):
            self.repository.create_class("   ")
        with self.assertRaises(ValueError):
            self.repository.create_teacher("")
        class_id = self.repository.create_class("Sixième")
        with self.assertRaises(ValueError):
            self.repository.create_student(class_id, " ")

    def test_archive_hides_student_without_erasing_history(self):
        class_id = self.repository.create_class("CE2")
        student_id = self.repository.create_student(class_id, "Alex")
        self.repository.archive_student(student_id)
        self.assertEqual(self.repository.list_students(class_id), [])
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT archived_at FROM students WHERE id=?", (student_id,)
            ).fetchone()
        self.assertIsNotNone(row["archived_at"])

    def test_teacher_profile_can_be_edited(self):
        teacher_id = self.repository.create_teacher("Professeur A")
        self.repository.update_teacher(teacher_id, "Professeur B")
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT display_name FROM teachers WHERE id=?", (teacher_id,)
            ).fetchone()
        self.assertEqual(row["display_name"], "Professeur B")


if __name__ == "__main__":
    unittest.main()

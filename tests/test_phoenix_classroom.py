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
            self.repository.create_teacher("", "MotDePasse123!")
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

    def test_archiving_group_and_class_hides_them_without_erasing_records(self):
        class_id = self.repository.create_class("CM1")
        group_id = self.repository.create_group(class_id, "Groupe rouge")
        self.repository.archive_group(group_id)
        self.assertEqual(self.repository.list_groups(class_id), [])
        with self.database.connect() as connection:
            archived_group = connection.execute(
                "SELECT archived_at FROM groups WHERE id=?", (group_id,)
            ).fetchone()
        self.assertIsNotNone(archived_group["archived_at"])

        self.repository.archive_class(class_id)
        self.assertEqual(self.repository.list_classes(), [])
        with self.database.connect() as connection:
            archived_class = connection.execute(
                "SELECT archived_at FROM classes WHERE id=?", (class_id,)
            ).fetchone()
        self.assertIsNotNone(archived_class["archived_at"])

    def test_teacher_can_assign_exercises_only_to_owned_classes(self):
        teacher = self.repository.create_teacher("Professeur A", "MotDePasse123!")
        other_teacher = self.repository.create_teacher("Professeur B", "MotDePasse456!")
        class_id = self.repository.create_class("CM1 A", owner_teacher_id=teacher)
        other_class = self.repository.create_class("CM2 B", owner_teacher_id=other_teacher)
        student_id = self.repository.create_student(class_id, "Camille")

        plan_id = self.repository.create_exercise_plan(
            class_id, teacher, "Révisions", "cp.addition_20", 10, 2
        )
        plans = self.repository.list_exercise_plans(class_id, teacher)
        self.assertEqual([plan["id"] for plan in plans], [plan_id])
        self.assertEqual(
            self.repository.get_exercise_plan_for_student(plan_id, student_id)["name"],
            "Révisions",
        )
        self.assertIsNone(
            self.repository.get_exercise_plan_for_student(
                plan_id, self.repository.create_student(other_class, "Alex")
            )
        )
        with self.assertRaises(ValueError):
            self.repository.create_exercise_plan(
                other_class, teacher, "Interdit", "cp.addition_20", 10, 2
            )
        with self.assertRaises(ValueError):
            self.repository.create_exercise_plan(
                class_id, teacher, "Compétence indisponible",
                "college.proportionality", 10, 2
            )
        self.repository.archive_exercise_plan(plan_id, teacher)
        self.assertEqual(self.repository.list_exercise_plans(class_id, teacher), [])

    def test_group_and_student_edits_are_scoped_to_teacher(self):
        teacher = self.repository.create_teacher("Professeur A", "MotDePasse123!")
        other_teacher = self.repository.create_teacher("Professeur B", "MotDePasse456!")
        class_id = self.repository.create_class("CM1 A", owner_teacher_id=teacher)
        other_class = self.repository.create_class("CM2 B", owner_teacher_id=other_teacher)
        group_id = self.repository.create_group(class_id, "Groupe bleu", teacher)
        student_id = self.repository.create_student(class_id, "Camille", group_id, teacher)
        self.repository.update_group(group_id, "Groupe vert", teacher)
        self.repository.update_student(student_id, "Camille B", teacher)
        with self.assertRaises(ValueError):
            self.repository.update_group(group_id, "Interdit", other_teacher)
        with self.assertRaises(ValueError):
            self.repository.update_student(student_id, "Interdit", other_teacher)
        self.assertEqual(self.repository.list_groups(class_id, teacher)[0]["name"], "Groupe vert")
        self.assertEqual(
            self.repository.list_students(class_id, teacher_id=teacher)[0]["display_name"],
            "Camille B",
        )

    def test_teacher_classes_are_scoped_and_protected(self):
        first_teacher = self.repository.create_teacher("Professeur A", "MotDePasse123!")
        second_teacher = self.repository.create_teacher("Professeur B", "MotDePasse456!")
        first_class = self.repository.create_class("CM1 A", owner_teacher_id=first_teacher)
        second_class = self.repository.create_class("CM2 B", owner_teacher_id=second_teacher)

        self.assertEqual(
            [item["id"] for item in self.repository.list_classes(first_teacher)],
            [first_class],
        )
        self.assertEqual(
            [item["id"] for item in self.repository.list_classes(second_teacher)],
            [second_class],
        )
        with self.assertRaises(ValueError):
            self.repository.create_group(second_class, "Groupe interdit", first_teacher)
        with self.assertRaises(ValueError):
            self.repository.create_student(
                second_class, "Élève interdit", teacher_id=first_teacher
            )
        with self.assertRaises(ValueError):
            self.repository.archive_class(second_class, first_teacher)

    def test_legacy_classes_are_claimed_by_first_teacher(self):
        legacy_class = self.repository.create_class("Classe historique")
        teacher_id = self.repository.create_teacher("Professeur", "MotDePasse123!")
        self.assertEqual(self.repository.claim_unowned_classes(teacher_id), 1)
        self.assertEqual(
            [item["id"] for item in self.repository.list_classes(teacher_id)],
            [legacy_class],
        )

    def test_teacher_profile_can_be_edited(self):
        teacher_id = self.repository.create_teacher("Professeur A", "MotDePasse123!")
        self.assertTrue(self.repository.authenticate_teacher(teacher_id, "MotDePasse123!"))
        self.assertFalse(self.repository.authenticate_teacher(teacher_id, "incorrect"))
        self.repository.update_teacher(teacher_id, "Professeur B")
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT display_name FROM teachers WHERE id=?", (teacher_id,)
            ).fetchone()
        self.assertEqual(row["display_name"], "Professeur B")


if __name__ == "__main__":
    unittest.main()

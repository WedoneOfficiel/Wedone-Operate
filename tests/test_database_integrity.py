import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database as db


class DatabaseIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patch = patch.object(db, "data_file", side_effect=lambda name: self.root / name)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_student_can_belong_to_class_without_group(self):
        cls = db.add_class("CM1 A", "teacher-a")
        student = db.add_student("Camille", "Martin", "teacher-a", class_id=cls["id"])
        self.assertIsNotNone(student)
        self.assertIsNone(student["group_id"])
        self.assertEqual([student["id"]], [s["id"] for s in db.get_students(class_id=cls["id"])])
        self.assertEqual([student["id"]], [s["id"] for s in db.get_students(teacher_id="teacher-a")])

    def test_same_student_name_allowed_in_separate_teacher_workspaces(self):
        first = db.add_student("Alex", "Martin", "teacher-a")
        second = db.add_student("Alex", "Martin", "teacher-b")
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertNotEqual(first["id"], second["id"])
        self.assertIsNone(db.add_student("Alex", "Martin", "teacher-a"))

    def test_removing_teacher_preserves_students_and_scores(self):
        student = db.add_student("Lou", "Durand", "teacher-a")
        db.save_score(student["id"], "CM2", 10, 8, False, ["addition"])
        db.add_class("CM2", "teacher-a")
        db.add_group("Groupe 1", "teacher-a")
        db.save_template("Entraînement", "teacher-a", {"operations": ["addition"]})
        db.remove_teacher("teacher-a")
        retained = db.get_student(student["id"])
        self.assertEqual("guest", retained["created_by"])
        self.assertEqual([], db.get_classes(owner_id="teacher-a"))
        self.assertEqual([], db.get_groups(owner_id="teacher-a"))
        self.assertEqual([], db.get_templates(owner_id="teacher-a"))
        self.assertEqual(1, len(db.get_scores(student["id"])))

    def test_csv_export_quotes_commas_and_accents(self):
        student = db.add_student("Éloïse, Anne", 'O"Neil', "teacher-a")
        group = db.add_group("Groupe, A", "teacher-a")
        db.assign_student_group(student["id"], group["id"])
        db.save_score(student["id"], "CM2", 10, 9, False, ["addition"])
        rows = list(csv.reader(db.export_group_csv(group["id"]).splitlines()))
        self.assertEqual("Éloïse, Anne", rows[1][0])
        self.assertEqual('O"Neil', rows[1][1])

    def test_corrupt_json_is_not_silently_replaced(self):
        (self.root / db.USERS_FILE).write_text("{broken", encoding="utf-8")
        with self.assertRaises(db.DataIntegrityError):
            db._load(db.USERS_FILE, {})
        self.assertEqual("{broken", (self.root / db.USERS_FILE).read_text(encoding="utf-8"))

    def test_save_replaces_json_with_valid_complete_document(self):
        db._save("sample.json", {"ok": True, "items": [1, 2, 3]})
        self.assertEqual({"ok": True, "items": [1, 2, 3]}, db._load("sample.json", {}))
        self.assertEqual([], list(self.root.glob("*.tmp")))


if __name__ == "__main__":
    unittest.main()

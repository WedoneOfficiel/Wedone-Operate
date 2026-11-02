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

    def test_same_name_is_allowed_in_different_classes(self):
        first_class = db.add_class("CM1", "teacher-a")
        second_class = db.add_class("CM2", "teacher-a")
        first = db.add_student("Alex", "Martin", "teacher-a", class_id=first_class["id"])
        second = db.add_student("Alex", "Martin", "teacher-a", class_id=second_class["id"])
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertNotEqual(first["id"], second["id"])

    def test_removing_group_keeps_students_in_their_class_and_detaches_templates(self):
        cls = db.add_class("6e A", "teacher-a")
        group = db.add_group("Groupe A", "teacher-a", class_id=cls["id"])
        student = db.add_student("Mina", "Petit", "teacher-a", group_id=group["id"])
        db.save_template("Révisions", "teacher-a", {"operations": ["addition"]}, group_id=group["id"])
        db.remove_group(group["id"])
        retained = db.get_student(student["id"])
        self.assertIsNone(retained["group_id"])
        self.assertEqual(cls["id"], retained["class_id"])
        self.assertEqual([student["id"]], [s["id"] for s in db.get_students(class_id=cls["id"])])
        self.assertIsNone(db.get_templates(owner_id="teacher-a")[0]["group_id"])

    def test_removing_teacher_preserves_students_and_scores(self):
        student = db.add_student("Lou", "Durand", "teacher-a")
        db.save_score(student["id"], "CM2", 10, 8, False, ["addition"])
        db.add_class("CM2", "teacher-a")
        db.add_group("Groupe 1", "teacher-a")
        db.save_template("Entraînement", "teacher-a", {"operations": ["addition"]})
        db.remove_teacher("teacher-a")
        retained = db.get_student(student["id"])
        self.assertEqual("guest", retained["created_by"])
        self.assertEqual("guest", db.get_classes(owner_id="guest")[0]["owner_id"])
        self.assertEqual("guest", db.get_groups(owner_id="guest")[0]["owner_id"])
        self.assertEqual("guest", db.get_templates(owner_id="guest")[0]["owner_id"])
        self.assertEqual(1, len(db.get_scores(student["id"])))

    def test_csv_export_quotes_commas_and_accents(self):
        student = db.add_student("Éloïse, Anne", 'O"Neil', "teacher-a")
        group = db.add_group("Groupe, A", "teacher-a")
        db.assign_student_group(student["id"], group["id"])
        db.save_score(student["id"], "CM2", 10, 9, False, ["addition"])
        rows = list(csv.reader(db.export_group_csv(group["id"]).splitlines()))
        self.assertEqual("Éloïse, Anne", rows[1][0])
        self.assertEqual('O"Neil', rows[1][1])

    def test_first_teacher_adopts_legacy_admin_workspace(self):
        cls = db.add_class("CM2 A", "admin")
        group = db.add_group("Groupe 1", "admin", class_id=cls["id"])
        student = db.add_student("Noa", "Petit", "admin", group_id=group["id"])
        db.save_template("Révisions", "admin", {"operations": ["addition"]}, group_id=group["id"])
        teacher = db.add_teacher("Marie", "Curie", "motdepasse123")
        self.assertEqual(teacher["id"], db.get_class(cls["id"])["owner_id"])
        self.assertEqual(teacher["id"], db.get_group(group["id"])["owner_id"])
        self.assertEqual(teacher["id"], db.get_student(student["id"])["created_by"])
        self.assertEqual(teacher["id"], db.get_templates(owner_id=teacher["id"])[0]["owner_id"])

    def test_teacher_password_uses_salted_pbkdf2(self):
        teacher = db.add_teacher("Ada", "Lovelace", "un-mot-de-passe")
        stored = db.get_teacher(teacher["id"])["password_hash"]
        self.assertTrue(stored.startswith("pbkdf2_sha256$"))
        self.assertTrue(db.check_teacher_password(teacher["id"], "un-mot-de-passe"))
        self.assertFalse(db.check_teacher_password(teacher["id"], "incorrect"))

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

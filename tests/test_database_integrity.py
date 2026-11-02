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

    def test_class_level_applies_to_students_without_groups(self):
        cls = db.add_class("CE2 A", "teacher-a", level="CE2")
        student = db.add_student("Inès", "Petit", "teacher-a", class_id=cls["id"])
        self.assertEqual("CE2", db.get_student_level(student["id"]))

    def test_group_level_overrides_class_level(self):
        cls = db.add_class("CM2 B", "teacher-a", level="CM2")
        group = db.add_group("Groupe CE1", "teacher-a", level="CE1", class_id=cls["id"])
        student = db.add_student("Noé", "Martin", "teacher-a", group_id=group["id"])
        self.assertEqual("CE1", db.get_student_level(student["id"]))

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
        group = db.add_group("Groupe A", "teacher-a", level="CE1", class_id=cls["id"])
        student = db.add_student("Mina", "Petit", "teacher-a", group_id=group["id"])
        db.save_template("Révisions", "teacher-a", {"operations": ["addition"]}, group_id=group["id"])
        db.remove_group(group["id"])
        retained = db.get_student(student["id"])
        self.assertIsNone(retained["group_id"])
        self.assertEqual("CE1", retained["level"])
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

    def test_class_template_applies_to_students_without_groups(self):
        cls = db.add_class("CM1 A", "teacher-a")
        student = db.add_student("Lina", "Martin", "teacher-a", class_id=cls["id"])
        self.assertTrue(db.save_template(
            "Entraînement CM1", "teacher-a",
            {"operations": ["addition"], "level": "CM1"},
            class_id=cls["id"]
        ))
        template = db.get_student_default_template(student["id"])
        self.assertEqual("Entraînement CM1", template["name"])

    def test_group_template_overrides_class_template(self):
        cls = db.add_class("CM2 A", "teacher-a")
        group = db.add_group("Groupe rapide", "teacher-a", class_id=cls["id"])
        student = db.add_student("Noé", "Petit", "teacher-a", group_id=group["id"])
        db.save_template("Classe", "teacher-a", {"operations": ["addition"]}, class_id=cls["id"])
        db.save_template("Groupe", "teacher-a", {"operations": ["multiplication"]}, group_id=group["id"])
        self.assertEqual("Groupe", db.get_student_default_template(student["id"])["name"])

    def test_removing_group_promotes_its_template_to_class_scope(self):
        cls = db.add_class("CE2 A", "teacher-a")
        group = db.add_group("Groupe A", "teacher-a", class_id=cls["id"])
        student = db.add_student("Milo", "Durand", "teacher-a", group_id=group["id"])
        db.save_template("Travail du groupe", "teacher-a",
                         {"operations": ["soustraction"]}, group_id=group["id"])
        db.remove_group(group["id"])
        template = db.get_student_default_template(student["id"])
        self.assertEqual("Travail du groupe", template["name"])
        self.assertEqual(cls["id"], template["class_id"])

    def test_editing_group_updates_members_level_and_class(self):
        cls_a = db.add_class("CM1 A", "teacher-a")
        cls_b = db.add_class("CM2 B", "teacher-a")
        group = db.add_group("Groupe A", "teacher-a", level="CM1", class_id=cls_a["id"])
        student = db.add_student("Mina", "Petit", "teacher-a", group_id=group["id"])
        self.assertTrue(db.update_group(group["id"], name="Groupe avancé", level="CM2", class_id=cls_b["id"]))
        updated = db.get_student(student["id"])
        self.assertEqual("Groupe avancé", db.get_group(group["id"])["name"])
        self.assertEqual("CM2", db.get_student_level(student["id"]))
        self.assertEqual(cls_b["id"], updated["class_id"])

    def test_editing_student_preserves_score_history(self):
        cls = db.add_class("CM2 A", "teacher-a")
        student = db.add_student("Léa", "Martin", "teacher-a", class_id=cls["id"])
        db.save_score(student["id"], "CM2", 10, 8, False, ["addition"])
        self.assertTrue(db.update_student(student["id"], "Lea", "Durand", cls["id"], None))
        self.assertEqual("Lea", db.get_student(student["id"])["prenom"])
        self.assertEqual(1, len(db.get_scores(student["id"])))

    def test_editing_template_renames_by_id_without_duplicate(self):
        db.save_template("Révisions", "teacher-a", {"operations": ["addition"]})
        template = db.get_templates(owner_id="teacher-a")[0]
        self.assertTrue(db.update_template(template["id"], "Entraînement", {"operations": ["division"]}))
        templates = db.get_templates(owner_id="teacher-a")
        self.assertEqual(1, len(templates))
        self.assertEqual("Entraînement", templates[0]["name"])
        self.assertEqual(["division"], templates[0]["config"]["operations"])

    def test_editing_class_updates_ungrouped_student_level(self):
        cls = db.add_class("CM1 A", "teacher-a", level="CM1")
        student = db.add_student("Inès", "Petit", "teacher-a", class_id=cls["id"])
        self.assertTrue(db.update_class(cls["id"], "CM2 A", "CM2"))
        self.assertEqual("CM2", db.get_student_level(student["id"]))

    def test_editing_teacher_can_change_identity_and_password(self):
        teacher = db.add_teacher("Ada", "Lovelace", "ancien-secret")
        self.assertTrue(db.update_teacher(teacher["id"], "Ada", "Byron", "nouveau-secret"))
        self.assertEqual("Byron", db.get_teacher(teacher["id"])["nom"])
        self.assertTrue(db.check_teacher_password(teacher["id"], "nouveau-secret"))

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

    def test_legacy_admin_data_migrates_when_teacher_profiles_already_exist(self):
        first = db.add_teacher("Alice", "Martin", "motdepasse123")
        cls = db.add_class("5e B", "admin")
        student = db.add_student("Sam", "Durand", "admin", class_id=cls["id"])
        db.add_teacher("Bob", "Durand", "motdepasse456")
        self.assertEqual(first["id"], db.get_class(cls["id"])["owner_id"])
        self.assertEqual(first["id"], db.get_student(student["id"])["created_by"])

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

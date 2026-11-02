"""Entry point for the Phoenix Qt Quick app and its local workflows."""

from __future__ import annotations

import csv
import json
import sys
from time import perf_counter_ns
from pathlib import Path

from .domain.questions import Question, generate_session
from .domain.curriculum import SKILLS
from .storage import (
    ClassroomRepository,
    Database,
    PracticeRepository,
    ProgressRepository,
    get_database_path,
    get_phoenix_data_dir,
    export_json,
    import_json,
    reset_data,
)
from .storage.backup import create_backup, restore_backup
from datetime import datetime


def main(argv: list[str] | None = None) -> int:
    try:
        from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot, QCoreApplication, QTimer, qInstallMessageHandler
        from PySide6.QtGui import QGuiApplication, QIcon, QImageReader, QPalette, QColor
        from PySide6.QtQuick import QQuickImageProvider
        from PySide6.QtQml import QQmlApplicationEngine
    except ImportError as exc:
        raise SystemExit(
            "L'interface Phoenix nécessite PySide6. Installez requirements-phoenix.txt."
        ) from exc

    args = list(sys.argv[1:] if argv is None else argv)
    smoke_test = "--smoke-test" in args
    qt_args = [sys.argv[0]]

    class AppBridge(QObject):
        modeChanged = Signal(str)
        practiceChanged = Signal()
        classroomChanged = Signal()
        settingsChanged = Signal()
        progressChanged = Signal()

        def __init__(self, database: Database):
            super().__init__()
            self._database = database
            self._practice = PracticeRepository(database)
            self._classroom = ClassroomRepository(database)
            self._progress = ProgressRepository(database)
            self._mode = database.get_mode() or ""
            self._questions: tuple[Question, ...] = ()
            self._session_id: str | None = None
            self._question_index = 0
            self._answered = False
            self._finished = False
            self._feedback = ""
            self._score_text = ""
            self._question_started_ns: int | None = None
            self._teacher_id: str | None = None
            self._active_student_id: str | None = None
            self._classroom_message = ""
            self._classroom_revision = 0
            self._ui_scale = float(database.get_setting("ui_scale", 1.0))
            self._high_contrast = bool(database.get_setting("high_contrast", False))
            self._theme_mode = str(database.get_setting("theme_mode", "dark"))
            if self._theme_mode not in ("system", "light", "dark"):
                self._theme_mode = "dark"
            self._reduce_motion = bool(database.get_setting("reduce_motion", False))
            self._data_message = ""

        @Property(str, notify=modeChanged)
        def mode(self) -> str:
            return self._mode

        @Property(str, notify=practiceChanged)
        def questionPrompt(self) -> str:
            if not self._questions or self._finished:
                return ""
            return self._questions[self._question_index].prompt

        @Property(int, notify=practiceChanged)
        def questionNumber(self) -> int:
            return self._question_index + 1 if self._questions else 0

        @Property(int, notify=practiceChanged)
        def questionTotal(self) -> int:
            return len(self._questions)

        @Property(bool, notify=practiceChanged)
        def answerSubmitted(self) -> bool:
            return self._answered

        @Property(bool, notify=practiceChanged)
        def practiceFinished(self) -> bool:
            return self._finished

        @Property(str, notify=practiceChanged)
        def feedback(self) -> str:
            return self._feedback

        @Property(str, notify=practiceChanged)
        def scoreText(self) -> str:
            return self._score_text

        @Property(bool, notify=classroomChanged)
        def teacherAuthenticated(self) -> bool:
            return self._teacher_id is not None

        @Property(int, notify=classroomChanged)
        def classroomRevision(self) -> int:
            return self._classroom_revision

        @Property(str, notify=classroomChanged)
        def teachersJson(self) -> str:
            return json.dumps(self._classroom.list_teachers(), ensure_ascii=False)

        @Property(str, notify=classroomChanged)
        def classesJson(self) -> str:
            return json.dumps(
                self._classroom.list_classes(self._teacher_id),
                ensure_ascii=False,
            )

        @Property(str, notify=classroomChanged)
        def allClassesJson(self) -> str:
            return json.dumps(self._classroom.list_classes(), ensure_ascii=False)

        @Property(str, notify=classroomChanged)
        def skillsJson(self) -> str:
            return json.dumps(
                [
                    {"id": skill.id, "label": f"{skill.level_id} · {skill.label}"}
                    for skill in SKILLS if skill.enabled
                ],
                ensure_ascii=False,
            )

        @Property(str, notify=classroomChanged)
        def classroomMessage(self) -> str:
            return self._classroom_message

        @Property(float, notify=settingsChanged)
        def uiScale(self) -> float:
            return self._ui_scale

        @Property(bool, notify=settingsChanged)
        def highContrast(self) -> bool:
            return self._high_contrast

        @Property(str, notify=settingsChanged)
        def themeMode(self) -> str:
            return self._theme_mode

        @Property(bool, notify=settingsChanged)
        def systemDark(self) -> bool:
            return system_prefers_dark()

        @Property(bool, notify=settingsChanged)
        def reduceMotion(self) -> bool:
            return self._reduce_motion

        @Property(str, notify=settingsChanged)
        def dataMessage(self) -> str:
            return self._data_message

        @Property(str, notify=progressChanged)
        def progressJson(self) -> str:
            if self._mode == "individual":
                summary = self._progress.overview("individual")
            elif self._mode == "classroom" and self._active_student_id:
                summary = self._progress.overview("classroom", self._active_student_id)
            else:
                summary = {
                    "sessions": 0, "completed": 0, "abandoned": 0,
                    "answered": 0, "correct": 0, "accuracy": None,
                    "elapsed_ms": 0, "recent": [], "skills": [],
                }
            return json.dumps(summary, ensure_ascii=False)

        @Slot(float)
        def setUiScale(self, value: float) -> None:
            self._ui_scale = min(1.25, max(0.85, float(value)))
            self._database.set_setting("ui_scale", self._ui_scale)
            self.settingsChanged.emit()

        @Slot(bool)
        def setHighContrast(self, enabled: bool) -> None:
            self._high_contrast = bool(enabled)
            self._database.set_setting("high_contrast", self._high_contrast)
            apply_application_palette(self._theme_mode, self._high_contrast)
            self.settingsChanged.emit()

        @Slot(str)
        def setThemeMode(self, mode: str) -> None:
            if mode not in ("system", "light", "dark"):
                return
            self._theme_mode = mode
            self._database.set_setting("theme_mode", mode)
            apply_application_palette(self._theme_mode, self._high_contrast)
            self.settingsChanged.emit()

        @Slot(bool)
        def setReduceMotion(self, enabled: bool) -> None:
            self._reduce_motion = bool(enabled)
            self._database.set_setting("reduce_motion", self._reduce_motion)
            self.settingsChanged.emit()

        def _safety_path(self, label: str) -> Path:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            return get_phoenix_data_dir() / "backups" / f"{label}-{stamp}.sqlite3"

        @Slot(str, str)
        def exportClassReport(self, class_id: str, destination: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    rows = self._progress.class_report(class_id, self._teacher_id)
                    columns = (
                        "class_name", "school_year", "student_id", "display_name", "group_name",
                        "sessions", "answered", "correct", "accuracy", "elapsed_ms",
                    )
                    target = Path(destination)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open("w", newline="", encoding="utf-8-sig") as handle:
                        writer = csv.DictWriter(handle, fieldnames=columns)
                        writer.writeheader()
                        writer.writerows(rows)
                    self._classroom_message = f"Rapport CSV exporté : {target}"
                except Exception as exc:
                    self._classroom_message = f"Export du rapport impossible : {exc}"
            self._emit_classroom_changed()

        @Slot()
        def createBackup(self) -> None:
            try:
                path = get_phoenix_data_dir() / "backups" / (
                    "backup-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".sqlite3"
                )
                create_backup(self._database, path)
                self._data_message = f"Sauvegarde créée : {path}"
            except Exception as exc:
                self._data_message = f"Échec de la sauvegarde : {exc}"
            self.settingsChanged.emit()

        @Slot(str)
        def restoreBackup(self, source: str) -> None:
            try:
                path = Path(source)
                restore_backup(self._database, path, self._safety_path("before-restore"))
                self._reload_after_data_change("Sauvegarde restaurée.")
            except Exception as exc:
                self._data_message = f"Restauration impossible : {exc}"
            self.settingsChanged.emit()

        @Slot(str)
        def exportData(self, destination: str) -> None:
            try:
                export_json(self._database, destination)
                self._data_message = f"Export créé : {destination}"
            except Exception as exc:
                self._data_message = f"Export impossible : {exc}"
            self.settingsChanged.emit()

        @Slot(str)
        def importData(self, source: str) -> None:
            try:
                import_json(self._database, source)
                self._reload_after_data_change("Données importées. Une sauvegarde de sécurité a été créée.")
            except Exception as exc:
                self._data_message = f"Import impossible : {exc}"
            self.settingsChanged.emit()

        @Slot()
        def resetData(self) -> None:
            try:
                reset_data(self._database)
                self._reload_after_data_change("Données réinitialisées. Une sauvegarde de sécurité a été créée.")
            except Exception as exc:
                self._data_message = f"Réinitialisation impossible : {exc}"
            self.settingsChanged.emit()

        def _reload_after_data_change(self, message: str) -> None:
            self._mode = self._database.get_mode() or ""
            self._teacher_id = None
            self._active_student_id = None
            self._ui_scale = float(self._database.get_setting("ui_scale", 1.0))
            self._high_contrast = bool(self._database.get_setting("high_contrast", False))
            self._theme_mode = str(self._database.get_setting("theme_mode", "dark"))
            if self._theme_mode not in ("system", "light", "dark"):
                self._theme_mode = "dark"
            apply_application_palette(self._theme_mode, self._high_contrast)
            self._reduce_motion = bool(self._database.get_setting("reduce_motion", False))
            self._data_message = message
            self.modeChanged.emit(self._mode)
            self._emit_classroom_changed()
            self.practiceChanged.emit()
            self.settingsChanged.emit()
            self.progressChanged.emit()

        def _emit_classroom_changed(self) -> None:
            self._classroom_revision += 1
            self.classroomChanged.emit()

        @Slot(str)
        def chooseMode(self, mode: str) -> None:
            if mode not in ("individual", "classroom"):
                return
            self._database.set_mode(mode)
            self._mode = mode
            self.modeChanged.emit(mode)
            self.progressChanged.emit()

        @Slot()
        def returnToModeChoice(self) -> None:
            self._database.set_setting("usage_mode", None)
            self._mode = ""
            self._active_student_id = None
            self._teacher_id = None
            self.modeChanged.emit("")
            self._emit_classroom_changed()
            self.progressChanged.emit()

        @Slot(str, result="QVariantList")
        def groupsForClass(self, class_id: str):
            return self._classroom.list_groups(class_id) if class_id else []

        @Slot(str, result="QVariantList")
        def teacherGroupsForClass(self, class_id: str):
            return (
                self._classroom.list_groups(class_id, self._teacher_id)
                if class_id and self._teacher_id else []
            )

        @Slot(str, str, result="QVariantList")
        def studentsForClass(self, class_id: str, group_id: str):
            if not class_id:
                return []
            return self._classroom.list_students(class_id, group_id or None)

        @Slot(str, str, result="QVariantList")
        def teacherStudentsForClass(self, class_id: str, group_id: str):
            if not class_id or not self._teacher_id:
                return []
            return self._classroom.list_students(
                class_id, group_id or None, self._teacher_id
            )

        @Slot(str, str)
        def createTeacher(self, display_name: str, password: str) -> None:
            try:
                self._teacher_id = self._classroom.create_teacher(display_name, password)
                self._classroom.claim_unowned_classes(self._teacher_id)
                self._classroom_message = "Profil professeur créé. Vous êtes connecté."
            except Exception as exc:
                self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str)
        def loginTeacher(self, teacher_id: str, password: str) -> None:
            if self._classroom.authenticate_teacher(teacher_id, password):
                self._teacher_id = teacher_id
                self._classroom.claim_unowned_classes(teacher_id)
                self._classroom_message = "Connexion réussie."
            else:
                self._classroom_message = "Mot de passe incorrect."
            self._emit_classroom_changed()

        @Slot()
        def logoutTeacher(self) -> None:
            self._teacher_id = None
            self._active_student_id = None
            self._classroom_message = "Vous êtes déconnecté."
            self._emit_classroom_changed()
            self.progressChanged.emit()

        @Slot(str, str)
        def createClass(self, name: str, school_year: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_class(name, school_year or None, self._teacher_id)
                    self._classroom_message = "Classe créée."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str)
        def createGroup(self, class_id: str, name: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_group(class_id, name, self._teacher_id)
                    self._classroom_message = "Groupe créé."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str, str)
        def createStudent(self, class_id: str, display_name: str, group_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_student(class_id, display_name, group_id or None, self._teacher_id)
                    self._classroom_message = "Élève ajouté."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str, str)
        def updateClass(self, class_id: str, name: str, school_year: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.update_class(
                        class_id, name, school_year or None, self._teacher_id
                    )
                    self._classroom_message = "Classe mise à jour."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str)
        def updateGroup(self, group_id: str, name: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.update_group(group_id, name, self._teacher_id)
                    self._classroom_message = "Groupe mis à jour."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, str)
        def updateStudent(self, student_id: str, display_name: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.update_student(
                        student_id, display_name, self._teacher_id
                    )
                    self._classroom_message = "Profil élève mis à jour."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str, result="QVariantList")
        def plansForClass(self, class_id: str):
            return self._classroom.list_exercise_plans(class_id) if class_id else []

        @Slot(str, result="QVariantList")
        def teacherPlansForClass(self, class_id: str):
            return (
                self._classroom.list_exercise_plans(class_id, self._teacher_id)
                if class_id and self._teacher_id else []
            )

        @Slot(str, str, str, int, int)
        def createExercisePlan(
            self, class_id: str, name: str, skill_id: str,
            question_count: int, difficulty: int,
        ) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_exercise_plan(
                        class_id, self._teacher_id, name, skill_id,
                        question_count, difficulty,
                    )
                    self._classroom_message = "Exercice assigné à la classe."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def archiveExercisePlan(self, plan_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.archive_exercise_plan(plan_id, self._teacher_id)
                    self._classroom_message = "Exercice archivé."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def startAssignedPractice(self, plan_id: str) -> None:
            if not self._active_student_id:
                self._classroom_message = "Sélectionnez d'abord un profil élève."
                self._emit_classroom_changed()
                return
            plan = self._classroom.get_exercise_plan_for_student(
                plan_id, self._active_student_id
            )
            if plan is None:
                self._classroom_message = "Cet exercice n'est pas disponible pour cet élève."
                self._emit_classroom_changed()
                return
            configuration = json.loads(plan["configuration_json"])
            self.startPractice(
                configuration["skill_id"],
                int(configuration["question_count"]),
                int(configuration["difficulty"]),
            )

        @Slot(str)
        def archiveStudent(self, student_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.archive_student(student_id, self._teacher_id)
                    if self._active_student_id == student_id:
                        self._active_student_id = None
                        self.progressChanged.emit()
                    self._classroom_message = "Élève archivé. Son historique est conservé."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def archiveGroup(self, group_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.archive_group(group_id, self._teacher_id)
                    self._classroom_message = "Groupe archivé."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def archiveClass(self, class_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.archive_class(class_id, self._teacher_id)
                    self._active_student_id = None
                    self._classroom_message = "Classe archivée. Les résultats restent conservés."
                    self.progressChanged.emit()
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def updateTeacherProfile(self, display_name: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.update_teacher(self._teacher_id, display_name)
                    self._classroom_message = "Profil mis à jour."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self._emit_classroom_changed()

        @Slot(str)
        def selectStudent(self, student_id: str) -> None:
            self._active_student_id = student_id or None
            self._emit_classroom_changed()
            self.progressChanged.emit()

        @Slot(str, int, int)
        def startPractice(self, skill_id: str, count: int, difficulty: int) -> None:
            if self._mode not in ("individual", "classroom"):
                self._feedback = "Choisissez d'abord un mode d'utilisation."
                self.practiceChanged.emit()
                return
            try:
                questions = generate_session(skill_id, count, difficulty, avoid_duplicates=True)
                session_id = self._practice.start_session(
                    self._mode,
                    len(questions),
                    {"skill_id": skill_id, "difficulty": difficulty},
                    student_id=self._active_student_id if self._mode == "classroom" else None,
                )
            except Exception as exc:
                self._questions = ()
                self._session_id = None
                self._feedback = str(exc)
                self.practiceChanged.emit()
                return
            self._questions = questions
            self._session_id = session_id
            self._question_index = 0
            self._answered = False
            self._finished = False
            self._feedback = ""
            self._score_text = ""
            self._question_started_ns = perf_counter_ns()
            self.practiceChanged.emit()

        @Slot(str)
        def submitAnswer(self, response: str) -> None:
            if not self._session_id or not self._questions or self._answered or self._finished:
                return
            question = self._questions[self._question_index]
            elapsed_ms = None
            if self._question_started_ns is not None:
                elapsed_ms = max(0, (perf_counter_ns() - self._question_started_ns) // 1_000_000)
            correct = self._practice.record_answer(
                self._session_id, question.skill_id, question.prompt,
                question.answer, response, elapsed_ms=int(elapsed_ms) if elapsed_ms is not None else None,
            )
            self._answered = True
            self._feedback = (
                "Bonne réponse !" if correct
                else f"Pas tout à fait. La bonne réponse était {question.answer}."
            )
            self.practiceChanged.emit()

        @Slot()
        def nextQuestion(self) -> None:
            if not self._answered or self._finished:
                return
            if self._question_index + 1 < len(self._questions):
                self._question_index += 1
                self._answered = False
                self._feedback = ""
                self._question_started_ns = perf_counter_ns()
            else:
                result = self._practice.finish_session(self._session_id)
                self._finished = True
                self._question_started_ns = None
                self._score_text = (
                    f"{result['correct']} bonne(s) réponse(s) sur {result['answered']}."
                )
            self.practiceChanged.emit()
            self.progressChanged.emit()

        @Slot()
        def abandonPractice(self) -> None:
            if self._session_id and not self._finished:
                self._practice.abandon_session(self._session_id)
            self._questions = ()
            self._session_id = None
            self._question_index = 0
            self._answered = False
            self._finished = False
            self._feedback = ""
            self._score_text = ""
            self._question_started_ns = None
            self.practiceChanged.emit()
            self.progressChanged.emit()

    app = QGuiApplication(qt_args)

    def system_prefers_dark() -> bool:
        try:
            from PySide6.QtCore import Qt
            return app.styleHints().colorScheme == Qt.ColorScheme.Dark
        except (AttributeError, TypeError):
            return app.palette().color(QPalette.ColorRole.Window).lightness() < 128

    def apply_application_palette(theme_mode: str, high_contrast: bool = False) -> None:
        dark = system_prefers_dark() if theme_mode == "system" else theme_mode == "dark"
        palette = app.palette()
        if not dark:
            values = {
                QPalette.ColorRole.Window: "#FFFFFF" if high_contrast else "#F5F8FC",
                QPalette.ColorRole.WindowText: "#0D1B2A" if high_contrast else "#202B3A",
                QPalette.ColorRole.Base: "#FFFFFF" if high_contrast else "#FFFFFF",
                QPalette.ColorRole.AlternateBase: "#F1F5FA",
                QPalette.ColorRole.ToolTipBase: "#FFFFFF",
                QPalette.ColorRole.ToolTipText: "#172A45",
                QPalette.ColorRole.Text: "#0D1B2A" if high_contrast else "#202B3A",
                QPalette.ColorRole.Button: "#EAF2FF",
                QPalette.ColorRole.ButtonText: "#172A45",
                QPalette.ColorRole.Highlight: "#1769D2",
                QPalette.ColorRole.HighlightedText: "#FFFFFF",
            }
        else:
            values = {
                QPalette.ColorRole.Window: "#090F18" if high_contrast else "#151B26",
                QPalette.ColorRole.WindowText: "#FFFFFF" if high_contrast else "#F2F6FC",
                QPalette.ColorRole.Base: "#0C1420" if high_contrast else "#182333",
                QPalette.ColorRole.AlternateBase: "#1B2739",
                QPalette.ColorRole.ToolTipBase: "#1B2739",
                QPalette.ColorRole.ToolTipText: "#F1F5FB",
                QPalette.ColorRole.Text: "#FFFFFF" if high_contrast else "#F2F6FC",
                QPalette.ColorRole.Button: "#203B61",
                QPalette.ColorRole.ButtonText: "#F1F5FB",
                QPalette.ColorRole.Highlight: "#5796FF",
                QPalette.ColorRole.HighlightedText: "#FFFFFF",
            }
        for role, value in values.items():
            palette.setColor(role, QColor(value))
        app.setPalette(palette)

    app.setApplicationName("Wedone Operate Phoenix")
    app.setOrganizationName("WedoneOfficiel")

    def resource_path(name: str) -> Path:
        bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
        return bundle_root / name

    icon_path = resource_path("icon.png")
    if icon_path.is_file():
        app.setWindowIcon(QIcon(str(icon_path)))

    class BrandingImageProvider(QQuickImageProvider):
        def __init__(self):
            super().__init__(QQuickImageProvider.Image)

        def requestImage(self, image_id, size, requested_size):
            reader = QImageReader(str(icon_path))
            image = reader.read()
            if image.isNull():
                image = QIcon(str(icon_path)).pixmap(256, 256).toImage()
            if requested_size.width() > 0 and requested_size.height() > 0:
                image = image.scaled(requested_size)
            if size is not None:
                size.setWidth(image.width())
                size.setHeight(image.height())
            return image

    database = Database(get_database_path())
    database.initialize()
    bridge = AppBridge(database)
    apply_application_palette(bridge.themeMode, bridge.highContrast)

    def on_system_color_scheme_changed(*_args):
        if bridge.themeMode == "system":
            apply_application_palette("system", bridge.highContrast)
            bridge.settingsChanged.emit()

    try:
        app.styleHints().colorSchemeChanged.connect(on_system_color_scheme_changed)
    except (AttributeError, TypeError):
        pass

    engine = QQmlApplicationEngine()
    # Keep the bridge owned by the engine for the entire QML lifetime. This
    # avoids a packaged-runtime wrapper being released while QML still binds it.
    bridge.setParent(engine)
    qt_qml_errors: list[str] = []

    def qt_message_handler(mode, context, message):
        lowered = str(message).lower()
        if any(marker in lowered for marker in (
            "typeerror:", "referenceerror:", "failed to load",
            "is not installed", "no such file or directory",
        )):
            qt_qml_errors.append(str(message))

    if smoke_test:
        qInstallMessageHandler(qt_message_handler)

    if icon_path.is_file():
        engine.addImageProvider("branding", BrandingImageProvider())
    engine.rootContext().setContextProperty("appBridge", bridge)
    qml_file = Path(__file__).parent / "ui" / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file.resolve())))
    if not engine.rootObjects():
        if smoke_test and qt_qml_errors:
            print("Smoke test failed: the QML engine could not create the application window:")
            for message in qt_qml_errors:
                print(f"  {message}")
        return 2
    if smoke_test:
        QCoreApplication.processEvents()
        if engine.rootContext().contextProperty("appBridge") is None:
            print("Smoke test failed: appBridge is not available in the QML root context.")
            return 3
        if qt_qml_errors:
            print("Smoke test failed: QML runtime reported errors:")
            for message in qt_qml_errors:
                print(f"  {message}")
            return 4
        QTimer.singleShot(750, app.quit)
        exit_code = app.exec()
        if qt_qml_errors:
            print("Smoke test failed: QML runtime reported errors:")
            for message in qt_qml_errors:
                print(f"  {message}")
            return 4
        return exit_code
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

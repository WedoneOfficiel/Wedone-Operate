"""Entry point for the Phoenix Qt Quick app and its local workflows."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .domain.questions import Question, generate_session
from .storage import (
    ClassroomRepository,
    Database,
    PracticeRepository,
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
        from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot
        from PySide6.QtGui import QGuiApplication
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

        def __init__(self, database: Database):
            super().__init__()
            self._database = database
            self._practice = PracticeRepository(database)
            self._classroom = ClassroomRepository(database)
            self._mode = database.get_mode() or ""
            self._questions: tuple[Question, ...] = ()
            self._session_id: str | None = None
            self._question_index = 0
            self._answered = False
            self._finished = False
            self._feedback = ""
            self._score_text = ""
            self._teacher_id: str | None = None
            self._active_student_id: str | None = None
            self._classroom_message = ""
            self._ui_scale = float(database.get_setting("ui_scale", 1.0))
            self._high_contrast = bool(database.get_setting("high_contrast", False))
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

        @Property(str, notify=classroomChanged)
        def teachersJson(self) -> str:
            return json.dumps(self._classroom.list_teachers(), ensure_ascii=False)

        @Property(str, notify=classroomChanged)
        def classesJson(self) -> str:
            return json.dumps(self._classroom.list_classes(), ensure_ascii=False)

        @Property(str, notify=classroomChanged)
        def classroomMessage(self) -> str:
            return self._classroom_message

        @Property(float, notify=settingsChanged)
        def uiScale(self) -> float:
            return self._ui_scale

        @Property(bool, notify=settingsChanged)
        def highContrast(self) -> bool:
            return self._high_contrast

        @Property(bool, notify=settingsChanged)
        def reduceMotion(self) -> bool:
            return self._reduce_motion

        @Property(str, notify=settingsChanged)
        def dataMessage(self) -> str:
            return self._data_message

        @Slot(float)
        def setUiScale(self, value: float) -> None:
            self._ui_scale = min(1.25, max(0.85, float(value)))
            self._database.set_setting("ui_scale", self._ui_scale)
            self.settingsChanged.emit()

        @Slot(bool)
        def setHighContrast(self, enabled: bool) -> None:
            self._high_contrast = bool(enabled)
            self._database.set_setting("high_contrast", self._high_contrast)
            self.settingsChanged.emit()

        @Slot(bool)
        def setReduceMotion(self, enabled: bool) -> None:
            self._reduce_motion = bool(enabled)
            self._database.set_setting("reduce_motion", self._reduce_motion)
            self.settingsChanged.emit()

        def _safety_path(self, label: str) -> Path:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            return get_phoenix_data_dir() / "backups" / f"{label}-{stamp}.sqlite3"

        @Slot()
        def createBackup(self) -> None:
            try:
                path = get_phoenix_data_dir() / "backups" / (
                    "backup-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".sqlite3"
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
            self._data_message = message
            self.modeChanged.emit(self._mode)
            self.classroomChanged.emit()
            self.practiceChanged.emit()

        @Slot(str)
        def chooseMode(self, mode: str) -> None:
            if mode not in ("individual", "classroom"):
                return
            self._database.set_mode(mode)
            self._mode = mode
            self.modeChanged.emit(mode)

        @Slot()
        def returnToModeChoice(self) -> None:
            self._database.set_setting("usage_mode", None)
            self._mode = ""
            self._active_student_id = None
            self._teacher_id = None
            self.modeChanged.emit("")
            self.classroomChanged.emit()

        @Slot(str, result="QVariantList")
        def groupsForClass(self, class_id: str):
            return self._classroom.list_groups(class_id) if class_id else []

        @Slot(str, str, result="QVariantList")
        def studentsForClass(self, class_id: str, group_id: str):
            if not class_id:
                return []
            return self._classroom.list_students(class_id, group_id or None)

        @Slot(str, str)
        def createTeacher(self, display_name: str, password: str) -> None:
            try:
                self._teacher_id = self._classroom.create_teacher(display_name, password)
                self._classroom_message = "Profil professeur créé."
            except Exception as exc:
                self._classroom_message = str(exc)
            self.classroomChanged.emit()

        @Slot(str, str)
        def loginTeacher(self, teacher_id: str, password: str) -> None:
            if self._classroom.authenticate_teacher(teacher_id, password):
                self._teacher_id = teacher_id
                self._classroom_message = "Connexion réussie."
            else:
                self._classroom_message = "Mot de passe incorrect."
            self.classroomChanged.emit()

        @Slot()
        def logoutTeacher(self) -> None:
            self._teacher_id = None
            self._classroom_message = "Vous êtes déconnecté."
            self.classroomChanged.emit()

        @Slot(str, str)
        def createClass(self, name: str, school_year: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_class(name, school_year or None)
                    self._classroom_message = "Classe créée."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self.classroomChanged.emit()

        @Slot(str, str)
        def createGroup(self, class_id: str, name: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_group(class_id, name)
                    self._classroom_message = "Groupe créé."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self.classroomChanged.emit()

        @Slot(str, str, str)
        def createStudent(self, class_id: str, display_name: str, group_id: str) -> None:
            if not self._teacher_id:
                self._classroom_message = "Connectez-vous à votre espace professeur."
            else:
                try:
                    self._classroom.create_student(class_id, display_name, group_id or None)
                    self._classroom_message = "Élève ajouté."
                except Exception as exc:
                    self._classroom_message = str(exc)
            self.classroomChanged.emit()

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
            self.classroomChanged.emit()

        @Slot(str)
        def selectStudent(self, student_id: str) -> None:
            self._active_student_id = student_id or None
            self.classroomChanged.emit()

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
            self.practiceChanged.emit()

        @Slot(str)
        def submitAnswer(self, response: str) -> None:
            if not self._session_id or not self._questions or self._answered or self._finished:
                return
            question = self._questions[self._question_index]
            correct = self._practice.record_answer(
                self._session_id, question.skill_id, question.prompt,
                question.answer, response,
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
            else:
                result = self._practice.finish_session(self._session_id)
                self._finished = True
                self._score_text = (
                    f"{result['correct']} bonne(s) réponse(s) sur {result['answered']}."
                )
            self.practiceChanged.emit()

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
            self.practiceChanged.emit()

    app = QGuiApplication(qt_args)
    app.setApplicationName("Wedone Operate Phoenix")
    app.setOrganizationName("WedoneOfficiel")

    database = Database(get_database_path())
    database.initialize()
    bridge = AppBridge(database)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("appBridge", bridge)
    qml_file = Path(__file__).parent / "ui" / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file.resolve())))
    if not engine.rootObjects():
        return 2
    if smoke_test:
        return 0
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

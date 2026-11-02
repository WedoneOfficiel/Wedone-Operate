"""Entry point for the Phoenix Qt Quick prototype and individual practice flow."""

from __future__ import annotations

import sys
from pathlib import Path

from .domain.questions import Question, generate_session
from .storage import Database, PracticeRepository, get_database_path


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

        def __init__(self, database: Database):
            super().__init__()
            self._database = database
            self._practice = PracticeRepository(database)
            self._mode = database.get_mode() or ""
            self._questions: tuple[Question, ...] = ()
            self._session_id: str | None = None
            self._question_index = 0
            self._answered = False
            self._finished = False
            self._feedback = ""
            self._score_text = ""

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
            self.modeChanged.emit("")

        @Slot(str, int, int)
        def startPractice(self, skill_id: str, count: int, difficulty: int) -> None:
            if self._mode != "individual":
                self._feedback = "L'entraînement individuel n'est pas disponible dans ce mode."
                self.practiceChanged.emit()
                return
            questions = generate_session(skill_id, count, difficulty, avoid_duplicates=True)
            session_id = self._practice.start_session(
                "individual",
                len(questions),
                {"skill_id": skill_id, "difficulty": difficulty},
            )
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
                self._session_id,
                question.skill_id,
                question.prompt,
                question.answer,
                response,
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

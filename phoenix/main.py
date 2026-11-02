"""Entry point for the Phoenix Qt Quick prototype.

Run with: python -m phoenix.main
Smoke test: QT_QPA_PLATFORM=offscreen python -m phoenix.main --smoke-test
"""

from __future__ import annotations

import sys
from pathlib import Path

from .storage import Database, get_database_path


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

        def __init__(self, database: Database):
            super().__init__()
            self._database = database
            self._mode = database.get_mode() or ""

        @Property(str, notify=modeChanged)
        def mode(self) -> str:
            return self._mode

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

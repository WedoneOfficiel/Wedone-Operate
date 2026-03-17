# main.py — Wedone Operate 2026.03.17

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
import settings as cfg
import session
from ui.theme           import apply as apply_theme
from ui.screen_login    import LoginScreen
from ui.screen_dashboard import DashboardScreen
from ui.screen_main     import MainScreen
from ui.screen_game     import GameScreen
from ui.screen_results  import ResultsScreen
from ui.screen_stats    import StatsScreen
from ui.screen_settings import SettingsScreen
from ui.screen_admin    import AdminScreen

IDX_LOGIN     = 0
IDX_DASHBOARD = 1
IDX_MAIN      = 2
IDX_GAME      = 3
IDX_RESULTS   = 4
IDX_STATS     = 5
IDX_SETTINGS  = 6
IDX_ADMIN     = 7


class WedoneOperateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self._settings = cfg.load()
        self._theme    = cfg.resolve_theme(self._settings)
        self._last_cfg = {}

        self.setWindowTitle("Wedone Operate")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(820, 560); self.resize(960, 660)
        apply_theme(QApplication.instance(), self._theme)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.s_login     = LoginScreen()
        self.s_dashboard = DashboardScreen()
        self.s_main      = MainScreen()
        self.s_game      = GameScreen()
        self.s_results   = ResultsScreen()
        self.s_stats     = StatsScreen()
        self.s_settings  = SettingsScreen()
        self.s_admin     = AdminScreen()

        for s in (self.s_login, self.s_dashboard, self.s_main, self.s_game,
                  self.s_results, self.s_stats, self.s_settings, self.s_admin):
            self.stack.addWidget(s)

        # Connexions
        self.s_login.logged_in.connect(self._on_logged_in)

        self.s_dashboard.open_admin.connect(self._open_admin)
        self.s_dashboard.open_stats.connect(self._open_stats)
        self.s_dashboard.open_settings.connect(self._open_settings)
        self.s_dashboard.logout.connect(self._logout)

        self.s_main.session_ready.connect(self._on_session_ready)
        self.s_main.open_settings.connect(self._open_settings)
        self.s_main.open_stats.connect(self._open_stats)
        self.s_main.logout.connect(self._logout)

        self.s_game.session_finished.connect(self._on_session_finished)
        self.s_game.session_aborted.connect(self._after_game_abort)

        self.s_results.play_again.connect(self._on_play_again)
        self.s_results.go_home.connect(self._go_home)

        self.s_stats.go_back.connect(self._go_home)
        self.s_admin.go_back.connect(self._go_home)

        self.s_settings.go_back.connect(self._on_settings_back)
        self.s_settings.theme_changed.connect(self._on_theme_changed)

        self._goto(IDX_LOGIN)

        if self._settings.get("auto_update", True):
            self._check_update_async()

    def _goto(self, idx): self.stack.setCurrentIndex(idx)

    def _on_logged_in(self):
        self._settings = cfg.load()
        if session.current.is_student():
            self.s_main.refresh()
            self._goto(IDX_MAIN)
        else:
            self.s_dashboard.refresh()
            self._goto(IDX_DASHBOARD)

    def _on_session_ready(self, config):
        self._last_cfg = config
        self.s_game.start_session(config)
        self._goto(IDX_GAME)

    def _on_session_finished(self, results):
        self.s_results.show_results(results)
        self._goto(IDX_RESULTS)

    def _after_game_abort(self):
        self._go_home()

    def _on_play_again(self):
        if self._last_cfg:
            self.s_game.start_session(self._last_cfg)
            self._goto(IDX_GAME)
        else: self._go_home()

    def _go_home(self):
        if session.current.is_student():
            self.s_main.refresh(); self._goto(IDX_MAIN)
        else:
            self.s_dashboard.refresh(); self._goto(IDX_DASHBOARD)

    def _open_stats(self):
        self.s_stats.refresh(); self._goto(IDX_STATS)

    def _open_admin(self):
        self.s_admin.refresh(); self._goto(IDX_ADMIN)

    def _open_settings(self):
        self.s_settings.refresh(); self._goto(IDX_SETTINGS)

    def _on_settings_back(self):
        self._settings = cfg.load(); self._go_home()

    def _logout(self):
        session.logout()
        self.s_login.refresh(); self._goto(IDX_LOGIN)

    def _on_theme_changed(self, theme):
        self._theme = theme
        apply_theme(QApplication.instance(), theme)

    def _check_update_async(self):
        from PyQt6.QtCore import QThread, pyqtSignal as Signal
        class Worker(QThread):
            found = Signal(dict)
            def run(self):
                from updater import check_for_update
                r = check_for_update()
                if r: self.found.emit(r)
        self._worker = Worker()
        self._worker.found.connect(lambda info: __import__("ui.dialog_update", fromlist=["UpdateDialog"]).UpdateDialog(info, self).exec())
        self._worker.start()


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("wedone.operate")
    except: pass
    app = QApplication(sys.argv)
    window = WedoneOperateApp()
    window.show()
    sys.exit(app.exec())

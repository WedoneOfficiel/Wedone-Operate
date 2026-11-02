# ui/screen_game.py — Wedone Operate

import random, time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QProgressBar, QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor
from constants import DIFFICULTY_RANGES, LEVEL_RANGES, TIMER_SECONDS, TIMER_SECONDS_BY_LEVEL, SCHOOL_LEVELS
import session


class GameScreen(QWidget):
    session_finished = pyqtSignal(dict)
    session_aborted  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._config = {}
        self._questions = []
        self._idx = 0
        self._score = 0
        self._details = []
        self._session_start = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(80)
        self._timer.timeout.connect(self._tick)
        self._time_left = 0.0
        self._epreuve_start = 0.0
        self._feedback_pause = 0.0
        self._feedback_started = None
        self._feedback_timer = QTimer(self)
        self._feedback_timer.setSingleShot(True)
        self._feedback_timer.timeout.connect(self._next_question)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Barre de progression session (permanente, tout en haut) ───
        self._session_bar = QProgressBar()
        self._session_bar.setTextVisible(False)
        self._session_bar.setFixedHeight(5)
        self._session_bar.setStyleSheet(
            "QProgressBar{border:none;border-radius:0;background:rgba(128,128,128,0.1);}"
            "QProgressBar::chunk{background:#0879C9;border-radius:0;}"
        )
        root.addWidget(self._session_bar)

        # ── En-tête ───────────────────────────────────────────────────
        topbar = QFrame()
        topbar.setFixedHeight(54)
        topbar.setStyleSheet("border-bottom: 1px solid rgba(128,128,128,0.12);")
        tl = QHBoxLayout(topbar)
        tl.setContentsMargins(24, 0, 24, 0)

        self._progress_lbl = QLabel("Épreuve 1 / 10")
        self._progress_lbl.setObjectName("subtitle")
        tl.addWidget(self._progress_lbl)
        tl.addStretch()

        self._score_lbl = QLabel("Score : 0")
        self._score_lbl.setObjectName("subtitle")
        tl.addWidget(self._score_lbl)

        abandon_btn = QPushButton("✕ Abandonner")
        abandon_btn.setProperty("class", "secondary")
        abandon_btn.clicked.connect(self._abandon)
        tl.addWidget(abandon_btn)
        root.addWidget(topbar)

        # ── Chronomètre (visible si activé) ───────────────────────────
        self._chrono_widget = QWidget()
        self._chrono_widget.setFixedHeight(42)
        cl = QHBoxLayout(self._chrono_widget)
        cl.setContentsMargins(24, 4, 24, 4)
        cl.setSpacing(12)

        self._chrono_lbl = QLabel("30.0 s")
        self._chrono_lbl.setFixedWidth(60)
        self._chrono_lbl.setStyleSheet("font-size: 16px; font-weight: 500;")
        cl.addWidget(self._chrono_lbl)

        self._chrono_bar = QProgressBar()
        self._chrono_bar.setTextVisible(False)
        self._chrono_bar.setFixedHeight(10)
        cl.addWidget(self._chrono_bar)

        self._chrono_widget.hide()
        root.addWidget(self._chrono_widget)

        # ── Zone question (fond coloré feedback) ──────────────────────
        self._feedback_bg = QWidget()
        self._feedback_bg.setAutoFillBackground(True)
        fbg_layout = QVBoxLayout(self._feedback_bg)
        fbg_layout.setContentsMargins(60, 40, 60, 40)
        fbg_layout.setSpacing(20)
        fbg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._question_lbl = QLabel("0 + 0 = ?")
        self._question_lbl.setObjectName("question")
        self._question_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fbg_layout.addWidget(self._question_lbl)

        self._answer_input = QLineEdit()
        self._answer_input.setObjectName("answer-input")
        self._answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._answer_input.setMaximumWidth(300)
        self._answer_input.returnPressed.connect(self._validate)
        fbg_layout.addWidget(self._answer_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self._feedback_lbl = QLabel("")
        self._feedback_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_lbl.setStyleSheet("font-size: 16px; font-weight: 500;")
        fbg_layout.addWidget(self._feedback_lbl)

        root.addWidget(self._feedback_bg, stretch=1)

        # ── Bouton valider ────────────────────────────────────────────
        bottom = QFrame()
        bottom.setFixedHeight(68)
        bottom.setStyleSheet("border-top: 1px solid rgba(128,128,128,0.12);")
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(24, 0, 24, 0)
        bl.addStretch()

        self._validate_btn = QPushButton("✔  Valider")
        self._validate_btn.setFixedSize(160, 44)
        self._validate_btn.setStyleSheet("font-size: 15px;")
        self._validate_btn.clicked.connect(self._validate)
        bl.addWidget(self._validate_btn)
        root.addWidget(bottom)

    # ── Session ───────────────────────────────────────────────────────
    def start_session(self, config: dict):
        self._config = config
        self._questions = self._gen_questions(config)
        self._idx = 0
        self._score = 0
        self._details = []
        self._feedback_pause = 0.0
        self._feedback_started = None
        self._session_start = time.monotonic()
        self._session_bar.setMaximum(len(self._questions))
        self._session_bar.setValue(0)
        self._chrono_widget.setVisible(config["timer_enabled"])
        self._reset_bg()
        self._show_question()

    def _gen_questions(self, cfg) -> list[dict]:
        ops = cfg.get("operations") or []
        if not ops or any(op not in ("addition", "soustraction", "multiplication", "division") for op in ops):
            raise ValueError("Sélectionnez au moins une opération valide.")
        count = int(cfg.get("nb_epreuves", 0))
        if not 1 <= count <= 100:
            raise ValueError("Le nombre d'épreuves doit être compris entre 1 et 100.")
        level = cfg.get("difficulty", "CM2")
        # Supporte autant les niveaux scolaires que les anciens Facile/Moyen/Difficile
        if level in LEVEL_RANGES:
            ranges = LEVEL_RANGES[level]
        elif level in DIFFICULTY_RANGES:
            ranges = DIFFICULTY_RANGES[level]
        else:
            ranges = LEVEL_RANGES["CM2"]
        result = []
        for _ in range(count):
            op = random.choice(ops)
            r  = ranges[op]
            a, b, res, sym = self._make_op(op, r)
            result.append({"op": op, "a": a, "b": b, "result": res, "sym": sym})
        return result

    def _make_op(self, op, r):
        if op == "addition":
            a, b = random.randint(r[0], r[1]), random.randint(r[2], r[3])
            return a, b, a + b, "+"
        elif op == "soustraction":
            # Ensure the first operand can always accommodate the minimum
            # second operand (notably for 5e and above, where min_b is 2).
            a = random.randint(max(r[0], r[2]), r[1])
            b = random.randint(r[2], min(r[3], a))
            return a, b, a - b, "−"
        elif op == "multiplication":
            a, b = random.randint(r[0], r[1]), random.randint(r[2], r[3])
            return a, b, a * b, "×"
        elif op == "division":
            div = random.randint(max(r[0], 1), r[1])
            quo = random.randint(max(r[2], 1), r[3])
            return div * quo, div, quo, "÷"
        return 0, 0, 0, "?"

    # ── Affichage question ────────────────────────────────────────────
    def _show_question(self):
        q   = self._questions[self._idx]
        n   = len(self._questions)
        self._progress_lbl.setText(f"Épreuve {self._idx + 1} / {n}")
        self._score_lbl.setText(f"Score : {self._score}")
        self._session_bar.setValue(self._idx)
        self._question_lbl.setText(f"{q['a']}  {q['sym']}  {q['b']}  = ?")
        self._feedback_lbl.setText("")
        self._answer_input.clear()
        self._answer_input.setEnabled(True)
        self._validate_btn.setEnabled(True)
        self._answer_input.setFocus()
        self._reset_bg()

        if self._config.get("timer_enabled"):
            lvl = self._config["difficulty"]
            secs = TIMER_SECONDS_BY_LEVEL.get(lvl) or TIMER_SECONDS.get(lvl, 20)
            self._time_left = float(secs)
            self._chrono_bar.setMaximum(secs * 10)
            self._chrono_bar.setValue(secs * 10)
            self._update_chrono_display()
            self._epreuve_start = time.monotonic()
            self._timer.start()

    # ── Chronomètre ───────────────────────────────────────────────────
    def _tick(self):
        # Sécurité : ne rien faire si la session est terminée ou l'entrée désactivée
        if self._idx >= len(self._questions):
            self._timer.stop()
            return
        if not self._answer_input.isEnabled():
            return
        elapsed = time.monotonic() - self._epreuve_start
        lvl  = self._config["difficulty"]
        secs    = TIMER_SECONDS_BY_LEVEL.get(lvl) or TIMER_SECONDS.get(lvl, 20)
        self._time_left = max(0.0, secs - elapsed)
        self._update_chrono_display()
        if self._time_left <= 0:
            self._timer.stop()
            self._register(timed_out=True)

    def _update_chrono_display(self):
        level = self._config.get("difficulty", "CM2")
        secs = TIMER_SECONDS_BY_LEVEL.get(level) or TIMER_SECONDS.get(level, 20)
        ratio = self._time_left / max(1, secs)
        self._chrono_lbl.setText(f"{self._time_left:.1f} s")
        self._chrono_bar.setValue(int(self._time_left * 10))

        if ratio > 0.5:
            color, cls = "#269B70", "timer-green"
        elif ratio > 0.25:
            color, cls = "#F0A030", "timer-orange"
        else:
            color, cls = "#E24B5F", "timer-red"

        self._chrono_lbl.setStyleSheet(
            f"font-size:16px;font-weight:500;color:{color};"
        )
        self._chrono_bar.setProperty("class", cls)
        self._chrono_bar.style().unpolish(self._chrono_bar)
        self._chrono_bar.style().polish(self._chrono_bar)

    # ── Validation ────────────────────────────────────────────────────
    def _validate(self):
        if not self._answer_input.isEnabled():
            return
        if self._config.get("timer_enabled"):
            self._timer.stop()
        self._register(timed_out=False)

    def _register(self, timed_out: bool):
        q = self._questions[self._idx]
        answer = self._answer_input.text().strip()
        correct = False

        self._answer_input.setEnabled(False)
        self._validate_btn.setEnabled(False)

        if timed_out:
            self._set_bg_feedback("error")
            self._feedback_lbl.setObjectName("feedback")
            self._feedback_lbl.setStyleSheet("color:#E24B5F;")
            self._feedback_lbl.setText(f"⏱  Temps écoulé !  La réponse était  {q['result']}")
        else:
            try:
                if int(answer) == q["result"]:
                    correct = True
                    self._score += 1
                    self._set_bg_feedback("success")
                    self._feedback_lbl.setObjectName("feedback")
                    self._feedback_lbl.setStyleSheet("color:#269B70;")
                    self._feedback_lbl.setText("✔  Bonne réponse !")
                else:
                    self._set_bg_feedback("error")
                    self._feedback_lbl.setObjectName("feedback")
                    self._feedback_lbl.setStyleSheet("color:#E24B5F;")
                    self._feedback_lbl.setText(f"✘  Incorrect.  La réponse était  {q['result']}")
            except ValueError:
                # Saisie invalide : on relance
                self._feedback_lbl.setObjectName("feedback")
                self._feedback_lbl.setStyleSheet("color:#B87516;")
                self._feedback_lbl.setText("⚠  Entrez un nombre entier.")
                self._answer_input.setEnabled(True)
                self._validate_btn.setEnabled(True)
                self._answer_input.setFocus()
                if self._config.get("timer_enabled"):
                    self._epreuve_start = time.monotonic() - (
                        (TIMER_SECONDS_BY_LEVEL.get(self._config["difficulty"]) or TIMER_SECONDS.get(self._config["difficulty"], 20)) - self._time_left
                    )
                    self._timer.start()
                return

        self._feedback_started = time.monotonic()
        self._details.append({
            "question":  f"{q['a']} {q['sym']} {q['b']}",
            "expected":  q["result"],
            "given":     answer if not timed_out else None,
            "correct":   correct,
            "timed_out": timed_out,
            "operation": q["op"],
        })
        self._score_lbl.setText(f"Score : {self._score}")
        self._feedback_timer.start(950)

    def _set_bg_feedback(self, kind: str):
        """Flash de couleur sur le fond de la zone question."""
        if kind == "success":
            color = "rgba(28,138,78,0.10)"
        else:
            color = "rgba(192,57,43,0.10)"
        self._feedback_bg.setStyleSheet(f"background-color: {color};")

    def _reset_bg(self):
        self._feedback_bg.setStyleSheet("background-color: transparent;")

    # ── Navigation ────────────────────────────────────────────────────
    def _next_question(self):
        if self._feedback_started is not None:
            self._feedback_pause += max(0.0, time.monotonic() - self._feedback_started)
            self._feedback_started = None
        self._idx += 1
        if self._idx >= len(self._questions):
            self._finish()
        else:
            self._show_question()

    def _finish(self):
        self._timer.stop()
        self._feedback_timer.stop()
        # The 950 ms answer-feedback animation is not practice time.
        elapsed = max(0.0, time.monotonic() - self._session_start - self._feedback_pause)
        n = len(self._questions)
        results = {
            "student_id":     self._config.get("student_id"),
            "student_name":   self._config.get("student_name", ""),
            "difficulty":     self._config["difficulty"],
            "total":          n,
            "correct":        self._score,
            "percent":        round(self._score * 100 / n, 1) if n > 0 else 0,
            "timer_enabled":  self._config["timer_enabled"],
            "operations":     self._config["operations"],
            "elapsed_seconds":round(elapsed, 1),
            "details":        self._details,
        }
        self._session_bar.setValue(n)
        self.session_finished.emit(results)

    def _abandon(self):
        self._timer.stop()
        from PyQt6.QtWidgets import QMessageBox
        rep = QMessageBox.question(
            self, "Abandonner",
            "Abandonner la session ?\nLes résultats ne seront pas sauvegardés.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if rep == QMessageBox.StandardButton.Yes:
            self.session_aborted.emit()
        elif self._config.get("timer_enabled"):
            self._epreuve_start = time.monotonic() - (
                (TIMER_SECONDS_BY_LEVEL.get(self._config["difficulty"]) or TIMER_SECONDS.get(self._config["difficulty"], 20)) - self._time_left
            )
            self._timer.start()

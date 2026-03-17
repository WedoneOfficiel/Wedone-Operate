# ui/screen_results.py — Wedone Operate
# Écran de résultats avec jauge circulaire animée.

import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import database as db


class CircleScore(QWidget):
    """Jauge circulaire animée affichant le pourcentage."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 160)
        self._percent = 0.0
        self._target  = 0.0
        self._anim_value = 0.0

    def set_target(self, percent: float):
        self._target = percent
        self._anim_value = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _tick(self):
        step = self._target / 40
        self._anim_value = min(self._anim_value + step, self._target)
        self.update()
        if self._anim_value >= self._target:
            self._timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        margin = 16
        rect_size = min(w, h) - 2 * margin

        # Arc de fond
        pen_bg = QPen(QColor("#E8ECF4"), 12, Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(margin, margin, rect_size, rect_size, 0, 360 * 16)

        # Arc de progression
        pct = self._anim_value
        if pct >= 80:
            color = QColor("#2EBD6E")
        elif pct >= 50:
            color = QColor("#F0A030")
        else:
            color = QColor("#E05555")

        pen_fg = QPen(color, 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_fg)
        span = int(pct / 100 * 360 * 16)
        painter.drawArc(margin, margin, rect_size, rect_size, 90 * 16, -span)

        # Texte central
        painter.setPen(QColor("#1A1D23"))
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(0, 0, w, h, Qt.AlignmentFlag.AlignCenter,
                         f"{int(pct)}%")
        painter.end()


class ResultsScreen(QWidget):
    play_again = pyqtSignal()
    go_home    = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(50, 28, 50, 28)
        root.setSpacing(16)

        # En-tête
        self.title_label = QLabel("Résultats")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        root.addWidget(self.title_label)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep)

        # Score + résumé
        score_row = QHBoxLayout()
        score_row.setSpacing(30)

        self.circle = CircleScore()
        score_row.addWidget(self.circle)

        info_col = QVBoxLayout()
        info_col.setSpacing(6)
        info_col.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.detail_label  = QLabel("")
        self.detail_label.setObjectName("subtitle")
        self.chrono_label  = QLabel("")
        self.chrono_label.setObjectName("subtitle")
        info_col.addWidget(self.summary_label)
        info_col.addWidget(self.detail_label)
        info_col.addWidget(self.chrono_label)
        score_row.addLayout(info_col)
        score_row.addStretch()
        root.addLayout(score_row)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep2)

        # Détail scrollable
        detail_title = QLabel("Détail des épreuves")
        detail_title.setStyleSheet("font-weight: bold; font-size: 15px;")
        root.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.detail_container = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_container)
        self.detail_layout.setSpacing(5)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self.detail_container)
        root.addWidget(scroll)

        sep3 = QFrame(); sep3.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep3)

        btns = QHBoxLayout()
        home_btn = QPushButton("⌂  Accueil")
        home_btn.setProperty("class", "secondary")
        home_btn.clicked.connect(self.go_home)
        again_btn = QPushButton("↺  Rejouer")
        again_btn.clicked.connect(self.play_again)
        btns.addWidget(home_btn)
        btns.addStretch()
        btns.addWidget(again_btn)
        root.addLayout(btns)

    def show_results(self, results: dict):
        student_id   = results.get("student_id")
        student_name = results.get("student_name", "")
        correct  = results["correct"]
        total    = results["total"]
        percent  = results["percent"]
        elapsed  = results.get("elapsed_seconds")
        details  = results.get("details", [])

        # Sauvegarde si c'est un élève (pas admin ni prof)
        if student_id and student_id.startswith("s_"):
            db.save_score(
                student_id    = student_id,
                difficulty    = results["difficulty"],
                total         = total,
                correct       = correct,
                timer_enabled = results["timer_enabled"],
                operations    = results["operations"],
                elapsed_seconds = elapsed,
            )

        self.title_label.setText(f"Résultats — {student_name}")
        self.circle.set_target(percent)

        emoji = "🎉" if percent >= 80 else ("👍" if percent >= 50 else "💪")
        self.summary_label.setText(
            f"{emoji}  {correct} bonne{'s' if correct > 1 else ''} "
            f"réponse{'s' if correct > 1 else ''} sur {total}"
        )
        self.detail_label.setText(f"Niveau : {results['difficulty']}")

        if elapsed is not None:
            m, s = int(elapsed) // 60, int(elapsed) % 60
            self.chrono_label.setText(f"⏱ Durée totale : {m}min {s:02d}s")
        else:
            self.chrono_label.setText("")

        # Vider et remplir le détail
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        for i, d in enumerate(details, 1):
            row = QHBoxLayout()
            num = QLabel(f"{i:2}.")
            num.setFixedWidth(30)
            num.setObjectName("subtitle")
            question = QLabel(f"{d['question']} = {d['expected']}")
            question.setFixedWidth(190)

            if d.get("timed_out"):
                status = QLabel("⏱ Temps écoulé")
                status.setStyleSheet("color: #E07B00;")
            elif d["correct"]:
                status = QLabel("✔ Correct")
                status.setStyleSheet("color: #2EBD6E;")
            else:
                status = QLabel(f"✘ Répondu : {d.get('given', '—')}")
                status.setStyleSheet("color: #E05555;")

            row.addWidget(num)
            row.addWidget(question)
            row.addWidget(status)
            row.addStretch()

            c = QWidget()
            c.setLayout(row)
            self.detail_layout.addWidget(c)

        self.detail_layout.addStretch()

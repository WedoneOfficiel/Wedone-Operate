# ui/theme.py — Wedone Operate
# Identité visuelle Wedone : surfaces douces, accent rose, thèmes clair et sombre.
# Les polices Manrope / DM Sans sont utilisées si elles sont installées ; Qt conserve
# un fallback natif sur les systèmes qui ne les possèdent pas.

from PyQt6.QtGui import QFont
from constants import LIGHT, DARK


def get_stylesheet(theme: str) -> str:
    c = DARK if theme == "dark" else LIGHT
    return f"""
/* ── Base ───────────────────────────────────────────────────── */
QWidget {{
    background-color: {c['bg']};
    color: {c['text']};
    font-family: "DM Sans", "Segoe UI", "Ubuntu", "Cantarell", sans-serif;
    font-size: 13px;
}}
QMainWindow, QDialog {{ background-color: {c['bg']}; }}
QFrame {{ background: transparent; }}
QLabel {{ color: {c['text']}; background: transparent; }}
QLabel#title {{ color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif; font-size: 25px; font-weight: 800; }}
QLabel#section {{ color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif; font-size: 16px; font-weight: 750; }}
QLabel#subtitle {{ color: {c['text_secondary']}; font-size: 12px; }}
QLabel#success {{ color: {c['success']}; font-weight: 700; }}
QLabel#error {{ color: {c['error']}; font-weight: 700; }}
QLabel#warning {{ color: {c['warning']}; }}
QLabel#hint {{ color: {c['text_secondary']}; font-size: 11px; }}
QLabel#question {{ color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif; font-size: 42px; font-weight: 800; }}

/* ── Surfaces et panneaux ───────────────────────────────────── */
QFrame#opsBox, QFrame[class="card"], QFrame[class="card-selected"] {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 16px;
}}
QFrame[class="card"]:hover {{ border-color: {c['border_hover']}; }}
QFrame[class="card-selected"] {{
    border: 2px solid {c['primary']};
    background-color: {c['accent_soft']};
}}

/* ── Champs ─────────────────────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {c['input']};
    color: {c['text']};
    border: 1px solid {c['border']};
    border-radius: 12px;
    padding: 9px 12px;
    selection-background-color: {c['primary']};
    selection-color: white;
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover, QSpinBox:hover, QComboBox:hover {{
    border-color: {c['border_hover']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {c['primary']};
    background-color: {c['surface']};
}}
QLineEdit#answer-input {{ font-size: 24px; padding: 13px; border-radius: 14px; }}
QComboBox {{ padding-right: 28px; }}
QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 26px; border: 0; }}
QComboBox QAbstractItemView {{
    background-color: {c['surface']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 10px;
    selection-background-color: {c['accent_soft']}; selection-color: {c['text']};
    padding: 5px;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 18px; border: 0; background: transparent; }}

/* ── Boutons ────────────────────────────────────────────────── */
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {c['primary']}, stop:1 {c['primary_alt']});
    color: white; border: 0; border-radius: 12px;
    padding: 10px 17px; min-height: 18px;
    font-size: 13px; font-weight: 700;
}}
QPushButton:hover {{ background: {c['primary_hover']}; }}
QPushButton:pressed {{ background: {c['primary_pressed']}; }}
QPushButton:disabled {{ background: {c['disabled']}; color: {c['text_muted']}; }}
QPushButton[class="secondary"], QPushButton[class="nav"] {{
    background-color: {c['surface']}; color: {c['text_secondary']};
    border: 1px solid {c['border']}; border-radius: 12px;
}}
QPushButton[class="secondary"]:hover, QPushButton[class="nav"]:hover {{
    background-color: {c['surface_hover']}; border-color: {c['border_hover']}; color: {c['text']};
}}
QPushButton[class="danger"] {{ background-color: {c['error']}; color: white; }}
QPushButton[class="danger"]:hover {{ background-color: {c['error_hover']}; }}
QPushButton[class="nav"] {{ text-align: left; padding: 10px 14px; font-weight: 600; }}
QPushButton[class="nav-active"] {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
    border: 1px solid {c['accent_border']}; border-radius: 12px;
    text-align: left; padding: 10px 14px; font-weight: 800;
}}
QPushButton[class="role-chip"], QPushButton[class="tab"] {{
    background-color: {c['surface']}; color: {c['text_secondary']};
    border: 1px solid {c['border']}; border-radius: 11px; padding: 9px 16px;
}}
QPushButton[class="role-chip-active"], QPushButton[class="tab"]:checked {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
    border: 1px solid {c['accent_border']}; font-weight: 800;
}}

/* ── Sélection, cases et onglets ────────────────────────────── */
QCheckBox {{ color: {c['text']}; spacing: 9px; }}
QCheckBox::indicator {{ width: 18px; height: 18px; border: 1px solid {c['border']}; border-radius: 6px; background: {c['input']}; }}
QCheckBox::indicator:checked {{ background: {c['primary']}; border-color: {c['primary']}; }}
QTabWidget::pane {{ border: 1px solid {c['border']}; border-radius: 14px; top: -1px; }}
QTabBar::tab {{
    background: transparent; color: {c['text_secondary']};
    padding: 9px 15px; margin-right: 4px;
    border: 1px solid transparent; border-radius: 10px;
}}
QTabBar::tab:selected {{ background: {c['accent_soft']}; color: {c['accent_ink']}; font-weight: 800; }}
QTabBar::tab:hover:!selected {{ background: {c['surface_hover']}; }}

/* ── Tableaux et listes ─────────────────────────────────────── */
QListWidget, QTableWidget, QTreeWidget {{
    background-color: {c['surface']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 14px; outline: none;
    gridline-color: {c['border']};
}}
QListWidget::item {{ padding: 9px 11px; border-radius: 8px; margin: 2px 5px; }}
QListWidget::item:selected, QTableWidget::item:selected, QTreeWidget::item:selected {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
}}
QHeaderView::section {{
    background-color: {c['surface_hover']}; color: {c['text_secondary']};
    font-weight: 800; font-size: 11px; padding: 9px;
    border: 0; border-bottom: 1px solid {c['border']};
}}
QGroupBox {{
    border: 1px solid {c['border']}; border-radius: 14px;
    margin-top: 15px; padding: 14px 12px 12px;
    color: {c['text_secondary']}; font-weight: 700;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 13px; padding: 0 6px; background: {c['bg']}; }}

/* ── Progression et défilement ──────────────────────────────── */
QProgressBar {{ background: {c['surface_hover']}; border: 0; border-radius: 6px; height: 9px; text-align: center; }}
QProgressBar::chunk {{ background: {c['primary']}; border-radius: 6px; }}
QProgressBar[class="timer-green"]::chunk {{ background: {c['success']}; }}
QProgressBar[class="timer-orange"]::chunk {{ background: {c['warning']}; }}
QProgressBar[class="timer-red"]::chunk {{ background: {c['error']}; }}
QScrollBar:vertical {{ background: transparent; width: 8px; margin: 3px; }}
QScrollBar::handle:vertical {{ background: {c['scroll']}; border-radius: 4px; min-height: 28px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ background: transparent; height: 8px; margin: 3px; }}
QScrollBar::handle:horizontal {{ background: {c['scroll']}; border-radius: 4px; min-width: 28px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QFrame[frameShape="4"], QFrame[frameShape="5"] {{ color: {c['border']}; background: {c['border']}; border: 0; max-height: 1px; }}
QToolTip {{ background: {c['surface']}; color: {c['text']}; border: 1px solid {c['border']}; padding: 6px 9px; border-radius: 7px; }}
"""


def apply(app, theme: str) -> None:
    app.setFont(QFont("DM Sans", 10))
    app.setStyleSheet(get_stylesheet(theme))

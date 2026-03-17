# ui/theme.py — Wedone Operate
# Feuilles de style Qt modernisées — thème clair et sombre.

from constants import LIGHT, DARK


def get_stylesheet(theme: str) -> str:
    c = DARK if theme == "dark" else LIGHT
    base = f"""
/* ── Base ───────────────────────────────────────────────────── */
QWidget {{
    background-color: {c['bg']};
    color: {c['text']};
    font-family: "Segoe UI", "Ubuntu", "Cantarell", sans-serif;
    font-size: 14px;
}}
QDialog {{ background-color: {c['bg']}; }}
QMainWindow {{ background-color: {c['bg']}; }}

/* ── Labels ─────────────────────────────────────────────────── */
QLabel {{ color: {c['text']}; background: transparent; }}
QLabel#subtitle  {{ color: {c['text_secondary']}; font-size: 13px; }}
QLabel#title     {{ font-size: 22px; font-weight: 500; color: {c['primary']}; }}
QLabel#section   {{ font-size: 16px; font-weight: 500; color: {c['text']}; }}
QLabel#success   {{ color: {c['success']}; font-weight: 500; }}
QLabel#error     {{ color: {c['error']}; font-weight: 500; }}
QLabel#warning   {{ color: {c['warning']}; }}
QLabel#hint      {{ color: {c['text_secondary']}; font-size: 12px; font-style: italic; }}
QLabel#question  {{ font-size: 42px; font-weight: 500; color: {c['text']}; }}

/* ── Champs de saisie ───────────────────────────────────────── */
QLineEdit {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
    border: 1.5px solid {c['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
}}
QLineEdit:focus {{ border-color: {c['primary']}; }}
QLineEdit#answer-input {{
    font-size: 24px;
    text-align: center;
    padding: 12px;
    border-radius: 10px;
}}

/* ── Boutons principaux ─────────────────────────────────────── */
QPushButton {{
    background-color: {c['primary']};
    color: {c['primary_text']};
    font-weight: 500;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: 14px;
}}
QPushButton:hover   {{ background-color: {c['primary_hover']}; }}
QPushButton:pressed {{ padding-top: 10px; padding-bottom: 8px; }}
QPushButton:disabled {{
    background-color: {c['disabled']};
    color: {c['bg']};
}}

/* ── Boutons secondaires ────────────────────────────────────── */
QPushButton[class="secondary"] {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
    border: 1.5px solid {c['border']};
}}
QPushButton[class="secondary"]:hover {{
    border-color: {c['primary']};
    color: {c['primary']};
    background-color: {c['bg_secondary']};
}}

/* ── Boutons danger ─────────────────────────────────────────── */
QPushButton[class="danger"] {{
    background-color: {c['error']};
    color: white;
}}
QPushButton[class="danger"]:hover {{ background-color: #a93226; }}

/* ── Navigation latérale ────────────────────────────────────── */
QPushButton[class="nav"] {{
    background-color: transparent;
    color: {c['text_secondary']};
    font-weight: 400;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
}}
QPushButton[class="nav"]:hover {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
}}
QPushButton[class="nav-active"] {{
    background-color: {c['primary']};
    color: white;
    font-weight: 500;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
}}

/* ── Cartes élèves / profil ─────────────────────────────────── */
QFrame[class="card"] {{
    background-color: {c['bg_secondary']};
    border: 1.5px solid {c['border']};
    border-radius: 12px;
}}
QFrame[class="card"]:hover {{
    border-color: {c['primary']};
    background-color: {c['bg_secondary']};
}}
QFrame[class="card-selected"] {{
    background-color: {c['bg_secondary']};
    border: 2px solid {c['primary']};
    border-radius: 12px;
}}

/* ── Badges de rôle ─────────────────────────────────────────── */
QLabel[class="badge-admin"] {{
    background-color: #0672BC;
    color: white;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 500;
}}
QLabel[class="badge-teacher"] {{
    background-color: #0F6E56;
    color: white;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 500;
}}
QLabel[class="badge-student"] {{
    background-color: {c['bg_secondary']};
    color: {c['text_secondary']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
}}

/* ── Cases à cocher ─────────────────────────────────────────── */
QCheckBox {{ color: {c['text']}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 1.5px solid {c['border']};
    border-radius: 5px;
    background-color: {c['bg_secondary']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['primary']};
    border-color: {c['primary']};
}}

/* ── ComboBox ───────────────────────────────────────────────── */
QComboBox {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
    border: 1.5px solid {c['border']};
    border-radius: 8px;
    padding: 7px 12px;
}}
QComboBox:focus {{ border-color: {c['primary']}; }}
QComboBox QAbstractItemView {{
    background-color: {c['surface']};
    color: {c['text']};
    selection-background-color: {c['primary']};
    selection-color: white;
    border: 1px solid {c['border']};
    border-radius: 8px;
}}

/* ── SpinBox ────────────────────────────────────────────────── */
QSpinBox {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
    border: 1.5px solid {c['border']};
    border-radius: 8px;
    padding: 7px 10px;
}}
QSpinBox:focus {{ border-color: {c['primary']}; }}

/* ── Séparateurs ────────────────────────────────────────────── */
QFrame[frameShape="4"],
QFrame[frameShape="5"] {{
    color: {c['border']};
    background-color: {c['border']};
    border: none;
    max-height: 1px;
}}

/* ── Barre de progression ───────────────────────────────────── */
QProgressBar {{
    background-color: {c['bg_secondary']};
    border: none;
    border-radius: 5px;
    height: 8px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {c['primary']};
    border-radius: 5px;
}}
QProgressBar[class="timer-green"]::chunk  {{ background-color: {c['success']}; }}
QProgressBar[class="timer-orange"]::chunk {{ background-color: {c['warning']}; }}
QProgressBar[class="timer-red"]::chunk    {{ background-color: {c['error']}; }}

/* ── Listes ─────────────────────────────────────────────────── */
QListWidget {{
    background-color: {c['bg_secondary']};
    border: 1.5px solid {c['border']};
    border-radius: 8px;
    outline: none;
}}
QListWidget::item {{ padding: 9px 12px; border-radius: 6px; margin: 1px 4px; }}
QListWidget::item:selected {{
    background-color: {c['primary']};
    color: white;
}}
QListWidget::item:hover:!selected {{
    background-color: {c['bg_secondary']};
}}

/* ── ScrollBar ──────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {c['border']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0px; }}

/* ── TextEdit ───────────────────────────────────────────────── */
QTextEdit {{
    background-color: {c['bg_secondary']};
    color: {c['text']};
    border: 1.5px solid {c['border']};
    border-radius: 8px;
    padding: 8px;
}}

/* ── GroupBox ───────────────────────────────────────────────── */
QGroupBox {{
    border: 1.5px solid {c['border']};
    border-radius: 10px;
    margin-top: 14px;
    padding: 12px 10px 10px 10px;
    font-weight: 500;
    color: {c['text_secondary']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    background-color: {c['bg']};
    color: {c['text_secondary']};
    font-size: 12px;
}}

/* ── Onglet de rôle (chip sélectionnable) ───────────────────── */
QPushButton[class="role-chip"] {{
    background-color: {c['bg_secondary']};
    color: {c['text_secondary']};
    border: 1.5px solid {c['border']};
    border-radius: 20px;
    padding: 6px 18px;
    font-size: 13px;
}}
QPushButton[class="role-chip"]:hover {{
    border-color: {c['primary']};
    color: {c['primary']};
}}
QPushButton[class="role-chip-active"] {{
    background-color: {c['primary']};
    color: white;
    border: none;
    border-radius: 20px;
    padding: 6px 18px;
    font-size: 13px;
    font-weight: 500;
}}
"""


    return base + _extra_styles(c)


def apply(app, theme: str) -> None:
    app.setStyleSheet(get_stylesheet(theme))

def _extra_styles(c: dict) -> str:
    return f"""
/* ── Onglets de connexion (tabs login) ───────────────────── */
QPushButton[class="tab"] {{
    background-color: {c['bg_secondary']};
    color: {c['text_secondary']};
    font-weight: normal;
    border: 1px solid {c['border']};
    border-radius: 0px;
    padding: 10px 20px;
    font-size: 14px;
}}
QPushButton[class="tab"]:checked {{
    background-color: {c['primary']};
    color: white;
    font-weight: bold;
    border-color: {c['primary']};
}}
QPushButton[class="tab"]:hover:!checked {{
    background-color: {c['border']};
    color: {c['text']};
}}

/* ── Panneau opérations ──────────────────────────────────── */
QFrame#opsBox {{
    background-color: {c['bg_secondary']};
    border: 1px solid {c['border']};
    border-radius: 8px;
}}

/* ── Bouton danger ───────────────────────────────────────── */
QPushButton[class="danger"] {{
    background-color: {c['error']};
    color: white;
    border: none;
}}
QPushButton[class="danger"]:hover {{
    background-color: #c0392b;
}}

/* ── QTabWidget ──────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {c['border']};
    border-radius: 6px;
}}
QTabBar::tab {{
    background: {c['bg_secondary']};
    color: {c['text_secondary']};
    padding: 8px 18px;
    border: 1px solid {c['border']};
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    font-size: 13px;
}}
QTabBar::tab:selected {{
    background: {c['primary']};
    color: white;
    font-weight: bold;
}}

/* ── QTableWidget ────────────────────────────────────────── */
QTableWidget {{
    background-color: {c['bg_secondary']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    gridline-color: {c['border']};
}}
QHeaderView::section {{
    background-color: {c['bg']};
    color: {c['text_secondary']};
    font-weight: bold;
    font-size: 13px;
    padding: 6px;
    border: none;
    border-bottom: 1px solid {c['border']};
}}
QTableWidget::item:selected {{
    background-color: {c['primary']};
    color: white;
}}
"""

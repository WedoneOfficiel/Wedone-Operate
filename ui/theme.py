# ui/theme.py — Wedone Operate
# Transposition native du système Wedone Web Apps / SetScrobble :
# typographies DM Sans + Manrope, surfaces douces, arrondis généreux,
# hiérarchie nette et accent bleu Wedone.
#
# Qt Widgets ne propose pas backdrop-filter. Les surfaces vitrées sont donc
# simulées avec des fonds translucides/contrastés, des bordures fines et des
# dégradés natifs. Aucun rose propre à SetScrobble n'est réutilisé.

from PyQt6.QtGui import QFont
from ui.palette import LIGHT, DARK


def get_stylesheet(theme: str) -> str:
    c = DARK if theme == "dark" else LIGHT
    return f"""
/* ── Base : fond, typographie et hiérarchie ─────────────────── */
QWidget {{
    background-color: {c['bg']};
    color: {c['text']};
    font-family: "DM Sans", "Segoe UI", "Ubuntu", "Cantarell", sans-serif;
    font-size: 13px;
}}
QMainWindow, QDialog {{
    background-color: {c['bg']};
}}
QStackedWidget, QScrollArea, QScrollArea > QWidget > QWidget {{
    background: transparent;
    border: 0;
}}
QFrame {{ background: transparent; }}
QLabel {{ color: {c['text']}; background: transparent; }}
QLabel#title {{
    color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif;
    font-size: 25px; font-weight: 800;
}}
QLabel#section {{
    color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif;
    font-size: 17px; font-weight: 800;
}}
QLabel#subtitle, QLabel#hint {{
    color: {c['text_secondary']}; font-size: 12px;
}}
QLabel#success {{ color: {c['success']}; font-weight: 700; }}
QLabel#error {{ color: {c['error']}; font-weight: 700; }}
QLabel#warning {{ color: {c['warning']}; }}
QLabel#metric {{
    color: {c['primary']}; font-family: "Manrope", "Segoe UI", sans-serif;
    font-size: 28px; font-weight: 800;
}}
QLabel#question {{
    color: {c['text']}; font-family: "Manrope", "Segoe UI", sans-serif;
    font-size: 42px; font-weight: 800;
}}
QLabel#score {{ font-weight: 800; }}
QLabel#feedback {{ font-size: 16px; font-weight: 650; }}

/* ── Surfaces : cartes, panneaux et groupes ────────────────── */
QFrame#opsBox, QFrame[class="card"], QFrame[class="card-selected"],
QFrame[class="warning-card"], QGroupBox {{
    background-color: {c['surface_glass']};
    border: 1px solid {c['border']};
    border-radius: 18px;
}}
QFrame[class="card"]:hover {{
    background-color: {c['surface_hover']};
    border-color: {c['border_hover']};
}}
QFrame[class="card-compact"] {{
    background-color: {c['surface_glass']};
    border: 1px solid {c['border']};
    border-radius: 14px;
}}
QFrame[class="card-selected"] {{
    border: 2px solid {c['primary']};
    background-color: {c['accent_soft']};
}}
QFrame[class="warning-card"] {{
    background-color: {c['surface']};
    border: 1px solid {c['error']};
    border-radius: 16px;
}}
QFrame#templateBanner {{
    background-color: {c['accent_soft']};
    border: 1px solid {c['accent_border']};
    border-radius: 14px;
}}
QGroupBox {{
    margin-top: 16px; padding: 15px 13px 13px;
    color: {c['text_secondary']}; font-weight: 700;
}}
QGroupBox::title {{
    subcontrol-origin: margin; left: 13px; padding: 0 7px;
    background: {c['bg']};
}}

/* ── Champs et listes déroulantes ──────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {c['input']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 13px;
    padding: 10px 12px; selection-background-color: {c['primary']};
    selection-color: white;
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover, QSpinBox:hover,
QDoubleSpinBox:hover, QComboBox:hover {{
    border-color: {c['border_hover']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus,
QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {c['primary']}; background-color: {c['surface']};
}}
QLineEdit#answer-input {{
    font-size: 24px; padding: 13px; border-radius: 15px;
}}
QComboBox {{ padding-right: 28px; }}
QComboBox::drop-down {{
    subcontrol-origin: padding; subcontrol-position: top right;
    width: 26px; border: 0;
}}
QComboBox QAbstractItemView {{
    background-color: {c['surface']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 12px;
    selection-background-color: {c['accent_soft']};
    selection-color: {c['text']}; padding: 5px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px; border: 0; background: transparent;
}}

/* ── Boutons : primaire, secondaire, navigation et danger ──── */
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 {c['primary']}, stop:1 {c['primary_alt']});
    color: {c['primary_text']}; border: 0; border-radius: 13px;
    padding: 10px 18px; min-height: 19px;
    font-size: 13px; font-weight: 700;
}}
QPushButton:hover {{
    background: {c['primary_hover']};
}}
QPushButton:pressed {{
    background: {c['primary_pressed']};
}}
QPushButton:disabled {{
    background: {c['disabled']}; color: {c['text_muted']};
}}
QPushButton[class="secondary"], QPushButton[class="nav"] {{
    background-color: {c['surface']}; color: {c['text_secondary']};
    border: 1px solid {c['border']}; border-radius: 13px;
}}
QPushButton[class="secondary"]:hover, QPushButton[class="nav"]:hover {{
    background-color: {c['surface_hover']};
    border-color: {c['border_hover']}; color: {c['text']};
}}
QPushButton[class="danger"] {{
    background-color: {c['error']}; color: white;
}}
QPushButton[class="danger"]:hover {{ background-color: {c['error_hover']}; }}
QPushButton[class="nav"] {{
    text-align: left; padding: 11px 15px; font-weight: 600;
}}
QPushButton[class="nav-active"] {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
    border: 1px solid {c['accent_border']}; border-radius: 13px;
    text-align: left; padding: 11px 15px; font-weight: 800;
}}
QPushButton[class="role-chip"], QPushButton[class="tab"] {{
    background-color: {c['surface']}; color: {c['text_secondary']};
    border: 1px solid {c['border']}; border-radius: 12px;
    padding: 9px 16px;
}}
QPushButton[class="role-chip-active"], QPushButton[class="tab"]:checked {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
    border: 1px solid {c['accent_border']}; font-weight: 800;
}}
QPushButton[class="student-card"] {{
    background-color: {c['surface_glass']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 16px;
    padding: 6px;
}}
QPushButton[class="student-card"]:hover {{
    background-color: {c['surface_hover']};
    border: 1px solid {c['primary']};
}}
QPushButton[class="student-card"]:pressed {{
    background-color: {c['accent_soft']};
}}

/* ── Cases à cocher, onglets et sélection ──────────────────── */
QCheckBox {{ color: {c['text']}; spacing: 9px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border: 1px solid {c['border']};
    border-radius: 6px; background: {c['input']};
}}
QCheckBox::indicator:checked {{
    background: {c['primary']}; border-color: {c['primary']};
}}
QTabWidget::pane {{
    border: 1px solid {c['border']}; border-radius: 16px; top: -1px;
}}
QTabBar::tab {{
    background: transparent; color: {c['text_secondary']};
    padding: 10px 16px; margin-right: 4px;
    border: 1px solid transparent; border-radius: 11px;
}}
QTabBar::tab:selected {{
    background: {c['accent_soft']}; color: {c['accent_ink']};
    font-weight: 800;
}}
QTabBar::tab:hover:!selected {{ background: {c['surface_hover']}; }}

/* ── Tableaux, progression et navigation ──────────────────── */
QListWidget, QTableWidget, QTreeWidget {{
    background-color: {c['surface']}; color: {c['text']};
    border: 1px solid {c['border']}; border-radius: 16px;
    outline: none; gridline-color: {c['border']};
}}
QListWidget::item {{
    padding: 9px 11px; border-radius: 9px; margin: 2px 5px;
}}
QListWidget::item:selected, QTableWidget::item:selected,
QTreeWidget::item:selected {{
    background-color: {c['accent_soft']}; color: {c['accent_ink']};
}}
QHeaderView::section {{
    background-color: {c['surface_hover']}; color: {c['text_secondary']};
    font-weight: 800; font-size: 11px; padding: 10px;
    border: 0; border-bottom: 1px solid {c['border']};
}}
QProgressBar {{
    background: {c['surface_hover']}; border: 0;
    border-radius: 7px; height: 9px; text-align: center;
}}
QProgressBar::chunk {{ background: {c['primary']}; border-radius: 7px; }}
QProgressBar[class="timer-green"]::chunk {{ background: {c['success']}; }}
QProgressBar[class="timer-orange"]::chunk {{ background: {c['warning']}; }}
QProgressBar[class="timer-red"]::chunk {{ background: {c['error']}; }}
QScrollBar:vertical {{
    background: transparent; width: 8px; margin: 3px;
}}
QScrollBar::handle:vertical {{
    background: {c['scroll']}; border-radius: 4px; min-height: 28px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: transparent; height: 8px; margin: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {c['scroll']}; border-radius: 4px; min-width: 28px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    color: {c['border']}; background: {c['border']};
    border: 0; max-height: 1px;
}}
QToolTip {{
    background: {c['surface']}; color: {c['text']};
    border: 1px solid {c['border']}; padding: 7px 10px;
    border-radius: 9px;
}}
QWidget:focus {{ outline: none; }}
"""


def apply(app, theme: str) -> None:
    app.setFont(QFont("DM Sans", 10))
    app.setStyleSheet(get_stylesheet(theme))

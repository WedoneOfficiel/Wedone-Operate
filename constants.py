# constants.py — Wedone Operate 2026.03.17

APP_VERSION = "2026.03.17"
APP_NAME    = "Wedone Operate"
GITHUB_REPO = "WedoneOfficiel/Wedone-Operate"

# ══════════════════════════════════════════════════════════════════════
# NIVEAUX SCOLAIRES — du CP au Lycée
# Plages pédagogiquement cohérentes avec les programmes officiels
# ══════════════════════════════════════════════════════════════════════

SCHOOL_LEVELS = ["CP", "CE1", "CE2", "CM1", "CM2", "6e", "5e", "4e", "3e", "Lycée"]

# Format par opération : (min_a, max_a, min_b, max_b)
# Pour division : (min_diviseur, max_diviseur, min_quotient, max_quotient)
LEVEL_RANGES = {
    "CP": {
        # CP : additions/soustractions jusqu'à 10, pas de × ni ÷
        "addition":       (1, 9,  1, 9),
        "soustraction":   (1, 10, 1, 9),
        "multiplication": (1, 2,  1, 5),   # tables de 2 seulement
        "division":       (1, 2,  1, 5),
    },
    "CE1": {
        # CE1 : nombres jusqu'à 20, tables × 2 et 5
        "addition":       (1, 20, 1, 20),
        "soustraction":   (1, 20, 1, 19),
        "multiplication": (1, 5,  1, 5),
        "division":       (1, 5,  1, 5),
    },
    "CE2": {
        # CE2 : jusqu'à 100, tables jusqu'à 5
        "addition":       (1, 50, 1, 50),
        "soustraction":   (1, 50, 1, 49),
        "multiplication": (1, 5,  1, 10),
        "division":       (1, 5,  1, 10),
    },
    "CM1": {
        # CM1 : jusqu'à 100, tables jusqu'à 9
        "addition":       (1, 100, 1, 100),
        "soustraction":   (1, 100, 1, 99),
        "multiplication": (1, 9,   1, 10),
        "division":       (1, 9,   1, 10),
    },
    "CM2": {
        # CM2 : jusqu'à 1000, toutes les tables
        "addition":       (1, 500, 1, 500),
        "soustraction":   (1, 500, 1, 499),
        "multiplication": (1, 10,  1, 10),
        "division":       (1, 10,  1, 10),
    },
    "6e": {
        # 6e : grands nombres, introduction aux fractions mentales
        "addition":       (1,  999, 1, 999),
        "soustraction":   (1,  999, 1, 998),
        "multiplication": (1,  12,  1, 12),
        "division":       (1,  12,  1, 12),
    },
    "5e": {
        # 5e : calculs plus complexes
        "addition":       (1,  9999, 1, 9999),
        "soustraction":   (1,  9999, 1, 9998),
        "multiplication": (2,  15,   2, 15),
        "division":       (2,  15,   2, 15),
    },
    "4e": {
        "addition":       (1,  9999, 1, 9999),
        "soustraction":   (1,  9999, 1, 9998),
        "multiplication": (2,  20,   2, 20),
        "division":       (2,  20,   2, 20),
    },
    "3e": {
        "addition":       (1,  99999, 1, 99999),
        "soustraction":   (1,  99999, 1, 99998),
        "multiplication": (2,  25,    2, 25),
        "division":       (2,  25,    2, 25),
    },
    "Lycée": {
        "addition":       (1,  99999, 1, 99999),
        "soustraction":   (1,  99999, 1, 99998),
        "multiplication": (2,  50,    2, 50),
        "division":       (2,  50,    2, 50),
    },
}

# Alias "difficulté" conservé pour compatibilité ascendante (screen_main)
# Facile/Moyen/Difficile = mapping vers des niveaux scolaires représentatifs
DIFFICULTY_LEVELS  = ["Facile", "Moyen", "Difficile"]
DIFFICULTY_RANGES  = {
    "Facile":    LEVEL_RANGES["CE1"],
    "Moyen":     LEVEL_RANGES["CM2"],
    "Difficile": LEVEL_RANGES["3e"],
}

# ── Chronomètres par niveau scolaire ──────────────────────────────────
# Plus le niveau est bas, plus on donne de temps
TIMER_SECONDS_BY_LEVEL = {
    "CP":    45, "CE1":  40, "CE2":  35,
    "CM1":   30, "CM2":  25, "6e":   20,
    "5e":    18, "4e":   15, "3e":   12,
    "Lycée": 10,
}
# Alias pour compatibilité
TIMER_SECONDS = {
    "Facile": 40, "Moyen": 25, "Difficile": 12,
}

# ── Identité visuelle Wedone — palettes clair / sombre ────────────────
# Palette inspirée du portail Wedone : lavande, rose et surfaces vitrées.
LIGHT = {
    "bg": "#F7F5FC",
    "bg_secondary": "#F0ECF8",
    "surface": "#FFFFFF",
    "surface_hover": "#FAF7FD",
    "input": "#FFFFFF",
    "border": "#E8E1F0",
    "border_hover": "#D5C5E8",
    "primary": "#8B5BC7",
    "primary_alt": "#B16BD1",
    "primary_hover": "#7545B0",
    "primary_pressed": "#633A99",
    "primary_text": "#FFFFFF",
    "accent_soft": "#F0E8FB",
    "accent_ink": "#68449A",
    "accent_border": "#DCC9F1",
    "text": "#29243B",
    "text_secondary": "#79748C",
    "text_muted": "#AAA5B8",
    "success": "#269B70",
    "error": "#D94B62",
    "error_hover": "#BC354D",
    "warning": "#D58A27",
    "disabled": "#E5E0EA",
    "scroll": "#D8D0E2",
}
DARK = {
    "bg": "#15131D",
    "bg_secondary": "#211D2B",
    "surface": "#211E2C",
    "surface_hover": "#2B2638",
    "input": "#1B1825",
    "border": "#393246",
    "border_hover": "#5A4A70",
    "primary": "#A77AD8",
    "primary_alt": "#C18AE0",
    "primary_hover": "#BD91E8",
    "primary_pressed": "#8F62C4",
    "primary_text": "#FFFFFF",
    "accent_soft": "#382B4B",
    "accent_ink": "#E0C8FA",
    "accent_border": "#604879",
    "text": "#F1EDF8",
    "text_secondary": "#B1A9C1",
    "text_muted": "#81798F",
    "success": "#55C99A",
    "error": "#F0788B",
    "error_hover": "#E45E75",
    "warning": "#E8B45C",
    "disabled": "#40394B",
    "scroll": "#51475F",
}

# ── Fichiers ──────────────────────────────────────────────────────────
SETTINGS_FILE  = "settings.json"
USERS_FILE     = "users.json"
GROUPS_FILE    = "groups.json"
SCORES_FILE    = "scores.json"
TEMPLATES_FILE = "templates.json"

# ── Sécurité ──────────────────────────────────────────────────────────
DEFAULT_ADMIN_PASSWORD_PLAIN = "admin1234"

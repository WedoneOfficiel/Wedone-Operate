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

# ── Palettes ──────────────────────────────────────────────────────────
LIGHT = {
    "bg":            "#FFFFFF",
    "bg_secondary":  "#F4F6F9",
    "surface":       "#FFFFFF",
    "border":        "#DDE3EC",
    "primary":       "#0672BC",
    "primary_hover": "#0558A0",
    "primary_text":  "#FFFFFF",
    "text":          "#1A1D23",
    "text_secondary":"#5A6270",
    "success":       "#1C8A4E",
    "error":         "#C0392B",
    "warning":       "#E07B00",
    "disabled":      "#B0B8C4",
}
DARK = {
    "bg":            "#141720",
    "bg_secondary":  "#1E2230",
    "surface":       "#252A3A",
    "border":        "#353C52",
    "primary":       "#3A8FD6",
    "primary_hover": "#5AA8E8",
    "primary_text":  "#FFFFFF",
    "text":          "#E8ECF4",
    "text_secondary":"#8A95AA",
    "success":       "#2EBD6E",
    "error":         "#E05555",
    "warning":       "#F0A030",
    "disabled":      "#444C60",
}

# ── Fichiers ──────────────────────────────────────────────────────────
SETTINGS_FILE  = "settings.json"
USERS_FILE     = "users.json"
GROUPS_FILE    = "groups.json"
SCORES_FILE    = "scores.json"
TEMPLATES_FILE = "templates.json"

# ── Sécurité ──────────────────────────────────────────────────────────
DEFAULT_ADMIN_PASSWORD_PLAIN = "admin1234"

# settings.py — Wedone Operate
# Gestion du fichier settings.json : chargement, sauvegarde, valeurs par défaut.

import json
import os
import platform
from constants import SETTINGS_FILE


# ---------------------------------------------------------------------------
# Détection du thème système (Windows / Linux GNOME)
# ---------------------------------------------------------------------------
def _detect_system_theme() -> str:
    """Retourne 'dark' ou 'light' selon le thème du système d'exploitation."""
    system = platform.system()

    if system == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if value == 1 else "dark"
        except Exception:
            return "light"

    elif system == "Linux":
        try:
            import subprocess
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True, text=True
            )
            return "dark" if "dark" in result.stdout.lower() else "light"
        except Exception:
            return "light"

    return "light"


# ---------------------------------------------------------------------------
# Valeurs par défaut
# ---------------------------------------------------------------------------
def _default_settings() -> dict:
    return {
        # Thème : "system" | "light" | "dark"
        "theme": "system",

        # Mises à jour
        "auto_update": True,

        # Épreuves — opérations activées
        "addition_enabled":       True,
        "subtraction_enabled":    True,
        "multiplication_enabled": True,
        "division_enabled":       True,

        # Épreuves — difficulté par défaut
        "difficulty": "Moyen",

        # Chronomètre
        "timer_enabled": False,

        # Dernier profil sélectionné (nom complet ou None)
        "last_profile": None,
    }


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------
def load() -> dict:
    """Charge settings.json. Crée le fichier avec les valeurs par défaut si absent."""
    defaults = _default_settings()
    if not os.path.exists(SETTINGS_FILE):
        save(defaults)
        return defaults

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Fusion : on conserve les clés inconnues mais on garantit les clés requises
        for key, val in defaults.items():
            data.setdefault(key, val)
        return data
    except (json.JSONDecodeError, OSError):
        save(defaults)
        return defaults


def save(settings: dict) -> None:
    """Sauvegarde settings.json."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def resolve_theme(settings: dict) -> str:
    """
    Retourne le thème effectif ('light' ou 'dark') en tenant compte
    du choix 'system' qui délègue à la détection OS.
    """
    choice = settings.get("theme", "system")
    if choice == "system":
        return _detect_system_theme()
    return choice  # 'light' ou 'dark'

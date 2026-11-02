# settings.py — Wedone Operate
# Gestion du fichier settings.json : chargement, sauvegarde, valeurs par défaut.

import json
import os
import platform
from data_paths import data_file
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
                capture_output=True, text=True, timeout=2
            )
            return "dark" if "dark" in result.stdout.lower() else "light"
        except Exception:
            return "light"

    elif system == "Darwin":
        try:
            import subprocess
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True, timeout=2
            )
            return "dark" if result.stdout.strip().lower() == "dark" else "light"
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
        "difficulty": "CM2",

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
    settings_path = data_file(SETTINGS_FILE)
    if not settings_path.exists():
        save(defaults)
        return defaults

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Fusion : on conserve les clés inconnues mais on garantit les clés requises
        for key, val in defaults.items():
            data.setdefault(key, val)
        return data
    except (json.JSONDecodeError, OSError):
        # Keep the original settings file for recovery; never overwrite it
        # automatically when it is malformed or temporarily unreadable.
        return defaults


def save(settings: dict) -> None:
    """Atomically save settings.json."""
    import tempfile

    settings_path = data_file(SETTINGS_FILE)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        prefix=f".{settings_path.name}.", suffix=".tmp", dir=str(settings_path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, settings_path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def resolve_theme(settings: dict) -> str:
    """
    Retourne le thème effectif ('light' ou 'dark') en tenant compte
    du choix 'system' qui délègue à la détection OS.
    """
    choice = settings.get("theme", "system")
    if choice == "system":
        return _detect_system_theme()
    return choice  # 'light' ou 'dark'

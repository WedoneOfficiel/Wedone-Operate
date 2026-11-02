# updater.py — Wedone Operate
# Vérification des mises à jour via l'API GitHub Releases.

import re

import requests
from constants import APP_VERSION, GITHUB_REPO


RELEASES_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases"
TIMEOUT = 5  # secondes

# Les releases historiques utilisent notamment "Stable-v2026.03.17".
# On extrait la version numérique sans dépendre du préfixe de canal.
_VERSION_PATTERN = re.compile(r"\d+(?:\.\d+){1,3}")


def _normalize_version_tag(tag: str) -> str:
    """Extrait une version numérique d'un tag (ex. Stable-v2026.03.17)."""
    match = _VERSION_PATTERN.search(str(tag or "").strip())
    return match.group(0) if match else ""


def _parse_version(tag: str) -> tuple[int, ...]:
    """
    Convertit un tag en tuple comparable.
    Accepte notamment 2026.03.17, v2026.03.17 et Stable-v2026.03.17.
    Un tag sans version numérique renvoie un tuple vide.
    """
    normalized = _normalize_version_tag(tag)
    if not normalized:
        return ()
    try:
        return tuple(int(part) for part in normalized.split("."))
    except ValueError:
        return ()


def check_for_update() -> dict | None:
    """
    Retourne les informations de mise à jour si la dernière release est
    strictement plus récente que la version installée.

    Les erreurs réseau ou les réponses GitHub invalides ne bloquent pas
    le démarrage de l'application.
    """
    try:
        response = requests.get(RELEASES_API, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        raw_tag = data.get("tag_name", "")
        latest_version = _parse_version(raw_tag)
        current_version = _parse_version(APP_VERSION)
        if not latest_version or not current_version:
            return None

        if latest_version > current_version:
            return {
                "version": _normalize_version_tag(raw_tag),
                "url": data.get("html_url") or RELEASES_PAGE,
                "changelog": data.get("body") or "Aucune note de version disponible.",
            }

        return None

    except (requests.exceptions.RequestException, ValueError, TypeError, AttributeError):
        return None

# updater.py — Wedone Operate
# Vérification des mises à jour via l'API GitHub Releases.
# Logique : chaque release GitHub est identifiée par son tag (ex. "2026.03.17").
# Une version est considérée plus récente si son tag est lexicographiquement supérieur.

import requests
from constants import APP_VERSION, GITHUB_REPO


RELEASES_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
RELEASES_PAGE = f"https://github.com/{GITHUB_REPO}/releases"
TIMEOUT = 5  # secondes


def _parse_version(tag: str) -> tuple[int, ...]:
    """
    Convertit un tag "2026.03.17" en tuple (2026, 3, 17) pour comparaison fiable.
    Ignore les préfixes éventuels comme 'v'.
    """
    tag = tag.lstrip("v").strip()
    try:
        return tuple(int(x) for x in tag.split("."))
    except ValueError:
        return (0,)


def check_for_update() -> dict | None:
    """
    Interroge l'API GitHub Releases.

    Retourne un dict si une mise à jour est disponible :
        {
            "version":   "2026.06.01",
            "url":       "https://github.com/.../releases/tag/2026.06.01",
            "changelog": "- Nouvelle feature\n- Correction de bug",
        }

    Retourne None si le logiciel est à jour ou si la vérification échoue.
    """
    try:
        response = requests.get(RELEASES_API, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        latest_tag  = data.get("tag_name", "").lstrip("v").strip()
        changelog   = data.get("body", "Aucune note de version disponible.")
        release_url = data.get("html_url", RELEASES_PAGE)

        if not latest_tag:
            return None

        if _parse_version(latest_tag) > _parse_version(APP_VERSION):
            return {
                "version":   latest_tag,
                "url":       release_url,
                "changelog": changelog,
            }

        return None

    except requests.exceptions.RequestException:
        return None

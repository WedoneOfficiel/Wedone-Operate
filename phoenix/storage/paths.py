"""Platform-specific Phoenix paths; deliberately separate from legacy data."""

import os
import platform
from pathlib import Path

APP_DATA_DIR_NAME = "Wedone Operate Phoenix"
DATABASE_FILENAME = "phoenix.sqlite3"


def get_phoenix_data_dir() -> Path:
    """Return the per-user Phoenix directory without touching legacy files."""
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / APP_DATA_DIR_NAME


def get_database_path() -> Path:
    """Return the database path; directory creation is explicit at DB startup."""
    return get_phoenix_data_dir() / DATABASE_FILENAME

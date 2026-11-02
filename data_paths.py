import os
import platform
import shutil
from pathlib import Path

APP_DATA_DIR_NAME = "Wedone Operate"

def get_data_dir() -> Path:
    """Return the per-user application data directory for this OS."""
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
        return base / APP_DATA_DIR_NAME
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / APP_DATA_DIR_NAME
    base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / "wedone-operate"

def data_file(filename: str) -> Path:
    """Resolve a data file and safely copy a legacy CWD file on first use."""
    if Path(filename).name != filename:
        raise ValueError("Le nom de fichier doit être simple, sans chemin.")
    directory = get_data_dir()
    destination = directory / filename
    if destination.exists():
        return destination
    directory.mkdir(parents=True, exist_ok=True)
    legacy = Path.cwd() / filename
    if legacy.is_file():
        try:
            shutil.copy2(legacy, destination)
        except OSError:
            pass
    return destination

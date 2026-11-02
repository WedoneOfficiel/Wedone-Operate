"""Helpers for locating bundled application resources (source and PyInstaller)."""
import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """Return an absolute resource path in development or a frozen bundle."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return str(base / relative_path)

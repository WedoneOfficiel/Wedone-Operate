"""Locate the Qt Quick QML runtime across PySide6 wheel layouts."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

try:
    import PySide6
except ImportError as exc:
    raise SystemExit(f"PySide6 Essentials is not installed: {exc}") from exc

spec = importlib.util.find_spec("PySide6")
locations = list(spec.submodule_search_locations or []) if spec else []
if not locations:
    raise SystemExit("PySide6 package location could not be resolved.")
package_root = Path(locations[0]).resolve()
matches = [
    qmldir for qmldir in package_root.rglob("qmldir")
    if qmldir.parent.name == "Controls"
    and qmldir.parent.parent.name == "QtQuick"
]
if not matches:
    candidates = [package_root / "Qt" / "qml", package_root / "qml"]
    for candidate in candidates:
        if candidate.is_dir():
            print(candidate)
            raise SystemExit(0)
    raise SystemExit(
        f"Qt QML runtime not found below {package_root}; checked Qt/qml and qml."
    )

# Normalize the destination to PySide6/Qt/qml inside every PyInstaller build.
print(matches[0].parents[2])

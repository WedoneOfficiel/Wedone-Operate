"""Validate a built Phoenix distribution before it is archived."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_phoenix_distribution.py <distribution-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Distribution directory does not exist: {root}", file=sys.stderr)
        return 1

    forbidden = [
        path for path in root.rglob("*")
        if "qtwebengine" in str(path.relative_to(root)).lower()
        or path.name.lower() in {
            "assistant.app", "designer.app", "linguist.app",
            "assistant__dot__app", "designer__dot__app", "linguist__dot__app",
        }
    ]
    if forbidden:
        print("Forbidden optional Qt components found:")
        for path in forbidden:
            print(f"  {path.relative_to(root)}")
        return 1

    app_qml = list(root.rglob("Main.qml"))
    if not app_qml or not any("phoenix" in path.parts for path in app_qml):
        print("Phoenix Main.qml was not included in the distribution.", file=sys.stderr)
        return 1

    glass_shaders = list(root.rglob("glass.frag.qsb"))
    if not glass_shaders:
        print("Compiled Liquid Glass shader is missing from the distribution.", file=sys.stderr)
        return 1

    controls = [
        path for path in root.rglob("qmldir")
        if path.parent.name == "Controls" and path.parent.parent.name == "QtQuick"
    ]
    if not controls:
        print("QtQuick.Controls QML runtime is missing.", file=sys.stderr)
        return 1

    print(f"Validated Phoenix distribution: {root}")
    print("Phoenix QML entry point, QtQuick.Controls runtime and Liquid Glass shader are present.")
    print("No QtWebEngine or standalone Qt desktop tools are bundled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

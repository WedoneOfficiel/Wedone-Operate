"""Compile Qt 6 QML shader sources into portable QSB assets."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "phoenix" / "ui" / "qml" / "shaders" / "glass.frag"
TARGET = SOURCE.with_suffix(SOURCE.suffix + ".qsb")


def find_qsb() -> str | None:
    executable = shutil.which("qsb")
    if executable:
        return executable
    try:
        import PySide6
        package = Path(PySide6.__file__).resolve().parent
    except Exception:
        return None
    for candidate in (
        package / "Qt" / "libexec" / ("qsb.exe" if sys.platform == "win32" else "qsb"),
        package / "Qt" / "bin" / ("qsb.exe" if sys.platform == "win32" else "qsb"),
    ):
        if candidate.is_file():
            return str(candidate)
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--required", action="store_true")
    args = parser.parse_args()
    if TARGET.is_file():
        print(f"Shader already compiled: {TARGET}")
        return 0
    compiler = find_qsb()
    if not compiler:
        print("Qt ShaderTools qsb compiler was not found.")
        return 1 if args.required else 0
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([compiler, "--qt6", "-o", str(TARGET), str(SOURCE)], check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Could not compile Liquid Glass shader: {exc}", file=sys.stderr)
        return 1
    print(f"Compiled shader: {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

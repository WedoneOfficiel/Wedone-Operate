# -*- mode: python ; coding: utf-8 -*-
"""macOS bundle recipe for Phoenix.

PySide6's collect_all() also discovers standalone Qt development tools
(Assistant, Designer, Linguist). Those are not runtime dependencies of this
application and their nested .app bundles contain symlink layouts that break
PyInstaller's recursive macOS bundle signing. Exclude those bundles at
analysis time instead of deleting files from the completed .app bundle.
"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

ROOT = Path(SPECPATH).resolve()
APP_NAME = "Wedone Operate Phoenix"
ICON = str(ROOT / "phoenix.icns")


def is_standalone_app_bundle(entry):
    """Return True for any TOC entry inside a nested *.app bundle."""
    for value in entry[:2]:
        normalized = str(value).replace("\\", "/").lower()
        parts = normalized.split("/")
        if any(part.endswith(".app") or part.endswith("__dot__app") for part in parts):
            return True
    return False


datas, binaries, hiddenimports = collect_all("PySide6")

# Keep the Qt runtime, QML modules and plugins, but do not ship Qt's separate
# desktop tools inside our application bundle.
datas = [entry for entry in datas if not is_standalone_app_bundle(entry)]
binaries = [entry for entry in binaries if not is_standalone_app_bundle(entry)]

# Fail during analysis if a helper app slipped through the collection.
assert not any(is_standalone_app_bundle(entry) for entry in datas + binaries)

datas += [
    (str(ROOT / "phoenix" / "ui" / "qml"), "phoenix/ui/qml"),
    (str(ROOT / "icon.png"), "."),
]

a = Analysis(
    [str(ROOT / "phoenix_entry.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="arm64",
    codesign_identity="-",
    entitlements_file=None,
    icon=ICON,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

app = BUNDLE(
    coll,
    name=f"{APP_NAME}.app",
    icon=ICON,
    bundle_identifier="fr.wedoneofficiel.wedoneoperate.phoenix",
    info_plist={"NSHighResolutionCapable": "True"},
    codesign_identity="-",
    entitlements_file=None,
)

# -*- mode: python ; coding: utf-8 -*-
"""Lean macOS arm64 bundle for the Phoenix Qt Quick application.

Phoenix depends on PySide6 Essentials, not the PySide6 meta-package/Addons.
The runtime QML tree is copied as data; unused WebEngine entries are filtered
again after Analysis as a defensive guard against future hook regressions.
"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).resolve()
APP_NAME = "Wedone Operate Phoenix"
ICON = str(ROOT / "phoenix.icns")

qml_datas = collect_data_files(
    "PySide6",
    includes=["Qt/qml/**"],
    excludes=["Qt/qml/QtWebEngine/**", "Qt/qml/QtWebEngine"],
)

datas = qml_datas + [
    (str(ROOT / "phoenix" / "ui" / "qml"), "phoenix/ui/qml"),
    (str(ROOT / "icon.png"), "."),
]

a = Analysis(
    [str(ROOT / "phoenix_entry.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=["AppKit", "Foundation", "objc"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineQuick",
        "PySide6.QtWebEngineWidgets",
        "PySide6.scripts",
    ],
    noarchive=False,
)

# PyInstaller's Qt hooks can collect optional framework binaries even when
# the application never imports them. Filter the final TOCs, not just the
# source QML directory, so no hook can reintroduce QtWebEngine into the app.
a.binaries = type(a.binaries)(
    entry for entry in a.binaries if "qtwebengine" not in entry[0].lower()
)
a.datas = type(a.datas)(
    entry for entry in a.datas if "qtwebengine" not in entry[0].lower()
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
    upx=False,
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
    upx=False,
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

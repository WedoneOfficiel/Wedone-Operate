# -*- mode: python ; coding: utf-8 -*-
"""Minimal macOS bundle recipe for Phoenix.

Do not use collect_all("PySide6") here: it pulls every optional Qt module,
including QtWebEngine, and adds several minutes to COLLECT/signing. Phoenix
imports only QtCore, QtGui, QtQml and QtQuick. PyInstaller's normal PySide6
hooks collect the matching Qt frameworks/plugins; this recipe adds the QML
runtime tree as data while explicitly omitting QtWebEngine.
"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).resolve()
APP_NAME = "Wedone Operate Phoenix"
ICON = str(ROOT / "phoenix.icns")

# Qt Quick Controls/Layouts/Dialogs are QML modules, not Python modules.
# Keep the installed QML runtime tree (including its module plugins and
# qmldir metadata), but do not ship the unused WebEngine QML modules.
qml_datas = collect_data_files(
    "PySide6",
    includes=["Qt/qml/**"],
    excludes=[
        "Qt/qml/QtWebEngine/**",
        "Qt/qml/QtWebEngine",
    ],
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
    hiddenimports=[],
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

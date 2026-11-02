# -*- mode: python ; coding: utf-8 -*-
"""macOS bundle recipe for Phoenix.

Phoenix uses Qt Quick, QML, Controls, Layouts and Dialogs. It does not use
QtWebEngine or Qt's standalone desktop development tools. Keep the Qt runtime
collection, but exclude those unrelated modules and nested applications before
PyInstaller assembles and signs the macOS bundle.
"""

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

ROOT = Path(SPECPATH).resolve()
APP_NAME = "Wedone Operate Phoenix"
ICON = str(ROOT / "phoenix.icns")


def normalized_entry_paths(entry):
    return [str(value).replace("\\", "/").lower() for value in entry[:2]]


def is_unneeded_qt_component(entry):
    """Exclude QtWebEngine and standalone Qt desktop tools."""
    for value in normalized_entry_paths(entry):
        parts = value.split("/")
        if any(part.startswith("qtwebengine") for part in parts):
            return True
        if any(
            part in {
                "assistant.app", "designer.app", "linguist.app",
                "assistant__dot__app", "designer__dot__app", "linguist__dot__app",
            }
            for part in parts
        ):
            return True
    return False


datas, binaries, hiddenimports = collect_all("PySide6")

# QtWebEngine is not imported by Python or by Main.qml. In particular, do not
# ship its helper application (QtWebEngineProcess.app) just because collect_all
# discovered every optional PySide6 module.
datas = [entry for entry in datas if not is_unneeded_qt_component(entry)]
binaries = [entry for entry in binaries if not is_unneeded_qt_component(entry)]
hiddenimports = [
    module for module in hiddenimports
    if not module.lower().startswith("pyside6.qtwebengine")
]

assert not any(is_unneeded_qt_component(entry) for entry in datas + binaries)
assert not any(module.lower().startswith("pyside6.qtwebengine") for module in hiddenimports)

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
    excludes=["PySide6.QtWebEngineCore", "PySide6.QtWebEngineQuick", "PySide6.QtWebEngineWidgets"],
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

"""Cross-platform native window effects and Qt Quick shader preparation."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Property, Signal, Slot


def _qml_root() -> Path:
    return Path(__file__).resolve().parent / "qml"


def _shader_binary() -> Path:
    return _qml_root() / "shaders" / "glass.frag.qsb"


def _find_qsb() -> str | None:
    found = shutil.which("qsb")
    if found:
        return found
    try:
        import PySide6
        package = Path(PySide6.__file__).resolve().parent
    except Exception:
        return None
    candidates = (
        package / "Qt" / "libexec" / ("qsb.exe" if os.name == "nt" else "qsb"),
        package / "Qt" / "bin" / ("qsb.exe" if os.name == "nt" else "qsb"),
    )
    return next((str(path) for path in candidates if path.is_file()), None)


class PlatformEffects(QObject):
    nativeBackdropChanged = Signal()
    shaderAvailableChanged = Signal()
    backendChanged = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._native_backdrop = False
        self._shader_available = _shader_binary().is_file()
        self._backend = self._describe_backend()

    @Property(bool, notify=nativeBackdropChanged)
    def nativeBackdropApplied(self) -> bool:
        return self._native_backdrop

    @Property(bool, notify=shaderAvailableChanged)
    def shaderAvailable(self) -> bool:
        return self._shader_available

    @Property(str, notify=backendChanged)
    def backend(self) -> str:
        return self._backend

    def _describe_backend(self) -> str:
        if sys.platform == "win32":
            return "Windows DWM · Desktop Acrylic + Qt Quick"
        if sys.platform == "darwin":
            return "macOS AppKit · NSVisualEffectView + Qt Quick"
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Linux")
        session = os.environ.get("XDG_SESSION_TYPE", "unknown")
        return f"{desktop} / {session} · Qt Quick fallback"

    @Slot(result=bool)
    def prepare_shader_assets(self) -> bool:
        target = _shader_binary()
        if target.is_file():
            self._set_shader_available(True)
            return True
        compiler = _find_qsb()
        source = _qml_root() / "shaders" / "glass.frag"
        if not compiler or not source.is_file():
            self._set_shader_available(False)
            return False
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([compiler, "--qt6", "-o", str(target), str(source)],
                           check=True, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            self._set_shader_available(False)
            return False
        self._set_shader_available(target.is_file())
        return self._shader_available

    def _set_shader_available(self, value: bool) -> None:
        value = bool(value)
        if value != self._shader_available:
            self._shader_available = value
            self.shaderAvailableChanged.emit()

    def _set_native_backdrop(self, value: bool) -> None:
        value = bool(value)
        if value != self._native_backdrop:
            self._native_backdrop = value
            self.nativeBackdropChanged.emit()

    @Slot(QObject)
    def applyToWindow(self, window: QObject) -> None:
        applied = False
        try:
            if sys.platform == "win32":
                applied = self._apply_windows(window)
            elif sys.platform == "darwin":
                applied = self._apply_macos(window)
            # Linux compositor blur protocols are not universal; the QML
            # shader remains active instead of advertising a fake native blur.
        except Exception:
            applied = False
        self._set_native_backdrop(applied)

    @staticmethod
    def _apply_windows(window: QObject) -> bool:
        import ctypes
        from ctypes import wintypes

        hwnd = int(window.winId())
        if not hwnd:
            return False
        dwmapi = ctypes.WinDLL("dwmapi")
        backdrop = wintypes.DWORD(3)  # DWMSBT_TRANSIENTWINDOW / Desktop Acrylic
        result = dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd), 38, ctypes.byref(backdrop), ctypes.sizeof(backdrop)
        )
        if result != 0:
            return False
        dark = wintypes.BOOL(1)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd), 20, ctypes.byref(dark), ctypes.sizeof(dark)
        )
        return True

    @staticmethod
    def _apply_macos(window: QObject) -> bool:
        import objc
        from AppKit import (
            NSViewWidthSizable, NSViewHeightSizable, NSWindowBelow,
            NSVisualEffectView, NSVisualEffectMaterialHUDWindow,
            NSVisualEffectBlendingModeWithinWindow, NSVisualEffectStateActive,
        )

        native_view = objc.objc_object(c_void_p=int(window.winId()))
        native_window = native_view.window()
        if native_window is None:
            return False
        content_view = native_window.contentView()
        effect = NSVisualEffectView.alloc().initWithFrame_(content_view.bounds())
        effect.setMaterial_(NSVisualEffectMaterialHUDWindow)
        effect.setBlendingMode_(NSVisualEffectBlendingModeWithinWindow)
        effect.setState_(NSVisualEffectStateActive)
        effect.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        content_view.setWantsLayer_(True)
        if content_view.layer() is not None:
            content_view.layer().setOpaque_(False)
        content_view.addSubview_positionedRelativeTo_(effect, NSWindowBelow, native_view)
        native_window.setOpaque_(False)
        return True

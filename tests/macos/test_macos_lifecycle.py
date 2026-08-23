from __future__ import annotations

import platform
import tkinter as tk

import pytest

from ftproductlab.gui.app import MainWindow


@pytest.mark.macos
@pytest.mark.skipif(platform.system() != "Darwin", reason="macOS-specific real window smoke")
def test_real_macos_window_lifecycle() -> None:
    root = tk.Tk()
    window = MainWindow(root)
    root.update()
    assert window.winfo_exists()
    root.destroy()

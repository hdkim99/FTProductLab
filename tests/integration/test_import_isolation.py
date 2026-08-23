from __future__ import annotations

import subprocess
import sys


def test_core_and_cli_do_not_import_gui_or_plotting_backends() -> None:
    code = """
import sys
import ftproductlab
import ftproductlab.cli.main
for forbidden in ('tkinter', 'matplotlib', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6'):
    assert forbidden not in sys.modules, forbidden
"""
    subprocess.run([sys.executable, "-c", code], check=True)

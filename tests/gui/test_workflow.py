from __future__ import annotations

import tkinter as tk
from pathlib import Path

import pytest

from ftproductlab.gui.app import MainWindow


@pytest.mark.gui
def test_window_main_workflow_export_and_close(tmp_path: Path) -> None:
    root = tk.Tk()
    root.withdraw()
    try:
        window = MainWindow(root)
        window.input_path.set(str(Path("examples/sample_distribution.csv").resolve()))
        window.output_path.set(str(tmp_path / "gui-report"))
        window.fit_minimum.set("5")
        window.fit_maximum.set("20")
        window.cut_specs.set("C1:1:1; Light:2:4; C5+:5")
        result = window.run_analysis(show_dialog=False)
        root.update_idletasks()
        assert result is not None
        assert window.last_result is result
        assert [cut.label for cut in result.cuts] == ["C1", "Light", "C5+"]
        assert len(window.results.get_children()) == len(result.points)
        assert (tmp_path / "gui-report" / "analysis.json").is_file()
        assert (tmp_path / "gui-report" / "asf_fit.svg").is_file()
    finally:
        root.destroy()

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_analyze_and_export(tmp_path: Path) -> None:
    output = tmp_path / "report"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "ftproductlab",
            "analyze",
            "examples/sample_distribution.csv",
            "--basis",
            "molar",
            "--fit-min",
            "5",
            "--fit-max",
            "20",
            "--output",
            os.fspath(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert 0 < payload["fit"]["alpha"] < 1
    assert {path.name for path in output.iterdir()} == {
        "analysis.json",
        "cuts.csv",
        "op_ratios.csv",
        "points.csv",
    }


def test_cli_validation() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "ftproductlab", "validate"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(completed.stdout)["error"] < 1e-12

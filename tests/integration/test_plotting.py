from __future__ import annotations

import struct
from pathlib import Path
from typing import Any

import pytest

from ftproductlab.application import AnalysisRequest, analyze_file
from ftproductlab.core import InputBasis
from ftproductlab.plotting import export_publication_figures, export_social_preview


def test_all_figure_formats_and_preview_dimensions(tmp_path: Path) -> None:
    result = analyze_file(
        AnalysisRequest(Path("examples/sample_distribution.csv"), InputBasis.MOLAR, 5, 20)
    )
    created = export_publication_figures(result, tmp_path)
    assert {path.suffix for path in created} == {".png", ".svg", ".pdf"}
    preview = export_social_preview(result, tmp_path / "preview.png")
    png_header = preview.read_bytes()[:24]
    width, height = struct.unpack(">II", png_header[16:24])
    assert (width, height) == (1280, 640)


def test_cambridge_fit_plot_uses_the_observed_measured_range_denominator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Regression for the plotting discrepancy exposed by CAM.92264 Fig. 1."""

    result = analyze_file(
        AnalysisRequest(
            Path("tests/fixtures/regression/cambridge_fig1_fr1_excerpt.csv"),
            InputBasis.MOLAR,
            30,
            50,
        )
    )
    assert result.fit.alpha == pytest.approx(0.9299914762, abs=1e-10)
    assert result.fit.r_squared == pytest.approx(0.9973376575, abs=1e-10)
    captured: dict[str, Any] = {}

    def capture_asf_figure(
        figure: Any, directory: Path, stem: str, formats: tuple[str, ...]
    ) -> list[Path]:
        del directory, formats
        if stem == "asf_fit":
            captured["fitted"] = tuple(figure.axes[0].lines[1].get_ydata())
            captured["ylabel"] = figure.axes[0].get_ylabel()
        return []

    monkeypatch.setattr("ftproductlab.plotting.figures._save", capture_asf_figure)
    export_publication_figures(result, tmp_path, formats=("png",))

    observed_total = sum(point.observed_molar for point in result.points)
    expected_fitted = tuple(point.predicted_molar / observed_total for point in result.points)
    assert captured["fitted"] == pytest.approx(expected_fitted)
    assert "measured-range denominator" in captured["ylabel"]

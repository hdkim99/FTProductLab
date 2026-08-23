from __future__ import annotations

import struct
from pathlib import Path

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

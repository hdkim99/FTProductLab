"""Deterministic scientific result export."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ftproductlab.core.asf import validate_analysis_result
from ftproductlab.core.models import AnalysisResult


def result_to_dict(result: AnalysisResult) -> dict[str, Any]:
    """Convert an immutable result to a JSON-compatible dictionary."""

    validate_analysis_result(result)
    data = asdict(result)
    data["basis"] = result.basis.value
    data["fit_config"]["weighting"] = result.fit_config.weighting.value
    data["fit"]["weighting"] = result.fit.weighting.value
    for item, ratio in zip(data["op_ratios"], result.op_ratios, strict=True):
        item["status"] = ratio.status.value
    return data


def write_analysis_bundle(result: AnalysisResult, output_directory: str | Path) -> Path:
    """Write JSON plus point, cut, and O/P CSV tables; return the output path."""

    destination = Path(output_directory)
    destination.mkdir(parents=True, exist_ok=True)
    payload = result_to_dict(result)
    (destination / "analysis.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with (destination / "points.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "carbon_number",
            "observed_molar",
            "observed_molar_fraction",
            "observed_carbon_fraction",
            "predicted_molar",
            "predicted_range_fraction",
            "log_residual",
            "relative_deviation",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for point in result.points:
            writer.writerow(asdict(point))

    with (destination / "cuts.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "label",
            "minimum_carbon",
            "maximum_carbon",
            "molar_fraction",
            "carbon_fraction",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for cut in result.cuts:
            writer.writerow(asdict(cut))

    with (destination / "op_ratios.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "carbon_number",
            "ratio",
            "olefin_molar",
            "paraffin_molar",
            "status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for ratio in result.op_ratios:
            row = asdict(ratio)
            row["status"] = ratio.status.value
            writer.writerow(row)
    return destination

"""Application service shared by CLI and GUI."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ftproductlab.core import (
    AnalysisResult,
    CutDefinition,
    FitConfig,
    InputBasis,
    Weighting,
    analyze_distribution,
)
from ftproductlab.io import read_product_csv, write_analysis_bundle

DEFAULT_CUTS = (
    CutDefinition("C1", 1, 1),
    CutDefinition("C2-C4", 2, 4),
    CutDefinition("C5+", 5, None),
    CutDefinition("C5-C12", 5, 12),
    CutDefinition("C13-C20", 13, 20),
    CutDefinition("C21+", 21, None),
)


def parse_cut_specs(specifications: Sequence[str]) -> tuple[CutDefinition, ...]:
    """Parse repeatable ``LABEL:MIN[:MAX]`` cut specifications.

    An omitted or empty maximum denotes an open-ended cut. Parsing lives in the
    application layer so CLI and GUI use the same convention.
    """

    cuts: list[CutDefinition] = []
    for specification in specifications:
        parts = specification.strip().split(":")
        if len(parts) not in {2, 3} or not parts[0].strip() or not parts[1].strip():
            raise ValueError(
                f"invalid cut {specification!r}; expected LABEL:MIN[:MAX], for example C5+:5"
            )
        maximum = None if len(parts) == 2 or not parts[2].strip() else int(parts[2])
        cuts.append(CutDefinition(parts[0].strip(), int(parts[1]), maximum))
    if not cuts:
        raise ValueError("at least one product cut is required")
    return tuple(cuts)


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    """Fully explicit user request independent from presentation framework."""

    input_path: Path
    basis: InputBasis
    fit_minimum: int
    fit_maximum: int
    weighting: Weighting = Weighting.UNIFORM
    include_below_detection: bool = False
    cuts: tuple[CutDefinition, ...] = field(default_factory=lambda: DEFAULT_CUTS)


def analyze_file(request: AnalysisRequest) -> AnalysisResult:
    """Read and analyze one CSV through the public scientific core."""

    records = read_product_csv(request.input_path, request.basis)
    return analyze_distribution(
        records,
        request.basis,
        FitConfig(
            minimum_carbon=request.fit_minimum,
            maximum_carbon=request.fit_maximum,
            weighting=request.weighting,
            include_below_detection=request.include_below_detection,
        ),
        request.cuts,
    )


def analyze_and_export(request: AnalysisRequest, output_directory: Path) -> AnalysisResult:
    """Run the same workflow used by both user interfaces and export all tables."""

    result = analyze_file(request)
    write_analysis_bundle(result, output_directory)
    return result


def fitted_observed_total_fractions(result: AnalysisResult) -> tuple[float, ...]:
    """Scale fitted amounts by the denominator used for observed molar fractions."""

    observed_total = sum(point.observed_molar for point in result.points)
    if observed_total <= 0:  # protected by scientific-core validation
        raise ValueError("positive observed molar-equivalent total is required")
    return tuple(point.predicted_molar / observed_total for point in result.points)

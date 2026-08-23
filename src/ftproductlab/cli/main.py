"""Headless command-line interface; importing it never initializes a GUI backend."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from ftproductlab import __version__
from ftproductlab.application import AnalysisRequest, analyze_and_export
from ftproductlab.core import InputBasis, ProductRecord, Weighting, analyze_distribution
from ftproductlab.core.models import FitConfig
from ftproductlab.io import result_to_dict


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ftproductlab",
        description="Reproducible Fischer-Tropsch product-distribution and ASF analysis.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze a carbon-number CSV file")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("--basis", choices=[item.value for item in InputBasis], required=True)
    analyze.add_argument("--fit-min", type=int, required=True)
    analyze.add_argument("--fit-max", type=int, required=True)
    analyze.add_argument(
        "--weighting", choices=[item.value for item in Weighting], default="uniform"
    )
    analyze.add_argument("--include-below-detection", action="store_true")
    analyze.add_argument("--output", type=Path, required=True)
    analyze.add_argument(
        "--plots", action="store_true", help="Export PNG, SVG, and PDF scientific figures"
    )

    subparsers.add_parser("validate", help="Run a deterministic alpha=0.8 core benchmark")
    return parser


def _run_validation() -> int:
    alpha = 0.8
    records = tuple(
        ProductRecord(carbon_number=n, amount=(1 - alpha) * alpha ** (n - 1)) for n in range(1, 21)
    )
    result = analyze_distribution(records, InputBasis.MOLAR, FitConfig(3, 20))
    error = abs(result.fit.alpha - alpha)
    print(json.dumps({"alpha_expected": alpha, "alpha_observed": result.fit.alpha, "error": error}))
    return 0 if error < 1e-12 else 1


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""

    arguments = _parser().parse_args(argv)
    if arguments.command == "validate":
        return _run_validation()
    request = AnalysisRequest(
        input_path=arguments.input,
        basis=InputBasis(arguments.basis),
        fit_minimum=arguments.fit_min,
        fit_maximum=arguments.fit_max,
        weighting=Weighting(arguments.weighting),
        include_below_detection=arguments.include_below_detection,
    )
    try:
        result = analyze_and_export(request, arguments.output)
        if arguments.plots:
            from ftproductlab.plotting import export_publication_figures

            export_publication_figures(result, arguments.output)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result_to_dict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

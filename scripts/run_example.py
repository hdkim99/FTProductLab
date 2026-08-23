"""Repository example workflow used by CI."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ftproductlab.application import AnalysisRequest, analyze_and_export
from ftproductlab.core import InputBasis


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = analyze_and_export(
        AnalysisRequest(Path("examples/sample_distribution.csv"), InputBasis.MOLAR, 5, 20),
        args.output,
    )
    print(f"alpha={result.fit.alpha:.6f}; output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

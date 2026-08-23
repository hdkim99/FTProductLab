"""Publication figure export with an explicit non-interactive backend."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ftproductlab.application import fitted_observed_total_fractions
from ftproductlab.core.models import AnalysisResult, InputBasis, RatioStatus


def _pyplot() -> Any:
    try:
        import matplotlib

        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt
    except ImportError as error:  # pragma: no cover - exercised in clean-core CI
        raise RuntimeError(
            'Plot dependencies are not installed. Install with: pip install "ftproductlab[plot]"'
        ) from error
    return plt


def _distribution_ylabel(basis: InputBasis) -> str:
    if basis is InputBasis.MOLAR:
        prefix = "Molar fraction"
    elif basis is InputBasis.MASS:
        prefix = "Molar-equivalent fraction (from mass input)"
    else:
        prefix = "Molar-equivalent fraction (from carbon input)"
    return f"{prefix}; measured-range denominator"


def export_publication_figures(
    result: AnalysisResult,
    output_directory: str | Path,
    formats: tuple[str, ...] = ("png", "svg", "pdf"),
) -> tuple[Path, ...]:
    """Export ASF, residual, O/P, and product-cut figures from an analysis result."""

    plt = _pyplot()
    destination = Path(output_directory)
    destination.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    carbons = [point.carbon_number for point in result.points]
    observed = [point.observed_molar_fraction for point in result.points]
    fitted = fitted_observed_total_fractions(result)
    figure, axis = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
    axis.semilogy(carbons, observed, "o", label="Observed (measured-range normalized)")
    axis.semilogy(
        carbons,
        fitted,
        "-",
        label=f"Single-alpha fit (same denominator; alpha={result.fit.alpha:.4f})",
    )
    axis.axvspan(
        result.fit_config.minimum_carbon,
        result.fit_config.maximum_carbon,
        color="#1f77b4",
        alpha=0.08,
        label="User fit range",
    )
    axis.set(
        xlabel="Carbon number",
        ylabel=_distribution_ylabel(result.basis),
        title="FT product distribution",
    )
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    created.extend(_save(figure, destination, "asf_fit", formats))
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    residuals = [
        point.log_residual if point.log_residual is not None else float("nan")
        for point in result.points
    ]
    axis.axhline(0, color="black", linewidth=0.8)
    axis.bar(carbons, residuals, color="#d95f02")
    axis.set(
        xlabel="Carbon number",
        ylabel="ln(observed / fitted)",
        title="Single-alpha ASF residuals",
    )
    axis.grid(axis="y", alpha=0.2)
    created.extend(_save(figure, destination, "asf_residuals", formats))
    plt.close(figure)

    valid_ratios = [ratio for ratio in result.op_ratios if ratio.status is RatioStatus.OK]
    if valid_ratios:
        figure, axis = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
        axis.plot(
            [ratio.carbon_number for ratio in valid_ratios],
            [ratio.ratio for ratio in valid_ratios],
            "o-",
            color="#1b9e77",
        )
        axis.set(xlabel="Carbon number", ylabel="O/P molar ratio", title="Olefin/paraffin ratio")
        axis.grid(alpha=0.2)
        created.extend(_save(figure, destination, "op_ratio", formats))
        plt.close(figure)

    if result.cuts:
        figure, axis = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
        axis.bar(
            [cut.label for cut in result.cuts],
            [cut.carbon_fraction for cut in result.cuts],
            color="#7570b3",
        )
        axis.set(
            xlabel="Explicit carbon-number cut",
            ylabel="Observed carbon fraction",
            title="Product-cut distribution",
        )
        axis.tick_params(axis="x", rotation=25)
        axis.grid(axis="y", alpha=0.2)
        created.extend(_save(figure, destination, "product_cuts", formats))
        plt.close(figure)
    return tuple(created)


def export_social_preview(result: AnalysisResult, destination: str | Path) -> Path:
    """Create a 1280x640 preview using the supplied real analysis result."""

    plt = _pyplot()
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    figure, (distribution_axis, residual_axis) = plt.subplots(
        1, 2, figsize=(12.8, 6.4), dpi=100, constrained_layout=True
    )
    figure.patch.set_facecolor("#f7f7f4")
    carbons = [point.carbon_number for point in result.points]
    distribution_axis.semilogy(
        carbons,
        [point.observed_molar_fraction for point in result.points],
        "o",
        color="#005a70",
        label="Observed",
    )
    distribution_axis.semilogy(
        carbons,
        fitted_observed_total_fractions(result),
        "-",
        color="#e36a25",
        linewidth=2.2,
        label=f"ASF fit  alpha={result.fit.alpha:.3f}",
    )
    distribution_axis.set_title("FT product distribution", loc="left", weight="bold")
    distribution_axis.set_xlabel("Carbon number")
    distribution_axis.set_ylabel(_distribution_ylabel(result.basis))
    distribution_axis.legend(frameon=False)
    distribution_axis.grid(alpha=0.2)
    residual_axis.axhline(0, color="black", linewidth=0.8)
    residual_axis.bar(
        carbons,
        [point.log_residual if point.log_residual is not None else 0.0 for point in result.points],
        color="#7b5aa6",
    )
    residual_axis.set_title("Deviation made visible", loc="left", weight="bold")
    residual_axis.set_xlabel("Carbon number")
    residual_axis.set_ylabel("ln(observed / fitted)")
    residual_axis.grid(axis="y", alpha=0.2)
    figure.suptitle(
        "FTProductLab  |  explicit ASF fitting and product-distribution diagnostics",
        fontsize=16,
        weight="bold",
    )
    figure.savefig(target, dpi=100, facecolor=figure.get_facecolor())
    plt.close(figure)
    return target


def _save(figure: Any, directory: Path, stem: str, formats: tuple[str, ...]) -> list[Path]:
    allowed = {"png", "svg", "pdf"}
    invalid = set(formats) - allowed
    if invalid:
        raise ValueError(f"unsupported plot formats: {', '.join(sorted(invalid))}")
    paths: list[Path] = []
    for extension in formats:
        path = directory / f"{stem}.{extension}"
        figure.savefig(path, dpi=300 if extension == "png" else None)
        paths.append(path)
    return paths

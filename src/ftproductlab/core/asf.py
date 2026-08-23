"""Anderson--Schulz--Flory aggregation, fitting, and diagnostics."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Sequence
from math import exp, isfinite, log

from .models import (
    AggregatedPoint,
    AnalysisResult,
    AsfFit,
    CutDefinition,
    CutResult,
    FitConfig,
    InputBasis,
    OpRatio,
    PointAnalysis,
    ProductCategory,
    ProductRecord,
    RatioStatus,
    Weighting,
)


def ideal_molar_fraction(carbon_number: int, alpha: float) -> float:
    """Return ideal infinite-distribution molecular fraction ``(1-a)*a**(n-1)``."""

    if carbon_number < 1:
        raise ValueError("carbon_number must be at least 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    return (1.0 - alpha) * alpha ** (carbon_number - 1)


def ideal_carbon_fraction(carbon_number: int, alpha: float) -> float:
    """Return ideal infinite-distribution carbon fraction ``n(1-a)^2 a^(n-1)``."""

    return carbon_number * (1.0 - alpha) * ideal_molar_fraction(carbon_number, alpha)


def ideal_carbon_cut_fraction(
    minimum_carbon: int, alpha: float, maximum_carbon: int | None = None
) -> float:
    """Analytical ideal ASF carbon fraction for an inclusive cut.

    The value refers to the untruncated infinite ASF distribution, unlike observed
    cut fractions which close only over supplied measurements.
    """

    if minimum_carbon < 1:
        raise ValueError("minimum_carbon must be at least 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    if maximum_carbon is not None and maximum_carbon < minimum_carbon:
        raise ValueError("maximum_carbon must not be below minimum_carbon")

    def tail(start: int) -> float:
        return alpha ** (start - 1) * (start - (start - 1) * alpha)

    value = tail(minimum_carbon)
    if maximum_carbon is not None:
        value -= tail(maximum_carbon + 1)
    return value


def _molar_equivalent(record: ProductRecord, basis: InputBasis) -> float:
    if basis is InputBasis.MOLAR:
        return record.amount
    if basis is InputBasis.CARBON:
        return record.amount / record.carbon_number
    if record.molecular_weight_g_mol is None:
        species = record.species or f"C{record.carbon_number} record"
        raise ValueError(f"mass-basis input requires molecular_weight_g_mol for {species}")
    return record.amount / record.molecular_weight_g_mol


def aggregate_records(
    records: Iterable[ProductRecord], basis: InputBasis
) -> tuple[AggregatedPoint, ...]:
    """Aggregate species by carbon number without discarding category identity."""

    input_amount: dict[int, float] = defaultdict(float)
    molar: dict[int, float] = defaultdict(float)
    categories: dict[int, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    below_detection: dict[int, bool] = defaultdict(bool)
    count = 0
    for record in records:
        count += 1
        equivalent = _molar_equivalent(record, basis)
        input_amount[record.carbon_number] += record.amount
        molar[record.carbon_number] += equivalent
        categories[record.carbon_number][record.category.strip().lower()] += equivalent
        below_detection[record.carbon_number] |= record.below_detection
    if count == 0:
        raise ValueError("at least one product record is required")
    return tuple(
        AggregatedPoint(
            carbon_number=carbon_number,
            input_amount=input_amount[carbon_number],
            molar_equivalent=molar[carbon_number],
            category_molar=dict(sorted(categories[carbon_number].items())),
            contains_below_detection=below_detection[carbon_number],
        )
        for carbon_number in sorted(molar)
    )


def fit_single_alpha(points: Sequence[AggregatedPoint], config: FitConfig) -> AsfFit:
    """Fit ``ln(molar-equivalent amount) = intercept + n ln(alpha)``.

    Zeros and, by default, points marked below detection are excluded. The fit
    range is never selected automatically.
    """

    selected = [
        point
        for point in points
        if config.minimum_carbon <= point.carbon_number <= config.maximum_carbon
        and point.molar_equivalent > 0
        and (config.include_below_detection or not point.contains_below_detection)
    ]
    if len(selected) < 2:
        raise ValueError("ASF fitting requires at least two positive, eligible points")
    x = [float(point.carbon_number) for point in selected]
    y = [log(point.molar_equivalent) for point in selected]
    if config.weighting is Weighting.UNIFORM:
        weights = [1.0] * len(selected)
    else:
        scale = max(point.molar_equivalent for point in selected)
        weights = [point.molar_equivalent / scale for point in selected]
    weight_sum = sum(weights)
    x_bar = sum(weight * value for weight, value in zip(weights, x, strict=True)) / weight_sum
    y_bar = sum(weight * value for weight, value in zip(weights, y, strict=True)) / weight_sum
    denominator = sum(
        weight * (x_value - x_bar) ** 2 for weight, x_value in zip(weights, x, strict=True)
    )
    if denominator <= 0:
        raise ValueError("fit carbon numbers must contain at least two distinct values")
    slope = (
        sum(
            weight * (x_value - x_bar) * (y_value - y_bar)
            for weight, x_value, y_value in zip(weights, x, y, strict=True)
        )
        / denominator
    )
    alpha = exp(slope)
    if not 0 < alpha < 1:
        raise ValueError(
            "fitted slope does not imply a physical single-alpha ASF probability (0 < alpha < 1)"
        )
    intercept = y_bar - slope * x_bar
    residual_sum = sum(
        weight * (y_value - (intercept + slope * x_value)) ** 2
        for weight, x_value, y_value in zip(weights, x, y, strict=True)
    )
    total_sum = sum(
        weight * (y_value - y_bar) ** 2 for weight, y_value in zip(weights, y, strict=True)
    )
    r_squared = 1.0 if total_sum == 0 and residual_sum == 0 else 1.0 - residual_sum / total_sum
    return AsfFit(
        alpha=alpha,
        slope=slope,
        intercept=intercept,
        r_squared=r_squared,
        fit_carbons=tuple(point.carbon_number for point in selected),
        weighting=config.weighting,
    )


def calculate_cuts(
    points: Sequence[AggregatedPoint], cuts: Sequence[CutDefinition]
) -> tuple[CutResult, ...]:
    """Calculate cut fractions closed over the supplied measured dataset."""

    total_molar = sum(point.molar_equivalent for point in points)
    total_carbon = sum(point.carbon_number * point.molar_equivalent for point in points)
    if total_molar <= 0 or total_carbon <= 0:
        raise ValueError("positive total product amount is required")
    results: list[CutResult] = []
    for cut in cuts:
        selected = [
            point
            for point in points
            if point.carbon_number >= cut.minimum_carbon
            and (cut.maximum_carbon is None or point.carbon_number <= cut.maximum_carbon)
        ]
        results.append(
            CutResult(
                label=cut.label,
                minimum_carbon=cut.minimum_carbon,
                maximum_carbon=cut.maximum_carbon,
                molar_fraction=sum(point.molar_equivalent for point in selected) / total_molar,
                carbon_fraction=sum(
                    point.carbon_number * point.molar_equivalent for point in selected
                )
                / total_carbon,
            )
        )
    return tuple(results)


def calculate_op_ratios(points: Sequence[AggregatedPoint]) -> tuple[OpRatio, ...]:
    """Calculate O/P ratios while retaining zeros and detection-limit states."""

    ratios: list[OpRatio] = []
    for point in points:
        olefin = point.category_molar.get(ProductCategory.OLEFIN.value, 0.0)
        paraffin = point.category_molar.get(ProductCategory.PARAFFIN.value, 0.0)
        if point.contains_below_detection and (olefin > 0 or paraffin > 0):
            status = RatioStatus.BELOW_DETECTION
            ratio = None
        elif paraffin == 0 and olefin == 0:
            status = RatioStatus.NO_SIGNAL
            ratio = None
        elif paraffin == 0:
            status = RatioStatus.ZERO_DENOMINATOR
            ratio = None
        else:
            status = RatioStatus.OK
            ratio = olefin / paraffin
        ratios.append(
            OpRatio(
                carbon_number=point.carbon_number,
                ratio=ratio,
                olefin_molar=olefin,
                paraffin_molar=paraffin,
                status=status,
            )
        )
    return tuple(ratios)


def analyze_distribution(
    records: Iterable[ProductRecord],
    basis: InputBasis,
    fit_config: FitConfig,
    cuts: Sequence[CutDefinition] = (),
) -> AnalysisResult:
    """Run aggregation, explicit-range ASF fit, deviations, cuts, and O/P analysis."""

    aggregated = aggregate_records(records, basis)
    fit = fit_single_alpha(aggregated, fit_config)
    total_molar = sum(point.molar_equivalent for point in aggregated)
    total_carbon = sum(point.carbon_number * point.molar_equivalent for point in aggregated)
    predictions = [exp(fit.intercept + fit.slope * point.carbon_number) for point in aggregated]
    prediction_total = sum(predictions)
    point_results: list[PointAnalysis] = []
    deviations: dict[int, float] = {}
    for point, predicted in zip(aggregated, predictions, strict=True):
        relative = (point.molar_equivalent - predicted) / predicted
        deviations[point.carbon_number] = relative
        log_residual = (
            log(point.molar_equivalent) - log(predicted) if point.molar_equivalent > 0 else None
        )
        point_results.append(
            PointAnalysis(
                carbon_number=point.carbon_number,
                observed_molar=point.molar_equivalent,
                observed_molar_fraction=point.molar_equivalent / total_molar,
                observed_carbon_fraction=(
                    point.carbon_number * point.molar_equivalent / total_carbon
                ),
                predicted_molar=predicted,
                predicted_range_fraction=predicted / prediction_total,
                log_residual=log_residual,
                relative_deviation=relative,
            )
        )
    warnings: list[str] = []
    if fit.r_squared < 0.95:
        warnings.append(
            "The single-alpha transformed fit shows substantial deviation; R-squared is a "
            "descriptive statistic, not proof of model validity."
        )
    if any(point.contains_below_detection for point in aggregated):
        warnings.append(
            "Below-detection records are retained for reporting and excluded from fitting "
            "by default."
        )
    assumptions = (
        "A single, carbon-number-independent chain-growth probability is fitted over the "
        "user range.",
        "Regression uses natural log of molar-equivalent amount with a free intercept.",
        "Observed cut fractions close over supplied measurements, not an unmeasured infinite tail.",
        "Mass inputs are converted species-by-species using supplied molecular weights.",
    )
    return AnalysisResult(
        basis=basis,
        fit_config=fit_config,
        fit=fit,
        points=tuple(point_results),
        cuts=calculate_cuts(aggregated, cuts),
        op_ratios=calculate_op_ratios(aggregated),
        c1_relative_deviation=deviations.get(1),
        c2_relative_deviation=deviations.get(2),
        assumptions=assumptions,
        warnings=tuple(warnings),
    )


def validate_analysis_result(result: AnalysisResult) -> None:
    """Defensive finite-number check used before serialization and plotting."""

    numeric_values = [
        result.fit.alpha,
        result.fit.slope,
        result.fit.intercept,
        result.fit.r_squared,
    ]
    for point in result.points:
        numeric_values.extend(
            [
                point.observed_molar,
                point.observed_molar_fraction,
                point.observed_carbon_fraction,
                point.predicted_molar,
                point.predicted_range_fraction,
                point.relative_deviation,
            ]
        )
        if point.log_residual is not None:
            numeric_values.append(point.log_residual)
    if not all(isfinite(value) for value in numeric_values):
        raise ValueError("analysis produced a non-finite numeric result")

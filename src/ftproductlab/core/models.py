"""Scientific data models for Fischer--Tropsch product distributions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite


class InputBasis(str, Enum):
    """Basis used by the input ``amount`` column."""

    MOLAR = "molar"
    MASS = "mass"
    CARBON = "carbon"


class Weighting(str, Enum):
    """Weights used for the linear ASF fit in logarithmic coordinates."""

    UNIFORM = "uniform"
    AMOUNT = "amount"


class ProductCategory(str, Enum):
    """Recommended product categories; arbitrary category strings remain accepted."""

    PARAFFIN = "paraffin"
    OLEFIN = "olefin"
    OXYGENATE = "oxygenate"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class ProductRecord:
    """One measured species or already aggregated carbon-number contribution.

    Amounts may use any consistent scale. Mass-basis records require molecular
    weight so that unlike product classes are not converted with a hydrocarbon
    approximation.
    """

    carbon_number: int
    amount: float
    category: str = ProductCategory.OTHER.value
    species: str = ""
    molecular_weight_g_mol: float | None = None
    below_detection: bool = False

    def __post_init__(self) -> None:
        if self.carbon_number < 1:
            raise ValueError("carbon_number must be a positive integer")
        if not isfinite(self.amount) or self.amount < 0:
            raise ValueError("amount must be finite and non-negative")
        if self.molecular_weight_g_mol is not None and (
            not isfinite(self.molecular_weight_g_mol) or self.molecular_weight_g_mol <= 0
        ):
            raise ValueError("molecular_weight_g_mol must be finite and positive")


@dataclass(frozen=True, slots=True)
class AggregatedPoint:
    """Carbon-number total retaining category-resolved molar equivalents."""

    carbon_number: int
    input_amount: float
    molar_equivalent: float
    category_molar: dict[str, float]
    contains_below_detection: bool = False


@dataclass(frozen=True, slots=True)
class FitConfig:
    """Explicit ASF fit range and regression weighting convention."""

    minimum_carbon: int
    maximum_carbon: int
    weighting: Weighting = Weighting.UNIFORM
    include_below_detection: bool = False

    def __post_init__(self) -> None:
        if self.minimum_carbon < 1:
            raise ValueError("minimum_carbon must be at least 1")
        if self.maximum_carbon < self.minimum_carbon:
            raise ValueError("maximum_carbon must not be below minimum_carbon")


@dataclass(frozen=True, slots=True)
class AsfFit:
    """Single-alpha ASF regression result.

    No confidence interval is reported: the residuals are usually structured and
    ordinary least-squares statistical assumptions should not be silently imposed.
    """

    alpha: float
    slope: float
    intercept: float
    r_squared: float
    fit_carbons: tuple[int, ...]
    weighting: Weighting
    transformed_coordinate: str = "ln(molar-equivalent amount)"


@dataclass(frozen=True, slots=True)
class PointAnalysis:
    """Observed and fitted values for one carbon number."""

    carbon_number: int
    observed_molar: float
    observed_molar_fraction: float
    observed_carbon_fraction: float
    predicted_molar: float
    predicted_range_fraction: float
    log_residual: float | None
    relative_deviation: float


@dataclass(frozen=True, slots=True)
class CutDefinition:
    """Inclusive, user-defined carbon-number product cut."""

    label: str
    minimum_carbon: int
    maximum_carbon: int | None = None

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("cut label must not be empty")
        if self.minimum_carbon < 1:
            raise ValueError("cut minimum_carbon must be at least 1")
        if self.maximum_carbon is not None and self.maximum_carbon < self.minimum_carbon:
            raise ValueError("cut maximum_carbon must not be below minimum_carbon")


@dataclass(frozen=True, slots=True)
class CutResult:
    """Observed molar and carbon fractions within the measured dataset."""

    label: str
    minimum_carbon: int
    maximum_carbon: int | None
    molar_fraction: float
    carbon_fraction: float


class RatioStatus(str, Enum):
    """State of an olefin/paraffin ratio."""

    OK = "ok"
    ZERO_DENOMINATOR = "zero-denominator"
    NO_SIGNAL = "no-signal"
    BELOW_DETECTION = "below-detection"


@dataclass(frozen=True, slots=True)
class OpRatio:
    """Olefin/paraffin ratio with an explicit non-numeric state."""

    carbon_number: int
    ratio: float | None
    olefin_molar: float
    paraffin_molar: float
    status: RatioStatus


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Complete analysis returned identically to API, CLI, and GUI adapters."""

    basis: InputBasis
    fit_config: FitConfig
    fit: AsfFit
    points: tuple[PointAnalysis, ...]
    cuts: tuple[CutResult, ...]
    op_ratios: tuple[OpRatio, ...]
    c1_relative_deviation: float | None
    c2_relative_deviation: float | None
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

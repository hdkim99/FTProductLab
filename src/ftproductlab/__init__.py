"""FTProductLab public Python API without GUI or plotting side effects."""

from .core import (
    AnalysisResult,
    CutDefinition,
    FitConfig,
    InputBasis,
    ProductCategory,
    ProductRecord,
    Weighting,
    analyze_distribution,
    ideal_carbon_cut_fraction,
    ideal_carbon_fraction,
    ideal_molar_fraction,
)

__version__ = "0.1.1"

__all__ = [
    "AnalysisResult",
    "CutDefinition",
    "FitConfig",
    "InputBasis",
    "ProductCategory",
    "ProductRecord",
    "Weighting",
    "__version__",
    "analyze_distribution",
    "ideal_carbon_cut_fraction",
    "ideal_carbon_fraction",
    "ideal_molar_fraction",
]

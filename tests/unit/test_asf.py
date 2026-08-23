from __future__ import annotations

from math import isclose

import pytest

from ftproductlab.core import (
    CutDefinition,
    FitConfig,
    InputBasis,
    ProductRecord,
    analyze_distribution,
    ideal_carbon_cut_fraction,
    ideal_carbon_fraction,
    ideal_molar_fraction,
)


def test_ideal_distributions_close() -> None:
    alpha = 0.8
    assert isclose(sum(ideal_molar_fraction(n, alpha) for n in range(1, 500)), 1.0)
    assert isclose(sum(ideal_carbon_fraction(n, alpha) for n in range(1, 500)), 1.0)


def test_analytic_carbon_cut_matches_direct_sum() -> None:
    alpha = 0.85
    expected = sum(ideal_carbon_fraction(n, alpha) for n in range(5, 13))
    assert ideal_carbon_cut_fraction(5, alpha, 12) == pytest.approx(expected)
    assert ideal_carbon_cut_fraction(5, alpha) == pytest.approx(
        sum(ideal_carbon_fraction(n, alpha) for n in range(5, 1000))
    )


def test_exact_single_alpha_and_cut_mass_balance() -> None:
    alpha = 0.82
    records = [
        ProductRecord(n, ideal_molar_fraction(n, alpha), category="paraffin") for n in range(1, 31)
    ]
    result = analyze_distribution(
        records,
        InputBasis.MOLAR,
        FitConfig(3, 20),
        (CutDefinition("C1", 1, 1), CutDefinition("C2-C4", 2, 4), CutDefinition("C5+", 5)),
    )
    assert result.fit.alpha == pytest.approx(alpha, abs=1e-14)
    assert result.fit.r_squared == pytest.approx(1.0)
    assert sum(cut.molar_fraction for cut in result.cuts) == pytest.approx(1.0)
    assert sum(cut.carbon_fraction for cut in result.cuts) == pytest.approx(1.0)


def test_nonphysical_increasing_distribution_fails() -> None:
    records = [ProductRecord(n, float(n)) for n in range(1, 5)]
    with pytest.raises(ValueError, match="physical"):
        analyze_distribution(records, InputBasis.MOLAR, FitConfig(1, 4))


def test_c1_c2_deviations_are_reported_but_fit_range_is_unchanged() -> None:
    alpha = 0.75
    records = [ProductRecord(n, ideal_molar_fraction(n, alpha)) for n in range(1, 11)]
    records[0] = ProductRecord(1, records[0].amount * 2)
    records[1] = ProductRecord(2, records[1].amount * 0.5)
    result = analyze_distribution(records, InputBasis.MOLAR, FitConfig(3, 10))
    assert result.fit.fit_carbons == tuple(range(3, 11))
    assert result.c1_relative_deviation is not None
    assert result.c1_relative_deviation > 0
    assert result.c2_relative_deviation is not None
    assert result.c2_relative_deviation < 0


@pytest.mark.parametrize("alpha", [0.0, 1.0, -0.1, 1.1])
def test_invalid_alpha(alpha: float) -> None:
    with pytest.raises(ValueError):
        ideal_molar_fraction(1, alpha)

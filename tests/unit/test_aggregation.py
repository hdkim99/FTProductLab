from __future__ import annotations

import pytest

from ftproductlab.core.asf import aggregate_records, calculate_op_ratios
from ftproductlab.core.models import InputBasis, ProductRecord, RatioStatus


def test_species_aggregation_preserves_categories() -> None:
    points = aggregate_records(
        [
            ProductRecord(3, 2.0, "paraffin", "propane"),
            ProductRecord(3, 1.0, "olefin", "propene"),
            ProductRecord(4, 0.5, "oxygenate", "butanol"),
        ],
        InputBasis.MOLAR,
    )
    assert points[0].molar_equivalent == 3.0
    assert points[0].category_molar == {"olefin": 1.0, "paraffin": 2.0}
    assert calculate_op_ratios(points)[0].ratio == 0.5


def test_mass_basis_uses_species_molecular_weight() -> None:
    points = aggregate_records(
        [
            ProductRecord(3, 44.0, "paraffin", "propane", 44.0),
            ProductRecord(3, 42.0, "olefin", "propene", 42.0),
        ],
        InputBasis.MASS,
    )
    assert points[0].molar_equivalent == pytest.approx(2.0)


def test_mass_basis_never_guesses_molecular_weight() -> None:
    with pytest.raises(ValueError, match="molecular_weight"):
        aggregate_records([ProductRecord(5, 1.0)], InputBasis.MASS)


def test_ratio_zero_and_detection_states() -> None:
    points = aggregate_records(
        [
            ProductRecord(2, 1.0, "olefin"),
            ProductRecord(3, 0.0, "olefin"),
            ProductRecord(3, 0.0, "paraffin"),
            ProductRecord(4, 1.0, "paraffin", below_detection=True),
        ],
        InputBasis.MOLAR,
    )
    ratios = calculate_op_ratios(points)
    assert [ratio.status for ratio in ratios] == [
        RatioStatus.ZERO_DENOMINATOR,
        RatioStatus.NO_SIGNAL,
        RatioStatus.BELOW_DETECTION,
    ]

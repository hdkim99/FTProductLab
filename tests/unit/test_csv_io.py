from __future__ import annotations

from pathlib import Path

import pytest

from ftproductlab.core import InputBasis
from ftproductlab.io import read_product_csv


def test_read_example() -> None:
    records = read_product_csv(Path("examples/sample_distribution.csv"), InputBasis.MOLAR)
    assert len(records) == 31
    assert records[0].species == "methane"


def test_mass_basis_requires_molecular_weight(tmp_path: Path) -> None:
    source = tmp_path / "mass.csv"
    source.write_text("carbon_number,amount\n3,1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="molecular_weight"):
        read_product_csv(source, InputBasis.MASS)


def test_unknown_column_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "bad.csv"
    source.write_text("carbon_number,amount,secret_guess\n3,1.0,yes\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported"):
        read_product_csv(source, InputBasis.MOLAR)

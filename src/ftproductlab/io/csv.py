"""Strict CSV input for FT product measurements."""

from __future__ import annotations

import csv
from pathlib import Path

from ftproductlab.core.models import InputBasis, ProductRecord

REQUIRED_COLUMNS = frozenset({"carbon_number", "amount"})
OPTIONAL_COLUMNS = frozenset({"category", "species", "molecular_weight_g_mol", "below_detection"})


def _required_text(row: dict[str, str | None], name: str, line: int) -> str:
    value = row.get(name)
    if value is None or not value.strip():
        raise ValueError(f"line {line}: {name} is required")
    return value.strip()


def _parse_bool(value: str | None, line: int) -> bool:
    if value is None or not value.strip():
        return False
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"line {line}: below_detection must be true/false")


def read_product_csv(path: str | Path, basis: InputBasis) -> tuple[ProductRecord, ...]:
    """Read documented CSV fields and validate basis-specific requirements."""

    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV must include a header row")
        fields = {field.strip() for field in reader.fieldnames}
        missing = REQUIRED_COLUMNS - fields
        unknown = fields - REQUIRED_COLUMNS - OPTIONAL_COLUMNS
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        if unknown:
            raise ValueError(f"CSV contains unsupported columns: {', '.join(sorted(unknown))}")
        records: list[ProductRecord] = []
        for line, row in enumerate(reader, start=2):
            if not any(value and value.strip() for value in row.values()):
                continue
            carbon_number = int(_required_text(row, "carbon_number", line))
            amount = float(_required_text(row, "amount", line))
            molecular_text = (row.get("molecular_weight_g_mol") or "").strip()
            molecular_weight = float(molecular_text) if molecular_text else None
            if basis is InputBasis.MASS and molecular_weight is None:
                raise ValueError(
                    f"line {line}: molecular_weight_g_mol is required for mass-basis input"
                )
            records.append(
                ProductRecord(
                    carbon_number=carbon_number,
                    amount=amount,
                    category=(row.get("category") or "other").strip().lower() or "other",
                    species=(row.get("species") or "").strip(),
                    molecular_weight_g_mol=molecular_weight,
                    below_detection=_parse_bool(row.get("below_detection"), line),
                )
            )
    if not records:
        raise ValueError("CSV contains no product records")
    return tuple(records)

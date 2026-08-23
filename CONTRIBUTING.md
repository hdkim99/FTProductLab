# Contributing

Use a focused issue or pull request and do not upload unpublished, confidential, export-
controlled, or personally identifiable research data to a public issue.

Scientific-core changes must state the equation or definition, units/basis, assumptions,
validity range, authoritative reference, independent numerical validation, and regression
test. A higher R² alone does not justify a new model. Do not add coefficients or thresholds
without a traceable source or derivation.

GUI changes must additionally record supported platforms, dependency changes, backend
impact, macOS smoke results, and CLI/core import isolation. PyQt and PySide must never be
mixed; introducing Qt requires a separate architecture decision and the compatibility tests
listed in the issue template. Tk code must create one root and must not update widgets from a
background thread.

Run before submitting:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

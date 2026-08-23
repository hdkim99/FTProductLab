# Changelog

## 0.1.1 - 2026-08-23

- Correct observed-versus-fitted figure normalization after a public Ru/TiO2 workbook
  exposed that 0.1.0 used different denominators for the two plotted series.
- Show the same comparable fitted fraction in the GUI result table. Numeric alpha,
  residuals, raw fitted amounts, and scientific-core equations were not affected.
- Add attributed public-data validation for Ru/TiO2, industrial Fe/Mn, and Co/TiO2 cases,
  including source checksums and discrepancy classification.

## 0.1.0 - 2026-08-23

- Initial species-preserving carbon-number aggregation.
- Explicit molar, mass, and carbon input bases.
- User-ranged single-alpha ASF fitting with uniform or amount weighting.
- C1/C2 and per-carbon residual diagnostics, user-defined cuts, and O/P states.
- Shared Python API, CLI, Tkinter GUI, deterministic tables, and PNG/SVG/PDF figures.

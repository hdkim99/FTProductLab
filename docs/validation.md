# Validation record

## Hand and synthetic benchmarks

The exact benchmark generates `M_n = (1-alpha) alpha^(n-1)` at alpha 0.8. Regression over
C3–C20 must return 0.8 within `1e-12`; `ftproductlab validate` exposes this check without test
framework dependencies.

Independent direct sums verify molecular and carbon distributions close to one and verify
the analytical finite/tail cut formula. Other regression tests cover scale invariance,
mass-to-mole conversion, category aggregation, input validation, fit failure for a positive
slope, zero denominator, below-detection state, CSV schema, CLI/GUI agreement through the
shared service, export, plotting, and import isolation.

## Public-data validation

The 0.1.0 package was first exercised unchanged against three external cases. FTP-PUB-002
uses a raw, repository-hosted workbook; FTP-PUB-003 uses processed experimental tables in
peer-reviewed supporting information; FTP-PUB-001 is a published-number and metadata
benchmark because the combined per-carbon values needed to reproduce the reported fit are
not tabulated.

Results include:

- Cambridge Ru/TiO2 wax distributions, C30–C50 uniform fits: alpha = 0.88372625,
  0.92999148, and 0.93840928 for feed H2/CO ratios 2, 1, and 0.5. Independent ordinary
  least-squares calculations on the workbook's logged values agree to floating-point
  precision.
- Gao et al. industrial Fe/Mn Run A-2, uniform fits: alpha = 0.88235535 for C6–C20,
  0.94460763 for C31–C60, and 0.92731071 for C6–C60. The fit-range dependence and
  structured residuals are evidence against silently adding a more complex model.
- Partington et al. report alpha = 0.92 over C10–C40 and C5+ = 85.0% for a Co/TiO2
  pilot-plant product. The article supports the explicit range/C1/C2 conventions, but the
  combined C10–C40 values needed for exact reproduction are figure-only.

The Cambridge case exposed one 0.1.0 plotting defect: observations used the measured-data
total while the fitted overlay used its own predicted total. Numeric alpha, residuals, and
exports were unaffected. A CC-BY-4.0 minimal fixture now reproduces that discrepancy and
guards the corrected common-denominator overlay.

Complete provenance, checksums, scope, search record, and discrepancy classification are in
[public-data-sources.md](public-data-sources.md).

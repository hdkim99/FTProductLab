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

## Real-data status

Candidate source:

- DOI: <https://doi.org/10.1186/s40543-020-00235-5>
- Citation: Partington et al., *J. Anal. Sci. Technol.* 11, 42 (2020)
- License: Creative Commons Attribution 4.0
- Reported target: hydrocarbon alpha 0.92 over C10–C40
- Scope: full gas/aqueous/liquid/wax FT product aggregation and ASF analysis
- Files used: none redistributed
- Checksum: not applicable; no source file vendored

The article is an authoritative external behavior target and confirms why fit range and
C1/C2 handling must be explicit. Numeric real-data reproduction is currently **pending**:
the repository does not yet contain a traceable tabular extraction of the article's C10–C40
hydrocarbon distribution. The bundled sample is synthetic and labeled as such.

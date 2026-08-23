# Scientific basis and conventions

## Ideal ASF definition

With a carbon-number-independent chain-growth probability `0 < alpha < 1`, the molecular
number fraction at chain length `n` is

`x_n = (1 - alpha) alpha^(n - 1)`.

Multiplication by carbon number followed by normalization gives the carbon fraction

`w_n = n (1 - alpha)^2 alpha^(n - 1)`.

Both infinite series sum to one. The analytical carbon fraction from `C_N` upward is

`alpha^(N-1) [N - (N-1) alpha]`.

The implementation regression is equivalent to the common `ln(W_n/n)` representation when
`W_n` is a carbon/approximately molecular-weight fraction, but it first converts every input
to a molecular equivalent. It then fits

`ln(M_n) = b + n ln(alpha)`

with a free intercept `b`. This avoids claiming complete infinite-distribution closure for a
scaled or truncated experiment.

## Fit range and weighting

The caller must supply both fit limits. C1 and C2 are neither included nor excluded
automatically. Uniform weighting gives every eligible transformed carbon number equal
weight. Amount weighting uses measured molar-equivalent amount as the linear regression
weight. This is a declared numerical convention, not an uncertainty model.

No confidence interval is emitted because analytical errors, phase recovery, missing carbon
numbers, and detector response generally violate an unqualified independent Gaussian error
model. R² is reported only as a descriptive transformed-coordinate statistic.

## Input basis

- Molar basis enters the regression unchanged.
- Carbon basis is divided by carbon number.
- Mass basis is divided by a species-specific molecular weight. Molecular weight is required
  for every record, because paraffin, olefin, and oxygenate masses at the same carbon number
  are not interchangeable.

## Residuals and cuts

Predicted raw amounts come from the fitted intercept and slope. Log residual is
`ln(observed/predicted)` and relative deviation is `(observed-predicted)/predicted`.
Observed fractions and fitted values shown together use the same denominator: the total
observed molar-equivalent amount over the supplied carbon numbers. Normalizing the fitted
curve by its own predicted total would change its vertical scale and visually contradict
the free-intercept regression. The JSON field `predicted_range_fraction` remains a separate
predicted-distribution normalization and is not used as the fitted overlay.

Observed product cuts report both molecular and carbon fractions closing over supplied
measurements. Users define cut boundaries; names alone never imply universal gasoline,
diesel, or wax definitions.

## References

1. P. J. Flory, “Molecular Size Distribution in Linear Condensation Polymers,” *Journal of
   the American Chemical Society* 58 (1936) 1877–1885.
   <https://doi.org/10.1021/ja01301a016>
2. R. A. Friedel and R. B. Anderson, “Composition of Synthetic Liquid Fuels. I. Product
   Distribution and Analysis of C5–C8 Paraffin Isomers from Cobalt Catalyst,” *Journal of
   the American Chemical Society* 72 (1950) 1212–1215.
   <https://doi.org/10.1021/ja01159a039>
3. D. Vervloet et al., “Selectivity of the Fischer–Tropsch process: deviations from single
   alpha product distribution explained by gradients in process conditions,” *Catalysis
   Science & Technology* 3 (2013) 3122–3135. <https://doi.org/10.1039/C3CY00080J>
4. R. Partington et al., “Quantitative carbon distribution analysis ... from a Co/TiO2
   catalyst,” *Journal of Analytical Science and Technology* 11 (2020) 42.
   <https://doi.org/10.1186/s40543-020-00235-5>

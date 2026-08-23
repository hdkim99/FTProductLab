# Naming and competitive audit

Audit date: 2026-08-23. Checks included exact and similar-name GitHub repository searches,
PyPI JSON endpoints, general web search, scientific-software searches, commercial products,
and Python/macOS GUI terminology. An empty single GitHub query was not treated as proof of
availability.

## Result

- Working name: `ASFStudio`
- Selected project and GitHub repository: `FTProductLab`
- PyPI candidate: `ftproductlab` (HTTP 404 at audit time)
- Python import: `ftproductlab`
- Assessment: CLEAR
- Known risk: “FT” can mean Fourier transform outside catalysis; the full compound name and
  metadata consistently spell out Fischer–Tropsch.

`ASFStudio` had no exact package collision but was rejected because ASF is heavily used for
Advanced Systems Format media, Alaska Satellite Facility tooling (`asf_search`), and other
unrelated formats. The name would be harder to retrieve without an FT qualifier.

## Candidates reviewed

| Candidate | Risk | Decision |
|---|---|---|
| ASFStudio | MINOR | Broad ASF acronym collision |
| ASFWorkbench | MINOR | Same acronym problem; longer |
| ASFExplorer | MINOR | Same acronym and generic “Explorer” |
| ASFAnalyzer | MINOR | Same acronym and generic analyzer term |
| ASFKit | MINOR | Short but scope is opaque |
| ASFPlotter | MINOR | Undersells analysis and export |
| FTProductLab | CLEAR | Selected; concise and scientifically descriptive |
| FTDistribution | MINOR | Generic distribution term and unrelated GitHub hits |
| FTSelectivity | CLEAR | Good alternative, but excludes O/P and residual emphasis |
| ChainGrowthLab | MINOR | Could describe polymer or biological chain growth |
| CarbonChainFit | CLEAR | Descriptive but fit-only and less FT-specific |
| FTSpectrum | HIGH | Strong Fourier-transform/mass-spectrometry ambiguity |
| ASFInsight | MINOR | Broad acronym and product-like wording |

At selection time, the exact `hdkim99/FTProductLab` repository did not exist, GitHub name
search showed no exact project, PyPI returned 404, and exact general-web search returned no
product or company. Availability is a point-in-time technical check, not legal trademark
advice.

## Competitive scope

Published FT work commonly performs ASF fits in spreadsheets, MATLAB, reactor models, or
paper-specific scripts. Aspen and proprietary reactor/process packages solve a different,
larger simulation problem. FTProductLab is deliberately an offline, vendor-neutral,
reproducible analysis tool: species-preserving aggregation, explicit basis conversion,
explicit fit range/weighting, residuals, cuts, O/P states, CLI/API/Tk GUI, and publication
exports. It does not compete as a process simulator or claim mechanistic model selection.

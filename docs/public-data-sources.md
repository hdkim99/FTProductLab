# Public research data and literature validation

This register records what FTProductLab was actually tested against. “Raw”, “processed”,
“published-number reproduction”, and “metadata audit” are intentionally distinguished.
Original source files are not committed; only the attributed FTP-PUB-002 regression excerpt
is retained.

## Search record

Searched in August 2026: Zenodo and DataCite metadata, Figshare/ACS supporting information,
Apollo (University of Cambridge Repository), Springer Nature article data, RSC supporting
information, and journal data-availability links. Nine plausible FT sources were inspected.
Three were selected.

Rejected candidates included an Fe–Zr–Na ACS Omega SI containing only a plotted ASF figure,
a nano-Fe Energy & Fuels SI without a reusable carbon-number table, a Co/TiO2 O/P study
limited to C2–C5 rather than broad ASF data, a Co DFT supplement containing coordinates
rather than product data, and an RSC source whose SI was not available under sufficiently
clear reusable access during this audit. Sources were not rejected because their results
disagreed with the software.

## Validation register

| ID | Source and persistent identifiers | License | System/data used | Validation scope | Original included? |
|---|---|---|---|---|---|
| FTP-PUB-001 | Roy Partington et al., “Quantitative carbon distribution analysis of hydrocarbons, alcohols and carboxylic acids in a Fischer-Tropsch product from a Co/TiO2 catalyst during gas phase pilot plant operation,” *JAST* 11, 42 (2020), [DOI 10.1186/s40543-020-00235-5](https://doi.org/10.1186/s40543-020-00235-5) | CC BY 4.0 | Co/TiO2 pilot-plant gas/liquid/wax tables and reported alpha/C5+ | Published-number benchmark; fit-range, C1/C2, phase-aggregation, and basis metadata audit | No |
| FTP-PUB-002 | Qingyuan Zheng et al., *Research data supporting “Operando magnetic resonance imaging…”*, Apollo, [dataset DOI 10.17863/CAM.92264](https://doi.org/10.17863/CAM.92264); related [publication DOI 10.1038/s41929-023-00913-8](https://doi.org/10.1038/s41929-023-00913-8) | CC BY 4.0 | Ru/TiO2, 220 °C, 37 bar; `Fig.1.xlsx`, sheet `Fig1e`, C1–C100 wax mole fractions at feed H2/CO 2, 1, 0.5 | Raw repository-workbook fit; independent OLS; plotting; measured-range boundary interpretation | No; attributed 22-row modified excerpt included |
| FTP-PUB-003 | Junhu Gao et al., “Irregularities in Product Distribution of Fischer–Tropsch Synthesis Due to Experimental Artifact,” *IECR* 51 (2012), [publication DOI 10.1021/ie201671g](https://doi.org/10.1021/ie201671g), [SI DOI 10.1021/ie201671g.s001](https://doi.org/10.1021/ie201671g.s001) | CC BY-NC 4.0 for the Figshare SI record | Industrial Fe/Mn Run A-2 Table S1 mass flows: paraffins C1–C60, olefins C2–C30, alcohols C1–C19 | Processed experimental-table aggregation, mass-to-mole conversion, fit-range dependence, residuals, C5+ over supplied range, O/P, and Table S2 closure audit | No |

## File integrity and extraction

| ID | Remote file | Original checksum | Files/rows used |
|---|---|---|---|
| FTP-PUB-001 | Springer full article HTML | SHA-256 `9171a395a4cb242119f979d1ccc5dd9b3b295d2ba76b5c0b47702eaeab12e07d` | Article text and Tables 3–5; no rows redistributed |
| FTP-PUB-002 | `Fig.1.xlsx` from Apollo | SHA-256 `d7ed46cafe9c0024c3f9c63a022a4092b1a5b8eacb30342a1811f88f83291b1d` | Sheet `Fig1e`, wax-product mole fractions; fixture retains H2/CO=1 C30–C50 and one C10 point |
| FTP-PUB-003 | `ie201671g_si_001.pdf`, Figshare file 4129978 | SHA-256 `fe69cce3bfc32f21a58a72b53606d267c272a91aaa2e542978f6137b55607ef2`; publisher MD5 `16d42aa4d6d2b85855c53063fb70dd4d` | Table S1 Run A-2 and Table S2; no CC-BY-NC rows redistributed |

The FTP-PUB-001 table-page SHA-256 values are
`5dfdf7856e47e236b49ae1bd09ff7beecc3a170b9a102bd5bfb67ed79d125856`,
`f5108285d2765867efea7f5e98aa54e2e655466d0e818cb9b9e3dd9250e31332`, and
`ebce2e97edbf4020fde250595ad6d52fa835a5da3895561e3f3dce3f939c4e03`
for Tables 3, 4, and 5 respectively.

## Scientific comparisons

### FTP-PUB-001 — Co/TiO2

The article reports hydrocarbon alpha 0.92 from C10–C40, with methane/C2 excluded because
they do not follow the fitted line, and reports C5+ 85.0%. It tabulates separate phase
quantities but the combined per-carbon C10–C40 distribution is only shown graphically.
FTProductLab therefore does not invent a digitized reference series or claim exact raw-data
reproduction. Classification: **insufficient metadata for numeric reproduction**, not an
implementation failure.

### FTP-PUB-002 — Ru/TiO2

Using the workbook's molar fractions and uniform, unweighted `ln(amount)` versus carbon
number regression over C30–C50 gives:

| Feed H2/CO | alpha | transformed R² |
|---:|---:|---:|
| 2.0 | 0.8837262481 | 0.9977201280 |
| 1.0 | 0.9299914762 | 0.9973376575 |
| 0.5 | 0.9384092760 | 0.9927089586 |

The independently computed slopes on the workbook's `Fig1f` logarithms agree. Zeros at
C1–C9 describe products outside this wax-phase measurement rather than below-detection
measurements; they are excluded by the explicit C30–C50 range and are not used as methane
or C2 deviation evidence.

### FTP-PUB-003 — industrial Fe/Mn

Species-specific molecular weights convert the reported g/day values before fitting. The
same measured Run A-2 data give alpha 0.88235535 (C6–C20), 0.94460763 (C31–C60), and
0.92731071 (C6–C60). The C6–C60 transformed R² is 0.97095578, while structured residuals
remain visible. C5+ over the supplied Table S1 range is 0.78470898 on a carbon basis; this
must not be compared directly with whole-product C5+ values using another phase or carbon
closure convention.

Table S1 gives C4 hydrocarbon mass `0.0816 + 0.234 = 0.3156 g/day`, while Table S2 prints
`0.313 g/day`; the 0.0026 g/day (0.83%) difference is recorded as a
**publication/data discrepancy**. Other C1–C23 totals agree within table rounding. Table S1
also labels olefins through C60 in its note although numerical olefin rows stop at C30. No
author error is inferred.

## Failure register

| Project | Dataset ID | Observed issue | Classification | Scientific impact | Fixed? | Regression | Release impact |
|---|---|---|---|---|---|---|---|
| FTProductLab | FTP-PUB-002 | 0.1.0 plotted observed fractions with the measured total but fitted fractions with a separate predicted total | implementation bug | Misleading fitted-line vertical position when supplied carbons extend beyond the fit range; fitted alpha/residuals/JSON raw predictions were correct | Yes | `test_cambridge_fit_plot_uses_the_observed_measured_range_denominator` | Corrected in 0.1.1 |
| FTProductLab | FTP-PUB-003 | Table S1 and Table S2 C4 totals differ by 0.0026 g/day; olefin range note exceeds populated rows | publication/data discrepancy | Attribution/interpretation only; no software correction justified | No code change | Documented comparison | None |

## Explicitly not validated

This round does not validate detector calibration, recovery across reactor/product phases,
unmeasured heavy tails, CO2/COx selectivity closure, automatic fit-range selection,
dual-alpha fitting, or automatic ingestion of arbitrary journal spreadsheets/PDFs. The
Cambridge workbook extraction is validation preprocessing, not a newly supported XLSX input
format.

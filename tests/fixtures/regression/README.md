# Public-data regression fixtures

`cambridge_fig1_fr1_excerpt.csv` is a minimal, modified extraction from sheet `Fig1e`
of `Fig.1.xlsx` in:

- Dataset: *Research data supporting Operando Magnetic Resonance Imaging of Product
  Distributions within the Pores of Catalyst Pellets during Fischer-Tropsch Synthesis*
- Authors: Qingyuan Zheng, Jack Williams, Léonard R. van Thiel, Scott V. Elgersma,
  Mick D. Mantle, Andrew J. Sederman, Timothy A. Baart, G. Leendert Bezemer,
  Constant M. Guédon, and Lynn F. Gladden
- Repository: Apollo — University of Cambridge Repository
- Dataset DOI: <https://doi.org/10.17863/CAM.92264>
- Related publication DOI: <https://doi.org/10.1038/s41929-023-00913-8>
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Original file: `Fig.1.xlsx`
- Original file SHA-256:
  `d7ed46cafe9c0024c3f9c63a022a4092b1a5b8eacb30342a1811f88f83291b1d`
- Extraction: H2/CO feed-ratio 1 column; C30–C50 fit values plus one measured
  point outside the fit range (C10), rounded to nine decimal places.

The retained C10 point is essential: it revealed that FTProductLab 0.1.0 plotted
observations and predictions with different normalization denominators. The fixture is
redistributed under the source dataset's CC BY 4.0 license; FTProductLab's source code
remains BSD-3-Clause.

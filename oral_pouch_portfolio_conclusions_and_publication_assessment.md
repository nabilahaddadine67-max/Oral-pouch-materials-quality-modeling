# Conclusions and Publication Assessment

**Project:** Data-Driven Quality Assessment and Predictive Modeling of Oral Nicotine Pouch Materials  
**Study type:** Independent secondary analysis of publicly reported measurements  
**Status:** Suitable for a transparently labeled research portfolio after final audit; not a validated optimum or original laboratory study.

## Integrated scientific conclusion

This project assembled and independently reanalyzed published physical-characterization, formulation, release, moisture, flavor-composition, and storage-stability observations relevant to oral nicotine pouch materials. The analysis identified several potentially important relationships, while demonstrating why they cannot yet be converted into a single validated prediction of product quality.

Across seven commercial products in Platt et al. (*Scientific Reports*, 2026), water activity and oven volatiles were strongly positively associated (Pearson r = 0.983), whereas density-derived powder-bed porosity was only weakly associated with oven volatiles (r = -0.333). These findings distinguish powder-bed packing from internal cellulose pore structure and suggest that moisture behavior cannot reliably be inferred from a bulk-density porosity calculation alone. The cross-product sample is small and heterogeneous, so neither association establishes causality.

Independent reanalysis of eight public patent formulations found descriptive 30-minute release contrasts of +18.27 percentage points for premix VI versus II, -6.23 percentage points for alginate presence, +9.32 percentage points for calcium chloride presence, and -6.78 percentage points for their alginate–calcium chloride interaction. An exploratory reduced model that included the interaction reduced leave-one-out RMSE from 7.33 to 3.74 percentage points. These findings are limited by unreplicated conditions and co-varying ingredient amounts, including water, xylitol, and sodium chloride; thus they are not isolated causal effects or validated formulation improvements.

A separate published seven-level HPC series supported exploratory continuous-factor modeling. A quadratic fit improved leave-one-out prediction of normalized 4-minute release relative to a linear fit (RMSE 2.90 versus 4.15 percentage points), but not the 16-minute response. The accompanying MCC series was conducted separately rather than as a crossed HPC × MCC experiment. The analysis therefore cannot identify an independently validated binder–cellulose interaction or justify a two-factor response surface.

Published artificial-saliva measurements demonstrated that the test medium can modify reported nicotine dissolution endpoints without changing the product formulation. This underscores the need to model experimental conditions and to avoid merging nominally similar measurements obtained by incompatible protocols.

Flavor studies showed that chemistry and storage environment deserve explicit attention. External e-liquid aging results provided supporting context rather than pouch-specific retention coefficients. More directly, pouch patent data provided forty reported flavor-retention observations across two markers, five matrix conditions, and four storage times. At week three (30 °C, 75% RH), the no-added-fat reference retained 3% limonene and 5% linalyl acetate, compared with 69% and 95%, respectively, for the 5% coconut-fat condition. Water fraction changed alongside fat fraction, so the observed differences cannot be attributed to fat independently. Temporal holdout testing indicated that a simple first-order model was not a reliable general forecasting rule for these short series.

**Overall, the project establishes reproducible exploratory associations and testable material-quality hypotheses, but not an optimized or clinically validated commercial nicotine pouch formulation.** The strongest next research step is a replicated, controlled materials study that independently varies cellulose grade, binder level, water availability, and selected flavor-carrier properties, with predeclared physical-stability and retention endpoints. Only suitably crossed experimental observations can support response-surface modeling, multiresponse optimization, and independent validation.

## Core outcomes, source by source

- Physical/moisture characterization: Platt et al. (2026), *Scientific Reports*, Table 6 and Table 8. https://doi.org/10.1038/s41598-025-34556-5
- Factorial secondary analysis: US20260232007A1, Tables 21–22. https://patents.google.com/patent/US20260232007A1/en
- HPC and MCC series: US20250072472A1, Tables 1, 4, 5. https://patents.google.com/patent/US20250072472A1/en
- Environment/medium sensitivity: Li et al. (2025), *ACS Omega*. https://doi.org/10.1021/acsomega.5c06007
- Flavor chemistry context: source inventory and source-specific caveats in `data/SOURCES.md` and `reports/stage5_flavor_evidence.md`.
- External liquid aging comparison: *ACS Omega* (2025), https://doi.org/10.1021/acsomega.5c01266
- Direct pouch marker retention: US11844368B2, Tables 1–5. https://patents.justia.com/patent/11844368
- Additional proposed MCC sorption research: Ibrahim and Markl, University of Strathclyde open dataset (not yet analyzed), https://doi.org/10.15129/e9a284a2-8954-463e-9fed-06b5b1893c82

## Publication readiness

### GitHub public research portfolio
Ready **after** completing a final audit:

- Confirm numerical transcriptions against original source tables.
- Run every analysis script and automated test from a clean Python environment.
- Confirm all README links and figures resolve in the published repository.
- Identify every dataset as literature-extracted, calculated, or prospective/blank.
- Review source licenses and reuse rights; published patents do not necessarily grant commercial freedom to operate.
- Add author, date, version, research limitations, the integrated conclusion, and a citation file (e.g., CITATION.cff).

### Peer-reviewed article
Not yet demonstrated to be publication-ready as original experimental research. A potential **methods-oriented secondary-analysis paper** could become viable if a focused novel question is selected, provenance independently verified, a formal transparent study protocol added, model robustness and sensitivity investigated, and comparisons expanded using suitable independently held-out datasets. A new formulation-optimization paper would require controlled crossed experimental observations, independent replicates, uncertainty, and validation.

## Claims to avoid

- “We conducted eight original formulation DOE laboratory experiments.”
- “We identified the optimal nicotine pouch formulation.”
- “5% coconut fat independently causes higher retention.”
- “Bulk-density-derived porosity quantifies MCC internal nanopores.”
- “The model predicts commercial shelf-life or safety.”
- “An interpolated 3D contour from categorical or separate one-factor experiments is a validated response surface.”

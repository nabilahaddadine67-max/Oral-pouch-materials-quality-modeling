# Oral Pouch Materials: Public-Data Quality Modeling and DOE

**Independent reproducible research portfolio | materials characterization, formulation science, and statistical analysis**

This project reanalyzes publicly reported experimental data to study the relationships among tapped bulk density, estimated powder-bed porosity, flowability, moisture, and formulation-dependent in-vitro release profiles.

> **No proprietary or employer data.** Published summary data only. No original laboratory measurements are claimed.

## New: independent factorial reanalysis (secondary analysis)

The original patent data were collected by the patent applicant, **not** by this project. This repository now performs an independent arithmetic factorial reanalysis of eight reported formulations, computes release-profile summaries, and compares two explicitly exploratory reduced prediction models. It does **not** establish a quality optimum.

**[Read the factorial analysis and limitations](reports/factorial_study.md)** · **[See computed effects](data/factorial_effects_by_time.csv)** · **[Compare models](data/model_comparison_30min.csv)**

### Observed 30-minute release: all eight categorical conditions

![Categorical heatmap of observed 30-minute release](figures/categorical_factorial_heatmap.png)

### Factorial contrasts over time

![Factorial effects over release measurement time](figures/factorial_effects_over_time.png)

### Exploratory out-of-sample prediction check

![Leave-one-out prediction vs observed release](figures/main_effects_loocv.png)

**Note:** A continuous contour or response surface is **not appropriate** for three two-level categorical factors. The colored heatmap displays only combinations actually measured in the patent. Eight unreplicated runs cannot establish a statistically validated optimum. Published formulations also differ in some ingredients outside the three simplified factor labels; the report explicitly discusses this confounding.

**Run the new study** after installing requirements:

```powershell
python scripts/factorial_study.py
```

## Research questions

1. How do tapped-bed porosity and oven volatiles vary across seven commercial oral nicotine pouch fillers?
2. What are the *descriptive* main and interaction effects of premix category, sodium alginate presence, and calcium chloride presence on 30-minute release in eight publicly reported patent formulations?
3. Which hypotheses warrant prospective replicated experiments before a product-quality improvement can be claimed?

## Project layout

```text
oral-pouch-materials-quality-modeling/
├── README.md
├── requirements.txt
├── data/
│   ├── SOURCES.md
│   ├── physical_properties_table6.csv
│   ├── moisture_table8.csv
│   └── patent_table22_release.csv
├── scripts/
│   ├── analyze.py
│   └── factorial_study.py
├── tests/
│   └── test_data.py
├── reports/
│   ├── results.md        (generated)
│   └── factorial_study.md
└── figures/              (generated PNGs)
```

## Run on Windows (Python 3.9+)

From the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/analyze.py
python scripts/factorial_study.py
```

Open the `figures` directory for the charts and `reports/results.md` for calculated results. If PowerShell blocks activation, run `.venv\Scripts\python.exe` directly instead of activating.

## Data and methods

**Study A (observational):** Seven commercial products reported in Platt et al., *Scientific Reports* (2026). Reported void fraction is defined as `100 × (1 − tapped bulk density / true density)`. This refers to the *packed powder bed*, not nanometer-scale pores inside MCC particles. Density-derived quantities (Carr index, Hausner ratio, and porosity) are algebraically related to input densities; do not enter all of them as independent causal predictors.

**Study B (formulation comparisons):** Eight patent examples in US20260232007A1, Table 22. The analysis codes premix II/VI, alginate absence/presence, and CaCl2 absence/presence as -1/+1. For each factor and interaction, the script calculates the difference in mean 30-minute release at the +1 and -1 levels. These are descriptive factorial contrasts, **not** significance-tested effects.

The studies are distinct and **must not be merged into a single factorial model**.

## Interpretation safeguards

- Seven product-level averages are too few to validate a multivariable predictive quality model.
- The eight patent runs have no cell-level replicates, leaving no pure-error estimate in a fully saturated 2³ model.
- Some patent formulation ingredients co-vary with the coded factors (e.g., xylitol, purified water, NaCl); this limits causal attribution.
- Higher release at 30 min is *not* automatically higher quality. Target performance specifications, stability, sensory properties, and safety are not jointly available here.
- These analyses generate hypotheses for **future, separately validated** experiments rather than claiming an optimized formulation.

## Reproducibility / attribution

See [`data/SOURCES.md`](data/SOURCES.md) for each primary source, the precise original tables, and caveats. Published numerical results are identified separately from our calculations. The scripts and report are original and can be reused with attribution. Check the original publication's license for reuse of source data; patents can still carry enforceable rights.

## Planned expansions

- Extract source-verified, numerical dissolution endpoints from the peer-reviewed study to compare with material properties.
- Add replication, uncertainty, and prospective formulation DOE when independent experimental data become available.
- Create literature-grounded, multiobjective quality specifications rather than maximizing one release endpoint.


---

## Stage 2 — Continuous-factor public-data reanalysis (2025 patent)

We independently transcribed Tables 1, 4 and 5 of [US20250072472A1](https://patents.google.com/patent/US20250072472A1/en) and investigated **seven hydroxypropyl-cellulose binder levels** and a **separate four-level MCC comparison**. These are independent secondary analyses; no experiments were conducted for this repository.

[Read the continuous-factor analysis](reports/continuous_factor_study.md) · [View model comparison CSV](data/hpc_model_comparison.csv) · [Source binder dataset](data/hpc_binder_patent_table4_table5.csv)

### Observed binder-level trend and exploratory regression

![Published binder levels and early release, with exploratory linear and quadratic fits](figures/hpc_vs_release4.png)

![Published binder levels and 16-min release](figures/hpc_vs_release16.png)

### Other physical properties

![Moisture versus binder level](figures/hpc_vs_moisture.png)

### Separate MCC study

![MCC levels and release, reported from a different published experiment](figures/mcc_vs_release.png)

### Actual measured binder levels by measurement time — NOT a two-factor RSM

![Observed release heatmap for binder level against measurement time](figures/hpc_time_observed_heatmap.png)

**Scientific limits:** Published patent-applicant results are unreplicated, and some outcomes and covariates (including pH) differ across runs. HPC binder and MCC were *not* studied jointly as a crossed factorial design. This is not evidence for a validated optimum; no invented 3D contour or response surface is shown. The [prospective DOE template](data/prospective_two_factor_design_TEMPLATE_NOT_RESULTS.csv) contains blank response cells for potential future laboratory work.

Run locally: `python scripts/continuous_factor_study.py`.


---

## Stage 3 — Material quality, sensitivity checks and prospective DOE

**[Read Stage 3 scientific report](reports/stage3_material_quality.md)** · [See quantitative associations](data/stage3_associations_and_sensitivity.csv) · [Open blank non-nicotine DOE](data/stage3_prospective_non_nicotine_DOE_BLANK.csv)

This phase compares **publicly reported moisture, water activity, particle-bed porosity, and binder-series physical responses** with leave-one-out sensitivity analysis. It also locates an independently released [open DVS/particle-size MCC dataset](https://doi.org/10.15129/e9a284a2-8954-463e-9fed-06b5b1893c82) for possible follow-up validation. The 115-MB external raw dataset is *not bundled or analyzed yet*.

### Measured cross-product moisture relationship

![Water activity vs oven volatiles](figures/stage3_aw_vs_oven_volatiles.png)

### Robustness check: does a single product dominate the correlation?

![Leave-one-out sensitivity](figures/stage3_porosity_loo_sensitivity.png)

### HPC series: physical-response variation

![HPC moisture and pH](figures/stage3_hpc_moisture_ph.png)

**Proposed experiment, not actual measurements:** The blank 81-run non-nicotine material design crosses MCC grade, HPC fraction, and RH with three independent preparations. This establishes what data are needed before a continuous response surface or optimum can be defended.

```powershell
python scripts/stage3_material_quality.py
```


---

## Stage 4 — Additional public data: robustness to test environment

**[Read the Stage 4 evidence report](reports/stage4_environmental_robustness.md)** · [Inspect the new literature observations](data/stage4_artificial_saliva_observations.csv) · [Source comparability inventory](data/stage4_public_data_feature_inventory.csv)

A 2025 peer-reviewed study provides data for one nicotine pouch product tested in **three different artificial salivas**, plus 3-brand same-medium assays and a neat-solution medium control. This adds an experimentally observed source of **measurement variability** to our predictive-quality framework; it does not yield a new commercial formulation optimum.

![Same product, different media](figures/stage4_zyn_saliva_concentration.png)

![Same medium, product comparison](figures/stage4_orthana_pH_permeability.png)

![Medium control benchmark](figures/stage4_medium_permeability_benchmark.png)

**Why this matters:** The test medium and assay design must be recorded alongside material properties. Different datasets are kept separate until their SKU, physical composition, endpoint definitions and protocols can be matched. Source: [Li et al. (2025), ACS Omega](https://doi.org/10.1021/acsomega.5c06007).

Run: `python scripts/stage4_environmental_robustness.py`.


---

## Stage 5 — Flavor effects: published evidence and material-quality DOE

**[Read the flavor evidence report](reports/stage5_flavor_evidence.md)** · [Published analytes](data/stage5_published_flavor_analyte_examples.csv) · [Source inventory](data/stage5_flavor_source_inventory.csv) · [Blank non-nicotine flavor DOE](data/stage5_proposed_flavor_mcc_reference_DOE_BLANK.csv)

Public studies show that flavor identities and chemical amounts differ across products, yet some controlled comparisons report broadly similar nicotine-release profiles. Stage 5 identifies this gap without pretending to have a validated flavor-effect regression.

![Published flavor chemical amounts](figures/stage5_published_flavor_chemistry.png)

![Reported flavor dissolution similarity factors](figures/stage5_reported_flavor_similarity.png)

**No flavor-specific optimum or continuous response surface is claimed.** The prospective test matrix uses nicotine-free MCC/HPC analogs and contains blank response fields.

Run: `python scripts/stage5_flavor_evidence.py`.


---

## Stage 6 — Flavor retention: external storage evidence and testable hypotheses

[**Scientific report**](reports/stage6_flavor_stability.md) · [Published e-liquid benchmark](data/stage6_external_aging_benchmark.csv) · [Compound-specific evidence](data/stage6_compound_specific_evidence.csv) · [Blank MCC/HPC aging DOE](data/stage6_proposed_flavor_humidity_aging_DOE_BLANK.csv)

We added **six numerical published aging observations** plus compound-specific chemical findings. The reference study uses PG/VG e-liquids, **not oral pouches**; results must not be treated as MCC flavor-retention coefficients. The planned 90-sample nicotine-free analog study has no measured results and claims no optimal formulation.

![Measured e-liquid flavor loss by storage condition](figures/stage6_external_flavor_aging_conditions.png)

![Measured flavor loss at two aging timepoints](figures/stage6_external_flavor_aging_timepoints.png)

Reproduce: `python scripts/stage6_flavor_stability.py`.


---

## Stage 7 — Measured oral-pouch flavor retention: time-course model

**New direct pouch data:** [US11844368B2, Tables 1–5](https://patents.justia.com/patent/11844368) provide two measured flavor markers × five matrix conditions × four storage times (**40 published summary observations**). Storage was 30 °C / 75% RH. This is a more relevant source than extrapolating from e-liquid aging.

**[Read the scientific analysis](reports/stage7_pouch_flavor_retention.md)** · [Original transcribed data](data/stage7_patent_flavor_retention.csv) · [3-week contrasts](data/stage7_week3_descriptive_comparisons.csv) · [Week-3 held-out predictions](data/stage7_holdout_forecasts.csv)

### Measured flavor-marker retention over time
![Limonene and linalyl acetate retention across 3 weeks](figures/stage7_measured_retention_curves.png)

### Reported 3-week outcomes
![Measured week-3 retention by matrix](figures/stage7_week3_retention_by_matrix.png)

### Exploratory temporal prediction check
![Model predicted versus observed week-3 retention](figures/stage7_holdout_prediction.png)

Reproduce locally: `python scripts/stage7_pouch_flavor_retention.py`

**Critical caveat:** water content changed with fat loading (52% reference vs. 47% with 5% fat), so the effect cannot be causally attributed to fat alone. The curves are source observations; only the temporal forecast is model-generated. **No optimal formulation is claimed.**

# Stage 2 — Public-data continuous-factor reanalysis

**Status:** Independent *secondary analysis* of published patent data, not new experimental research. **No optimal nicotine-pouch formulation is established.**

## Source and extraction

US20250072472A1, *Nicotine pouch filler and method of preparing the same*, published March 6, 2025, [Google Patents](https://patents.google.com/patent/US20250072472A1/en). Table 4 reports nicotine content, pH, particle size, and moisture for preparation Examples 9–15; Table 5 reports time-series cumulative nicotine elution. Table 1 reports a **separate** four-point MCC study. The sources are patent-applicant-reported, not independently reproduced data.

Our dataset was hand-transcribed from those tables. For 12% and 16% HPC, Table 5 provides cumulative mass through 16 min but not later time points; no missing points are invented. Normalized release percentages were **derived** by dividing the reported cumulative mass (mg) by the reported total assayed nicotine (mg/pouch); published rounded percentage entries may not exactly match derived values. This analysis is subject to patent-data transcription and methodology limitations.

## Results and descriptive interpretation

- Tested HPC levels: 2, 5, 6, 8, 10, 12, 16 wt% of solid formulation.
- At 4 min the measured released masses range from 0.335 to 0.920 mg, with the highest reported value at **8 wt% HPC (Preparation Example 11)**.
- Normalized 4-min release at 8% HPC is **17.5%** of its assayed nicotine, compared with **5.9%** at 2% HPC and **12.4%** at 16% HPC.
- The same set of binder levels does **not** establish a multi-variable optimum. pH differs substantially (e.g. 7.06–8.66), so apparent binder trends may have confounding contributions or batch effects.
- The separate MCC experiment shows 4-min release declining from **17.5% at 20% MCC** to **6.1% at 55% MCC**. It cannot be crossed with the HPC study to estimate a binder×MCC interaction.

## Fit diagnostics and interpretation

For normalized 4-minute release: linear LOOCV RMSE = **4.15 percentage points**; quadratic LOOCV RMSE = **2.90 percentage points**.

For normalized 16-minute release: linear LOOCV RMSE = **11.30 percentage points**; quadratic LOOCV RMSE = **12.61 percentage points**.

The quadratic 4-minute fit has a vertex at approximately **11.19% HPC**, but this is **a statistical feature of a small, unreplicated series**, not a validated formulation recommendation or quality optimum. Model estimates are sensitive to small sample size and covariates; do not infer an optimal composition or extrapolate outside the range.

## What this teaches us

1. **Binder fraction is a useful screening factor** for further controlled experiments.
2. **Early release differs from later release**; selecting a formulation on a single time point risks misleading conclusions.
3. **Particle size, moisture, and pH should be co-measured** in new studies; this source gives only seven formulations and lacks independent replicates/uncertainty estimates.
4. **Two-factor contour plots are currently not supported.** The figure `hpc_time_observed_heatmap.png` shows binder level × *measurement time*, which is not a two-factor formulation DOE. It contains no fabricated points.

## Prospective DOE proposal (not executed)

A 3×3 factorial **planning template** is included with three MCC levels (20, 30, 40 wt%) crossed with three HPC levels (5, 8, 11 wt%) and three proposed independent replicates = 27 rows. These are **hypothetical planning levels**, **not observed values or recommended nicotine-pouch recipes**. They require checking mixture-closure constraints, ingredients, feasibility, quality targets, and safety. A true two-factor response surface requires newly measured outcomes at crossed conditions, preferably including center points or replication and randomized run order.

## Reproducibility

`python scripts/continuous_factor_study.py` regenerates the derived CSV and figures. This is literature reanalysis, not an independent laboratory validation.

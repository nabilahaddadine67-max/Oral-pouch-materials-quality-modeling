# Independent reanalysis — 2026 public patent factorial data

**Research status:** secondary reanalysis of existing patented formulations; no new physical DOE experiments were conducted. Observations are applicant-reported; not independently reproduced.

## Source and objective

[US20260232007A1](https://patents.google.com/patent/US20260232007A1/en), Example 5M, Tables 21–22 and Example 6B. Eight reported pouch compositions constitute an apparent full 2³ factorial arrangement:

- A: premix II versus premix VI (not a single isolated chemical factor)
- B: no sodium alginate versus 2 wt% sodium alginate
- C: no CaCl₂ versus 1 wt% CaCl₂

Responses: nicotine released (%) at 2, 5, 10, 30 minutes. At 30 min, the descriptive **high minus low** contrasts are:

| Contrast | Effect (percentage points) |
|---|---:|
| A — premix VI versus II | +18.27 percentage points |
| B — alginate yes versus no | -6.23 percentage points |
| C — CaCl₂ yes versus no | +9.32 percentage points |
| AB | +1.38 percentage points |
| AC | -1.38 percentage points |
| BC | -6.78 percentage points |
| ABC | +2.02 percentage points |

These are exact arithmetic contrasts for this table, **not causal effect estimates** or validated product improvements.

## Observed release profiles and calculated AUC

Time-series values remain in `data/patent_table22_release.csv`. AUC uses linear trapezoids between reported measurements and assumes release at t=0 is 0%. This integration assumption is a derived quantity, not a new measurement.

## Prediction assessment (exploratory)

We fit a reduced categorical linear model with only three main effects, and a second prespecified model with the B×C term. The model comparison file records training and leave-one-out RMSE. These scores on eight treatment combinations do **not** constitute external validation, cannot estimate batch-to-batch error, and cannot establish formulation optimum.

| model        |   n_observations |   n_parameters |   residual_df |   training_rmse_pp |   leave_one_out_rmse_pp |
|:-------------|-----------------:|---------------:|--------------:|-------------------:|------------------------:|
| main_effects |                8 |              4 |             4 |               3.67 |                    7.33 |
| main_plus_BC |                8 |              5 |             3 |               1.40 |                    3.74 |

## Critical confounding and interpretation

Table 21 shows compensating changes in xylitol and purified-water amounts across premix variants. **C19 and C20 contain 2 wt% NaCl; the other six do not.** Thus the full study is **not an independently randomized, isolated 3-factor causal experiment**. The premix change is particularly confounded, and the NaCl change coincides with two specific cells; A, B, C contrasts are descriptive formulation-package differences.

A full seven-effect factorial model would use all eight observations, leaving zero residual degrees of freedom. The four time points from each pouch formulation are repeated measurements, not independent process replicates. There are no independent error estimates for significance tests or confidence intervals. Do not claim statistical significance.

## Why there are no genuine contour/surface plots

Factors A, B, and C are binary/categorical in these observations. Interpolating smooth concentration-space contours would fabricate unmeasured intermediate recipes. `categorical_factorial_heatmap.png` instead shows only tested conditions. A **future** response-surface study requires multiple numeric ingredient concentrations, adequately replicated runs, sufficient quadratic-design points, and quality targets defined independently of nicotine release speed.

## Technical limitations

- Faster release is not necessarily better; a prespecified target and stability, sensory, and physical criteria are needed.
- The patent reports an in-vitro phosphate buffer release method at 37°C; it is not a clinical performance measurement.
- Publicly published patent information is not necessarily free of patent rights for commercial exploitation.
- Correlations across the seven commercial brands belong to a separate observational dataset and are not part of this 2³ analysis.

## Reproduction

From repo root, run `python scripts/factorial_study.py`. Outputs: `data/factorial_effects_by_time.csv`, `data/model_comparison_30min.csv`, `data/model_predictions_30min.csv`, `data/release_auc_summary.csv`, and three figures. Re-running regenerates this report too.

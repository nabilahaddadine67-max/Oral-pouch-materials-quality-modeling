# Stage 7 — Quantitative Flavor Retention in Published Oral Pouch Materials

## Research objective
Independent reanalysis of **measured oral-pouch flavor-marker retention** across storage time. Unlike Stage 6, this dataset is from **pouched materials**, not an e-liquid proxy. No experiments were performed by the portfolio author.

## Primary evidence
US Patent **US11844368B2**, *Flavoured moist oral pouched nicotine product comprising monoglyceride*, Example 1 Tables 1–5. [Readable public patent](https://patents.justia.com/patent/11844368). Conditions: **30 °C and 75% RH**, measured at **0, 1, 2 and 3 weeks**. Five matrix conditions (0% added fat, 1% or 5% coconut fat, 1% or 5% rapeseed oil); two marker compounds (limonene and linalyl acetate). The study describes GC/MS measurements and reports the values as averages of three analyses. The sample-level measurements and standard deviations are not disclosed. The patent data are applicant-reported, not peer-reviewed validation.

## Main observations: 3-week retention

| Condition | Limonene (%) | Linalyl acetate (%) |
|---|---:|---:|
| No added fat/oil | 3 | 5 |
| 1% coconut fat | 20 | 54 |
| 5% coconut fat | 69 | 95 |
| 1% rapeseed oil | 14 | 44 |
| 5% rapeseed oil | 61 | 84 |

The observed 5%-fat conditions retained more marker flavor than the reported no-added-fat reference under these specific storage conditions. They also contained **47% water versus 52% in the reference**: changing fat concentration displaced water. Therefore fat/oil loading and water amount are **confounded**, and the present data cannot isolate which ingredient caused the difference. The two markers behaved differently and cannot be collapsed into a single flavor-retention target.

## Predictive model (held-out endpoint)
Each of the ten time series (2 flavors × 5 matrix conditions) is fitted on 0-, 1-, and 2-week reported retention using a nonnegative first-order loss rate, **R(t) = 100 exp(-k t)**. The 3-week point is held out and compared with the model prediction and a naive 2-week persistence benchmark. Model fit is not evidence that the mechanisms are first-order; the original data show deviations and sometimes increases, particularly for some high-fat cases. A week-3 holdout tests prediction across time **within the same formulations**, not transfer to new pouch matrices or future storage conditions.

Run `python scripts/stage7_pouch_flavor_retention.py` to reproduce tables and figures. Read the generated `data/stage7_holdout_forecasts.csv` for actual forecast errors.

## Supporting physicochemical measurements
US11844368B2 Tables 7 and 13 report pouch peel-strength comparisons for different formulations. These are **not** a matched factorial dataset of the same five flavor-retention conditions; do not combine into a multiresponse optimum.

A separate public patent [EP4680049A1](https://patents.google.com/patent/EP4680049A1/en) reports a polysaccharide-immobilized flavor concept, with one-week humidity-aging comparisons at **30 °C / 75% RH**, and menthol stability at **50 °C for two weeks**. Its results support a separate evidence thread, not a combined regression with US11844368B2.

## Hypotheses for an independent, nicotine-free prospective DOE
Use MCC/HPC carrier specimens containing two marker flavors, and independently control **water fraction** and **hydrophobic carrier loading**. Measure GC/MS retention, KF moisture, water activity, and physical properties at multiple storage times. Include true independent preparation replicates and process blanks. A crossed factor design is required before claiming an independent effect of oil or moisture or proposing a response surface.

## Scientific boundaries
- These are applicant-reported comparative results, not licensed instructions to reproduce patented formulations or a commercial product recipe.
- Published data are auditable but **not** necessarily in the public domain; give attribution and check rights before redistribution or commercial use.
- Flavor retention in the pouch material is distinct from headspace vapor pressure, flavor release during use, sensory acceptability, or product safety.
- We cannot declare an optimal nicotine pouch formulation on these measurements alone.

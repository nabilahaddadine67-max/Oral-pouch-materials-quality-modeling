# Stage 5 — Flavor identity and matrix quality: evidence and prospective design

## Research question
**When the matrix and testing conditions are controlled, does flavor identity or level change moisture sorption, flavor retention, or cellulose–binder physical stability?** This stage does **not** infer that a flavor will enhance nicotine delivery, nor claim an optimal commercial pouch formula.

## Directly reported evidence
1. **CORESTA 2025** compared nominally 6-mg pouches in coffee, mint and mango flavors by USP-IV dissolution. The publicly available conference abstract reports `f1=4.1` and `f2=77.5` for a comparison, indicating similarity according to commonly used dissolution-profile criteria. These two numbers are **not three independent flavor responses**; full time-series responses were not recovered. [Abstract](https://www.coresta.org/abstracts/does-flavor-influence-nicotine-dissolution-profile-oral-nicotine-pouches-40388.html)
2. **Aldeek et al. (2021)** assessed a portfolio of seven named flavors and five nicotine strengths (35 combinations). Normalized nicotine dissolution curves were broadly comparable between many variants, but product differences preclude attributing a precise effect to any single flavor compound. [Separations](https://www.mdpi.com/2297-8739/8/1/7)
3. **Nicotine & Tobacco Research (2025 online / 2026 print)** quantified 33 target flavor analytes and release from multiple commercial pouches. Examples: Rogue Peppermint menthol `15.1 ± 1.2 mg/pouch`; Rogue Wintergreen methyl salicylate `14.9 ± 0.5 mg/pouch`; Juice Head Raspberry Lemonade Mint triacetin `29.0 ± 0.1 mg/pouch`. These are *different formulations*, not levels of a controlled independent factor. [DOI](https://doi.org/10.1093/ntr/ntaf105)
4. A **2026 randomized clinical investigation** compared flavors in dry versus moist pouches, but its clinical and subjective endpoints are not interchangeable with material-quality measurements. [DOI](https://doi.org/10.1016/j.drugalcdep.2026.113050)

## What we can and cannot predict
- **Observed:** Chemical analytes vary substantially across products. A published controlled flavor comparison reports similar dissolution profiles for a particular pair.
- **Not identified:** The isolated causal effect of menthol, vanillin, or any other flavor on pouch quality, because comparable fully reported multi-level material response datasets were not identified.
- **No valid surface yet:** Neither flavor **identity** (categorical) nor a collection of unrelated measured concentrations supports a joint response surface with MCC or HPC concentration.

## Suggested next laboratory study: nicotine-free material analogs
`data/stage5_proposed_flavor_mcc_reference_DOE_BLANK.csv` is a **proposed design only**, with no measurements. Compare a fixed MCC grade/HPC ratio under two independent flavored series: menthol and vanillin, each at proposed `0.5` and `1.0 wt%` of dry test material, plus a no-flavor control, with RH `33/53/75%` and `2` independent preparations each (30 planned measurements). These arbitrary screening levels are *not published optimal levels*, not consumer exposure recommendations, and must be checked for material compatibility and laboratory safety. Fixed factors must be recorded before execution.

**Candidate responses:** equilibrium water uptake (g/g), water activity, flavor retained after conditioning (%), and mechanical cohesion. Proposed analytical tools: DVS for moisture sorption, calibrated GC/GC–MS for flavor retention, Karl Fischer for water specificity, and mechanical characterization. TGA may measure mass loss, but nonselective TGA mass loss must not be automatically assigned to flavor vapor pressure.

### Model plan
1. Compare flavor types as a **categorical** factor and flavor loading and RH as numeric factors, including interactions where supported.
2. Include an actual no-flavor control and retain independent preparations and randomized run order.
3. Predefine acceptable ranges for water uptake and physical integrity; do not define one quality response by a larger nicotine-release fraction.
4. Test residual behavior, repeatability and holdout validation before reporting any candidate material ranges.
5. Add a contour plot only after collecting a crossed numeric loading × RH response matrix within the **same** flavor identity; no invented predicted measurements.

## Reproduction
`python scripts/stage5_flavor_evidence.py` reproduces two charts from values explicitly stated in published sources. It **does not** fit a predictive flavor coefficient.

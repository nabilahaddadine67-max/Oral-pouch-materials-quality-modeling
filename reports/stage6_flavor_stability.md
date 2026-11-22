# Stage 6: Flavor stability as an external benchmark; proposed MCC/HPC study

## Research objective
Determine what published storage observations can tell us about selecting **measurements and experimental factors** for a future non-nicotine flavor–cellulose material-quality study. Do not treat flavor loss in e-liquid as measured flavor loss in oral pouches.

## Source and scope
Published peer-reviewed source: *Stability of Flavoring Chemicals in e-Cigarette Liquids: A Naturalistic Product Aging Study over 24 months*, **ACS Omega (2025)**, [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12019726/), [DOI](https://doi.org/10.1021/acsomega.5c01266).

The study examined **20 flavor chemicals in 55:45 PG/VG liquids containing 40 mg/mL nicotine**, as well as commercial e-cigarette liquids, stored in three conditions: ambient with light, ambient dark, and cold dark. **There is no MCC or HPC powder matrix and no tested oral pouch.**

### Directly reported numerical observations
For *commercial e-cigarette liquid samples*, the reported fraction of initial flavor analytes that underwent **at least 50% concentration loss** was:

| Storage | Six months | Twenty-four months |
|---|---:|---:|
| Ambient + light | 20.0% | 72.9% |
| Ambient + dark | 8.6% | 25.7% |
| Cold + dark | 0% | 4.3% |

These are **percentages of analytes**, not the fraction of flavor mass lost from the product, not an estimate of mean flavor retention, and not replicated experimental runs. The paper also reports menthol maintaining at least 50% of its starting level after 24 months in individual and mixture reference liquids under all three conditions; several other analytes lost more than half in one month in light-exposed ambient storage. Source: text under Results, Figure 1 and Discussion.

## Scientifically valid insights
1. **Storage conditions matter**, especially in that liquid matrix. Comparing ambient/light and cold/dark is **not an isolated light effect**, because temperature and illumination both differ. Ambient/light vs ambient/dark is a more direct light contrast, while ambient/dark vs cold/dark is a temperature contrast, subject to study-specific details.
2. **Chemical identity matters.** Menthol was comparatively persistent in this study, whereas limonene, furaneol and methyl salicylate showed faster loss under ambient/light in reference solutions. This does not rank those chemicals for MCC-based pouches.
3. **Measured flavor recovery is not synonymous with evaporation.** Loss may arise from oxidation, reactions, partitioning, or analytical recovery; the study reported tentative byproducts. No flavor vapor pressure is calculated here.
4. **We cannot fit a pouch flavor-retention prediction model** to this dataset. It is an external benchmark for prioritizing monitoring methods and study design, not a training dataset for a pouch optimum.

## Stage 6 prospective material-screening DOE (BLANK, 90 samples)
The file `data/stage6_proposed_flavor_humidity_aging_DOE_BLANK.csv` expands the prior Stage 5 material design to independent destructive sampling at **0, 7 and 28 days**. That is 30 base combinations × 3 time points = **90 proposed samples**. It includes no nicotine and is not a product recipe.

- Categorical flavor: no flavor control, menthol, vanillin; flavor loading at 0.5 or 1.0 wt% for flavored material only; no-flavor 0%. These are illustrative screening choices, not published optimum concentrations.
- Controlled relative humidity: 33, 53, 75%; storage at 25°C in darkness as initial fixed conditions. Two independently prepared replicates per combination and sampling time.
- Keep MCC grade and HPC concentration fixed and documented. Randomize sample processing and block by measurement day where necessary.
- Measured responses: **flavor-specific recovery** by validated GC/LC with authentic calibration standards, water by Karl Fischer, water activity, and physical cohesion. For no-flavor controls, flavor retention is *not applicable*, not zero.
- Determine whether adsorption to cellulose, chemical transformation, sample extraction recovery, or volatile losses contribute to changes. A thermogravimetric mass-loss curve cannot uniquely assign flavor evaporation and does not give MCC vapor pressure.
- If the goal becomes isolated humidity effects, use the proposed controlled RH levels; if light/temperature effects are desired, plan an **additional crossed experiment**, rather than claiming them from the dark-only template.

## Data-analysis plan once measured results exist
1. Confirm measured starting flavor recovery and quantify analytical-method recovery (spiked blank matrix controls).
2. Calculate `100 × measured remaining analyte mass / initial analyte mass`, with dilution, moisture-basis, and extraction corrections documented.
3. Compare each flavor separately; use RH, loading and storage time as quantitative factors, with independent replicates and interactions. Check model assumptions and out-of-sample errors.
4. Generate true within-flavor response surfaces only after numeric crossed observations exist; never fit a continuous flavor-identity axis.
5. Optimize **material stability and controlled variability**, with predefined constraints and uncertainty. Any proposed optimum would require independent experimental confirmation.

## Reproduction
`python scripts/stage6_flavor_stability.py` plots exactly six published e-liquid aggregate percentages from `data/stage6_external_aging_benchmark.csv`. It does **not** create a pouch-retention prediction or a response surface. Charts: `figures/stage6_external_flavor_aging_conditions.png`, `figures/stage6_external_flavor_aging_timepoints.png`.

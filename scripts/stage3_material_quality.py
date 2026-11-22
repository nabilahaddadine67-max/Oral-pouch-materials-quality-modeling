"""Stage 3 independent descriptive material-quality analysis and proposed DOE.
Inputs are public summary measurements, NOT experimental replicates.
Run from repository root: python scripts/stage3_material_quality.py
"""
from pathlib import Path
from itertools import product
import csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA, FIGURES, REPORTS = [ROOT / n for n in ("data", "figures", "reports")]
for d in (DATA, FIGURES, REPORTS): d.mkdir(exist_ok=True)
physical = pd.read_csv(DATA / "physical_moisture_combined.csv")
hpc = pd.read_csv(DATA / "hpc_binder_patent_table4_table5.csv")

def corr(a, b, method="pearson"):
    return float(pd.Series(a).corr(pd.Series(b), method=method))

rows=[]
for first, second, group, frame in [
 ("oven_volatiles_pct", "water_activity", "commercial_products", physical),
 ("porosity_pct_reported", "oven_volatiles_pct", "commercial_products", physical),
 ("porosity_pct_reported", "water_activity", "commercial_products", physical),
 ("hpc_binder_wt_pct_of_solids", "moisture_pct", "patent_HPC_series", hpc),
 ("hpc_binder_wt_pct_of_solids", "mean_particle_um", "patent_HPC_series", hpc),
 ("hpc_binder_wt_pct_of_solids", "measured_pH", "patent_HPC_series", hpc),
]:
    x, y=frame[first].to_numpy(dtype=float), frame[second].to_numpy(dtype=float)
    r=corr(x,y)
    rho=corr(x,y,"spearman")
    loo=[corr(np.delete(x,i),np.delete(y,i)) for i in range(len(x))]
    rows.append(dict(dataset=group,x=first,y=second,n=len(x),pearson_r=round(r,3),spearman_rho=round(rho,3),loo_pearson_min=round(min(loo),3),loo_pearson_max=round(max(loo),3),interpretation="Exploratory association only; observational or confounded published summaries"))
pd.DataFrame(rows).to_csv(DATA / 'stage3_associations_and_sensitivity.csv',index=False)

# Figure 1: measurement scatterplot, not evidence of causality
fig,ax=plt.subplots(figsize=(8.7,5.7))
x=physical.water_activity.to_numpy(); y=physical.oven_volatiles_pct.to_numpy()
ax.scatter(x,y,s=75)
for _,r in physical.iterrows(): ax.annotate(r['product'],(r.water_activity,r.oven_volatiles_pct),xytext=(5,5),textcoords='offset points',fontsize=9)
ax.set(xlabel='Reported water activity (25 °C)',ylabel='Oven volatiles (%)',title='Seven commercial products: water activity and oven volatiles')
ax.text(.02,.96,f'Pearson r = {corr(x,y):.2f}; n = 7\nAcross different commercial recipes; not causal',transform=ax.transAxes,va='top',fontsize=9)
ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIGURES/'stage3_aw_vs_oven_volatiles.png',dpi=190);plt.close(fig)

# Figure 2: leave-one-out robustness for the material-property association
fig, ax=plt.subplots(figsize=(9,5.4))
x=physical.porosity_pct_reported.to_numpy();y=physical.oven_volatiles_pct.to_numpy()
values=[corr(np.delete(x,i),np.delete(y,i)) for i in range(len(x))]
ax.bar(physical['product'].astype(str),values)
ax.axhline(corr(x,y),linestyle='--',color='black',label=f'Full-data Pearson r = {corr(x,y):.2f}')
ax.axhline(0,color='gray',linewidth=.8)
ax.set(xlabel='Product omitted from correlation',ylabel='Pearson r',title='Porosity vs oven volatiles: influence of individual products',ylim=(-1,1))
ax.grid(axis='y',alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIGURES/'stage3_porosity_loo_sensitivity.png',dpi=190);plt.close(fig)

# Figure 3: published HPC moisture and pH variations, without optimizing nicotine release
fig,axes=plt.subplots(2,1,figsize=(8,7),sharex=True)
order=hpc.sort_values('hpc_binder_wt_pct_of_solids');x=order.hpc_binder_wt_pct_of_solids
for ax,col,ylabel in [(axes[0],'moisture_pct','Moisture (%)'),(axes[1],'measured_pH','Measured pH')]:
 ax.plot(x,order[col],marker='o');ax.set_ylabel(ylabel);ax.grid(alpha=.2)
axes[1].set_xlabel('HPC binder (% dry solids)');fig.suptitle('Separate patent HPC series: physical responses and confounding')
fig.tight_layout();fig.savefig(FIGURES/'stage3_hpc_moisture_ph.png',dpi=190);plt.close(fig)

# PROSPECTIVE only. No release or formulation-performance values invented.
grades=['MCC grade A','MCC grade B','MCC grade C']
conditions=list(product(grades,[2.0,9.0,16.0],[33,55,75],range(1,4)))
rng=np.random.default_rng(20261122)
order=rng.permutation(len(conditions))+1
with (DATA/'stage3_prospective_non_nicotine_DOE_BLANK.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['run_order_randomized','condition_id','mcc_grade_block','hpc_pct_dry_solids','conditioning_rh_pct','independent_preparation','equilibrium_moisture_pct_MEASURE','dvs_hysteresis_pct_MEASURE','cohesion_metric_MEASURE','particle_size_um_MEASURE','notes'])
 for i,(grade,hpc_pct,rh,rep) in enumerate(conditions):w.writerow([int(order[i]),f'M{i+1:03d}',grade,hpc_pct,rh,rep,'','','','',''])

report=f"""# Stage 3 — Material-quality evidence and prospective experimental design

**Scope:** Independent analysis of published summary measurements, plus a PROPOSED non-nicotine material DOE. No original experiments and no validated product-quality optimum.

## Quantitative findings

Commercial-product data: {len(physical)} products (2026 *Scientific Reports*). The Pearson correlation between reported water activity and oven volatiles is **{corr(physical.water_activity, physical.oven_volatiles_pct):.3f}** (descriptive only). Reported tapped-bed porosity and oven volatiles have Pearson **r = {corr(physical.porosity_pct_reported,physical.oven_volatiles_pct):.3f}**. Removal of one product at a time changes that last coefficient from **{min(values):.3f} to {max(values):.3f}**, demonstrating sensitivity to the small heterogeneous sample. These correlations are not independent grade-controlled observations, and oven volatiles need not be chemically specific to water.

Patent binder-series data: **{len(hpc)} distinct HPC levels**. Both moisture and pH change across reported formulations, so any relation between HPC content and measured release is confounded; neither an optimal HPC fraction nor an HPC×MCC interaction can be estimated from this independent single-factor series.

See [`data/stage3_associations_and_sensitivity.csv`](../data/stage3_associations_and_sensitivity.csv) for all reported associations and leave-one-out ranges. Correlations are exploratory and are not hypothesis tests. With these sample sizes, avoid asserting population predictions.

## New external public dataset located (not automatically incorporated)

Ibrahim and Markl (2025), University of Strathclyde: [Dataset DOI 10.15129/e9a284a2-8954-463e-9fed-06b5b1893c82](https://doi.org/10.15129/e9a284a2-8954-463e-9fed-06b5b1893c82). The deposited dataset is **115 MB**, **CC BY 4.0**, and includes DVS adsorption/desorption Excel datasets and particle-size results for MCC, croscarmellose sodium and sodium starch glycolate. **The raw 115-MB data are not bundled with this repo and are not analyzed by this script.** Download from its publisher and verify metadata before reanalysis. This is an excipient data resource, not pouch formulation response data.

Related 2025 literature: [Serajuddin et al., *Moisture sorption and desorption of different commercially available MCC grades as a function of relative humidity*](https://doi.org/10.66617/001c.141261). The article can guide future controlled grade comparisons, but its graphs are not digitized or treated as raw data here.

## Prospective RSM-ready design — not experimental results

`data/stage3_prospective_non_nicotine_DOE_BLANK.csv` has **81 independently prepared runs**, randomized within a three-grade-block × three-HPC-level × three-RH-level × triplicate plan.

- Fixed factors: MCC grade (three selected materials; labels are placeholders).
- Numeric factors: **HPC 2, 9, 16% of dry solids** and conditioning **RH 33, 55, 75%**, at a fixed specified temperature. These are illustrative factor levels, not optimized or directly prescribed pouch formulations.
- Hold powder mass, non-HPC components, preprocessing, conditioning time/criterion, analytical methods, and material lot policy constant. When HPC varies, replace an explicitly specified inert carrier so dry mass sums to 100%. Do not infer a commercial recipe from this template.
- Proposed responses: equilibrated moisture (%) by gravimetry or validated Karl Fischer; DVS hysteresis (define statistic in advance); powder cohesion (validated method); particle size (validated method).
- The response columns are **blank**. If empirical data become available, a model including numeric linear, curvature, HPC×RH interaction and MCC-grade effects can be tested, with residual and lack-of-fit diagnostics and replicate-based uncertainty. Do not fit a response surface to unmeasured values.

## Decision gate for quality improvement

A material-quality recommendation requires: (1) a predeclared quality specification, (2) crossed experiments or appropriate public crossed-factor data, (3) replication and independent validation, (4) measured trade-offs in moisture management and physical integrity, (5) assessment of whether results transfer to pouch applications. **No best commercial formulation is claimed.**

## Figures

![Observed water activity and oven volatiles](../figures/stage3_aw_vs_oven_volatiles.png)

![Leave-one-product-out porosity sensitivity](../figures/stage3_porosity_loo_sensitivity.png)

![Published binder series moisture and pH](../figures/stage3_hpc_moisture_ph.png)
"""
(REPORTS/'stage3_material_quality.md').write_text(report,encoding='utf-8')
print('Regenerated Stage 3 results, figures, and PROSPECTIVE DOE (no simulated measurements).')

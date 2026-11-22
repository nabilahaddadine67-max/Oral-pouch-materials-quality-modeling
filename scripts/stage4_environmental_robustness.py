"""Stage 4: Public literature validation and experimental-context analysis.
Data are published condition-level summaries, NOT raw replicate measurements.
No cross-study model fit; no commercial formulation optimization.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; FIG=ROOT/'figures'; REPORT=ROOT/'reports'
for d in (DATA,FIG,REPORT):d.mkdir(exist_ok=True)
source='https://doi.org/10.1021/acsomega.5c06007'
# Li et al 2025 Table 1,2,3 and text Section 3.4.4. Aggregate means, not individual experiments.
rows=[
 ('Zyn','Cool Mint',6.0,'Buffer',0.60,0.02,8.06,0.03,8.46,0.02,46.29),
 ('Zyn','Cool Mint',6.0,'Salivea',0.48,0.05,8.04,0.05,8.36,0.04,44.63),
 ('Zyn','Cool Mint',6.0,'Orthana',0.60,0.01,7.79,0.09,8.09,0.02,38.24),
 ('Dryft','Spearmint',7.0,'Orthana',0.45,0.01,7.74,0.02,7.83,0.01,31.06),
 ('Velo','Mint',4.0,'Orthana',0.38,0.04,6.94,0.05,6.83,0.00,14.84),
]
cols=['brand','flavor','label_nicotine_mg_pouch','saliva','nicotine_conc_30min_mg_ml_mean','nicotine_conc_30min_mg_ml_sd_n3','donor_pH_0min_mean','donor_pH_0min_sd_n12','donor_pH_120min_mean','donor_pH_120min_sd_n12','Papp_mean_1e_minus6_cm_s']
df=pd.DataFrame(rows,columns=cols);df['source_doi']=source
df['release_mg_at_30min_assuming_10ml']=df.nicotine_conc_30min_mg_ml_mean*10
# The 30min concentration and 120min donor pH/Papp were obtained in distinct assay stages; not independent paired replicates.
df.to_csv(DATA/'stage4_artificial_saliva_observations.csv',index=False)
products=pd.DataFrame([('Zyn','Cool Mint',6,5.58,0.31,0.41,8.22,0.02),('Dryft','Spearmint',7,5.94,0.50,0.38,8.32,0.05),('Velo','Mint',4,4.16,0.24,0.44,7.40,0.02)],columns=['brand','flavor','label_nicotine_mg_pouch','assayed_nicotine_mg_pouch','assayed_nicotine_sd_n3','pouch_mass_g','product_extract_pH','product_extract_pH_sd'])
products['source_doi']=source
products.to_csv(DATA/'stage4_product_assay_summary.csv',index=False)
# Additional mechanistic benchmark separate neat nicotine solution study (controlled nicotine at 0.5mg/mL, pH 8.5)
bench=pd.DataFrame([('Buffer',59.19),('Salivea',49.65),('Orthana',31.32)],columns=['artificial_saliva','neat_nicotine_Papp_mean_1e_minus6_cm_s'])
bench['nicotine_mg_ml']=0.5;bench['solution_pH']=8.5;bench['source_doi']=source
bench.to_csv(DATA/'stage4_neat_solution_saliva_benchmark.csv',index=False)
# Observed Zyn cross-medium spread. Not a statistical inference; n=3 summary only
zyn=df[df.brand=='Zyn'].copy(); zyn['percent_difference_from_buffer_concentration']=100*(zyn.nicotine_conc_30min_mg_ml_mean/float(zyn.query("saliva == 'Buffer'").nicotine_conc_30min_mg_ml_mean.iloc[0])-1)
zyn.to_csv(DATA/'stage4_zyn_medium_sensitivity.csv',index=False)

# Fig 1: matched product, medium effect. Errorbars authors' SD, n3
fig,ax=plt.subplots(figsize=(8.3,5.3))
x=np.arange(len(zyn));ax.bar(x,zyn.nicotine_conc_30min_mg_ml_mean.to_numpy(),yerr=zyn.nicotine_conc_30min_mg_ml_sd_n3.to_numpy(),capsize=5)
ax.set_xticks(x, zyn.saliva.to_list());ax.set(ylabel='Nicotine concentration after 30 min (mg/mL)',title='Same product, three artificial salivas (reported mean ± SD, n=3)',ylim=(0,.72))
ax.text(.02,.96,'Zyn Cool Mint 6 mg, sinker method, 10 mL medium\nSalivea: 20% lower measured mean vs Buffer; descriptive',transform=ax.transAxes,va='top',fontsize=9)
ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(FIG/'stage4_zyn_saliva_concentration.png',dpi=180);plt.close(fig)

# Fig 2: different assays: same medium Orthana, observed pH and permeability. show data without causal regression
ort=df[df.saliva=='Orthana'].set_index('brand').loc[['Zyn','Dryft','Velo']].reset_index()
fig,axs=plt.subplots(1,2,figsize=(10,4.7));
axs[0].bar(ort.brand,ort.donor_pH_0min_mean,yerr=ort.donor_pH_0min_sd_n12,capsize=4)
axs[0].set(ylabel='Donor extract pH (T=0 min)',title='Reported extract pH',ylim=(6,8.5));axs[0].grid(axis='y',alpha=.2)
axs[1].bar(ort.brand,ort.Papp_mean_1e_minus6_cm_s)
axs[1].set(ylabel='Apparent permeability (×10⁻⁶ cm/s)',title='Reported permeation (n=12)');axs[1].grid(axis='y',alpha=.2)
fig.suptitle('Orthana saliva: distinct commercial formulations — descriptive, not causal');fig.tight_layout();fig.savefig(FIG/'stage4_orthana_pH_permeability.png',dpi=180);plt.close(fig)

# Fig 3: external benchmark with independent assays
joined=zyn[['saliva','Papp_mean_1e_minus6_cm_s']].merge(bench,left_on='saliva',right_on='artificial_saliva')
fig,ax=plt.subplots(figsize=(8.2,5));idx=np.arange(3);width=.36
ax.bar(idx-width/2,joined.Papp_mean_1e_minus6_cm_s,width,label='Pouch extract')
ax.bar(idx+width/2,joined.neat_nicotine_Papp_mean_1e_minus6_cm_s,width,label='Neat nicotine solution')
ax.set_xticks(idx,joined.saliva);ax.set(ylabel='Apparent permeability (×10⁻⁶ cm/s)',title='Medium-specific assay benchmarks (not formulation effects)')
ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(FIG/'stage4_medium_permeability_benchmark.png',dpi=180);plt.close(fig)

# Provide a literature feature inventory and explicit nonmerge rule
inventory=[
 ('A','2026 Scientific Reports','commercial_product','powder-bed porosity, moisture, water activity, density','observational across 7 brands','Within study only; brands not matching SKUs across papers','10.1038/s41598-025-34556-5'),
 ('B','2026 US20260232007A1','patent_factorial','premix type, alginate, CaCl2, 2–30 min release','8 unreplicated conditions; other ingredients co-vary','Descriptive effects, no independent validation','US20260232007A1'),
 ('C','2025 US20250072472A1','patent_binder','HPC wt%, early release, pH, moisture, particle size','7 binder levels; separate MCC study','One-factor regression only, no HPC×MCC surface','US20250072472A1'),
 ('D','2025 Li et al ACS Omega','dissolution_medium','same Zyn SKU vs 3 saliva media; 3 brands in Orthana','n=3 dissolution summary; n=12 pH/permeability assay summaries','Validate environmental sensitivity; do not pool brand rows with A','10.1021/acsomega.5c06007'),
 ('E','2025 Strathclyde DVS deposit','excipient_DVS','MCC sorption / desorption, swelling, particle size','raw Excel downloadable, raw dataset NOT yet processed','Transfer-learning hypothesis only; not a pouch response','10.15129/e9a284a2-8954-463e-9fed-06b5b1893c82'),
 ('F','2026 PK modeling paper','external_model_reference','time-dependent dissolution and pH','different SKUs and protocols','Context and future study; not raw data incorporated','10.1038/s41598-026-53537-w')]
pd.DataFrame(inventory,columns=['study_id','source','experimental_unit','candidate_features','limitations','approved_use','source_identifier']).to_csv(DATA/'stage4_public_data_feature_inventory.csv',index=False)

p={r.saliva:float(r.nicotine_conc_30min_mg_ml_mean) for _,r in zyn.iterrows()}
report=f"""# Stage 4 — Environmental robustness and evidence for predictive quality models

**Independent secondary analysis; no proprietary data, no new laboratory experiments.** The 2025 ACS Omega paper provides *published aggregated* concentration, pH and apparent permeability measurements. Its CC-BY-NC-ND license is restrictive; these files record individually cited numerical observations for research with attribution, not the paper's illustrations or full text. Check conditions before redistribution/commercial reuse.

## New, actually observed sensitivity

Zyn Cool Mint 6 mg tested via the same **30 min, 10 mL sinker method** had reported concentrations of **{p['Buffer']:.2f} mg/mL (Buffer), {p['Salivea']:.2f} mg/mL (Salivea), and {p['Orthana']:.2f} mg/mL (Orthana)** (n = 3 summaries). Salivea was **{(p['Salivea']/p['Buffer']-1)*100:.1f}%** lower than Buffer for this measured endpoint. The study also reported pH and ex-vivo permeability results that vary by medium and formulation. These represent **distinct assays** and are not raw paired observations. Do not treat the product rows as independent replicates or infer statistical significance from the percentage.

![Zyn three-media sensitivity](../figures/stage4_zyn_saliva_concentration.png)

## Distinguishing product formulation from test environment

In Orthana the paper reported different extract pH and apparent permeability for Zyn, Dryft and Velo. Brand identity, dose, flavor and matrix vary together, so these differences do **not** isolate the effect of any material ingredient. Avoid fitting a continuous regression from these **three** brand-level observations.

![Same medium, different brand summaries](../figures/stage4_orthana_pH_permeability.png)

The published neat-nicotine control experiment held nicotine concentration (0.5 mg/mL) and solution pH (8.5) constant while varying the artificial saliva. This establishes that *measurement medium* affects apparent permeability in this in-vitro/ex-vivo context. These controls are **not** additional formulation runs and must not be pooled with pouch extracts.

![Permeability benchmarks](../figures/stage4_medium_permeability_benchmark.png)

## Engineering implications for future cellulose-based pouch materials work

1. Treat *measurement environment* (saliva type, buffer capacity, volume, mixing, test time) as part of the experimental protocol and model metadata, never assume an effect is formulation-caused.
2. Predeclare material-focused critical quality attributes: equilibrium moisture, water activity, particle-size variation, batch homogeneity, cohesion, and aging stability.
3. For an **MCC/HPC non-nicotine reference-material DOE**, cross binder fraction with RH and MCC grade; monitor DVS hysteresis and physical integrity using a *consistent* protocol. This design requires new measured results before a response surface can be fitted.
4. Interpret moisture and particle-size evidence separately from biological permeability; biological release and absorption are not proxy quality targets.
5. If future data permit external validation, partition by **source study, batch, and product** rather than by individual time points or repeated readings. Product names shared across papers do not establish matching SKU or comparability.

## What the new data cannot prove

- No empirically established optimum MCC/HPC composition.
- No validated cross-study pore-volume-to-release predictive model.
- No causal quality ranking of commercial brands.
- No justified 3D HPC×MCC response surface, because the studies are not a crossed factorial design.

## Reproducibility and provenance

- Original: Xia Li et al., *ACS Omega* (2025), DOI [10.1021/acsomega.5c06007](https://doi.org/10.1021/acsomega.5c06007), Tables 1–3 and §§3.4.3–3.4.4.
- `data/stage4_artificial_saliva_observations.csv`: five rows; Tables 2–3 and the reported Papp values. The 30-min concentrations were reported with n=3; pH and permeability used different experimental measurements; avoid row-level paired inference.
- `data/stage4_product_assay_summary.csv`: Table 1 n=3.
- `data/stage4_neat_solution_saliva_benchmark.csv`: section 3.4.3 controls with constant 0.5 mg/mL and pH 8.5.
- `data/stage4_public_data_feature_inventory.csv`: sources, permissible interpretation, and missing variables. The Strathclyde raw DVS archive remains external, unprocessed.
- Scripts regenerate the three original figures and derived summary tables from manually transcribed, source-attributed values.
"""
(REPORT/'stage4_environmental_robustness.md').write_text(report,encoding='utf8')
print('Stage4 written',len(df),'observed study-level conditions')

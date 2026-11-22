"""Reproduce plots and descriptive analyses from two independent public sources.
Run from repository root: python scripts/analyze.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
REPORTS = ROOT / 'reports'
FIG.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

physical = pd.read_csv(DATA / 'physical_properties_table6.csv')
moisture = pd.read_csv(DATA / 'moisture_table8.csv')
physical['porosity_pct_recomputed'] = 100 * (1 - physical['tapped_density_g_ml']/physical['true_density_g_ml'])
physical['carr_index_recomputed'] = 100 * (1 - physical['untapped_density_g_ml']/physical['tapped_density_g_ml'])
physical['hausner_ratio_recomputed'] = physical['tapped_density_g_ml']/physical['untapped_density_g_ml']
physical['porosity_difference_pp'] = physical['porosity_pct_recomputed']-physical['porosity_pct_reported']
physical.to_csv(DATA/'physical_properties_with_calculations.csv', index=False)
merged=physical.merge(moisture,on='product',validate='one_to_one')
merged.to_csv(DATA/'physical_moisture_combined.csv',index=False)

fig, ax = plt.subplots(figsize=(8,4.8))
ax.bar(physical['product'],physical['porosity_pct_reported'])
ax.set_ylabel('Reported tapped-bed porosity (%)')
ax.set_xlabel('Product')
ax.set_title('Published powder-bed porosity (Table 6)')
ax.set_ylim(0,75)
fig.tight_layout(); fig.savefig(FIG/'porosity_by_product.png',dpi=180); plt.close(fig)

fig, ax=plt.subplots(figsize=(7.2,5))
ax.scatter(merged['oven_volatiles_pct'], merged['porosity_pct_reported'],s=55)
for _,r in merged.iterrows(): ax.annotate(r['product'],(r['oven_volatiles_pct'],r['porosity_pct_reported']),xytext=(5,4),textcoords='offset points',fontsize=9)
ax.set_xlabel('Oven volatiles (%) — not water-specific')
ax.set_ylabel('Reported tapped-bed porosity (%)')
ax.set_title('Exploratory association (n=7 products; not causal)')
fig.tight_layout();fig.savefig(FIG/'porosity_vs_oven_volatiles.png',dpi=180);plt.close(fig)

release=pd.read_csv(DATA/'patent_table22_release.csv')
# Two-level categorical factors. Descriptive contrasts only; no replication.
release['A_premix']=release['premix'].map({'II':-1,'VI':1})
release['B_alginate']=release['alginate_present'].map({0:-1,1:1})
release['C_cacl2']=release['cacl2_present'].map({0:-1,1:1})
for inter,fac in [('AB',['A_premix','B_alginate']),('AC',['A_premix','C_cacl2']),('BC',['B_alginate','C_cacl2']),('ABC',['A_premix','B_alginate','C_cacl2'])]:
 release[inter]=release[fac].prod(axis=1)
effects=[]
for term in ['A_premix','B_alginate','C_cacl2','AB','AC','BC','ABC']:
 # Difference between average response at coded +1 and -1
 effect=release.loc[release[term]==1,'release_30min_pct'].mean()-release.loc[release[term]==-1,'release_30min_pct'].mean()
 effects.append({'term':term,'contrast_effect_percentage_points':effect,'absolute_effect':abs(effect)})
effects=pd.DataFrame(effects).sort_values('absolute_effect',ascending=False)
effects.to_csv(DATA/'descriptive_factorial_effects_30min.csv',index=False)

fig,ax=plt.subplots(figsize=(8,5))
for _,r in release.iterrows():
 ax.plot([2,5,10,30],[r[f'release_{t}min_pct'] for t in [2,5,10,30]],marker='o',label=r['sample'])
ax.set_xlabel('Time (min)');ax.set_ylabel('Reported cumulative nicotine release (%)')
ax.set_title('Patent Table 22: release profiles (one value per cell)')
ax.legend(ncol=2,fontsize=8);fig.tight_layout()
fig.savefig(FIG/'patent_release_profiles.png',dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.9))
ax.barh(effects['term'].iloc[::-1],effects['absolute_effect'].iloc[::-1])
ax.set_xlabel('Absolute descriptive effect (percentage points)')
ax.set_title('Factorial effects — NOT an inferential Pareto chart')
fig.tight_layout();fig.savefig(FIG/'descriptive_factorial_effects.png',dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(7,4.6))
for pre in ['II','VI']:
 subset=release[release.premix==pre]
 means=subset.groupby('alginate_present')['release_30min_pct'].mean().reindex([0,1])
 ax.plot(['Absent','Present'],means.values,marker='o',label=f'Premix {pre}')
ax.set_ylabel('Mean reported release at 30 min (%)')
ax.set_xlabel('Alginate')
ax.set_title('Descriptive premix × alginate interaction')
ax.legend();fig.tight_layout();fig.savefig(FIG/'premix_alginate_interaction.png',dpi=180);plt.close(fig)

corr=merged[['porosity_pct_reported','oven_volatiles_pct']].corr().iloc[0,1]
with (REPORTS/'results.md').open('w',encoding='utf-8') as f:
 f.write('# Reproducible results\n\n')
 f.write('## Physical characterization (independent paper dataset)\n\n')
 f.write('n = 7 products. The reported porosity is estimated from tapped/true density and is not MCC intraparticle porosity.\n\n')
 f.write(f'- Pearson r (oven volatiles vs tapped-bed porosity): {corr:.3f}. This is an exploratory, cross-product association; no causal inference is justified.\n')
 f.write(f'- Largest absolute difference between porosity recomputed from displayed rounded densities and published porosity: {physical.porosity_difference_pp.abs().max():.3f} percentage points.\n\n')
 f.write('## Patent formulation study (separate dataset)\n\n')
 f.write('Effects are mean(+1) minus mean(-1). A positive effect means higher measured release at the high-coded level.\n\n')
 f.write(effects[['term','contrast_effect_percentage_points']].to_markdown(index=False) if False else effects[['term','contrast_effect_percentage_points']].to_string(index=False))
 f.write('\n\n**Caveats:** 8 unique conditions, no cell-level replicate data; saturated 2^3 model cannot estimate pure experimental error. Changes in xylitol, added water, and NaCl among formulations may confound individual contrasts. No statistical significance claims, confidence intervals, or optimum claims.\n')
print('Done. Outputs:',FIG,REPORTS/'results.md')

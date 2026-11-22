"""Reanalysis of publicly reported patent Table 22. Run from repo root: python scripts/factorial_study.py.
All effects are descriptive; no independent replicates or formal experimental uncertainty available.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.linalg import lstsq

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
FIG=ROOT/'figures'
FIG.mkdir(exist_ok=True)
REPORT=ROOT/'reports'
REPORT.mkdir(exist_ok=True)
df=pd.read_csv(DATA/'patent_table22_release.csv')
assert len(df)==8 and df[['premix','alginate_present','cacl2_present']].drop_duplicates().shape[0]==8
for col in ('premix','alginate_present','cacl2_present'):
    assert not df[col].isna().any()
df['A_premix']=df.premix.map({'II':-1,'VI':1})
df['B_alginate']=df.alginate_present.map({0:-1,1:1})
df['C_cacl2']=df.cacl2_present.map({0:-1,1:1})
for name, cols in [('AB',['A_premix','B_alginate']),('AC',['A_premix','C_cacl2']),('BC',['B_alginate','C_cacl2']),('ABC',['A_premix','B_alginate','C_cacl2'])]:
    df[name]=df[cols].prod(axis=1)
cols=['A_premix','B_alginate','C_cacl2','AB','AC','BC','ABC']
times=[2,5,10,30]
rows=[]
for t in times:
    y=df[f'release_{t}min_pct'].to_numpy()
    for term in cols:
        effect=2*np.mean(df[term].to_numpy()*y)
        rows.append({'time_min':t,'term':term,'effect_percentage_points':effect})
effects=pd.DataFrame(rows)
effects.to_csv(DATA/'factorial_effects_by_time.csv',index=False,float_format='%.5f')
# AUC percentages x minutes, calculated using trapezoidal interpolation and *assumed* 0% at t=0.
time_axis=np.array([0,2,5,10,30])
df['auc_0_30_pct_min']=[np.sum(np.diff(time_axis)*(np.r_[0,row[[f'release_{t}min_pct' for t in times]].to_numpy(dtype=float)][:-1]+np.r_[0,row[[f'release_{t}min_pct' for t in times]].to_numpy(dtype=float)][1:])/2) for _,row in df.iterrows()]
df['auc_0_30_normalized_pct']=df['auc_0_30_pct_min']/30
# Small models: compare main-effect only to prespecified A,B,C plus BC interaction.
# No model justifies causal generalization; LOOCV reflects *within these 8 comparisons* prediction only.
models={'main_effects':['A_premix','B_alginate','C_cacl2'], 'main_plus_BC':['A_premix','B_alginate','C_cacl2','BC']}
y=df['release_30min_pct'].to_numpy()
model_rows=[]; pred=[]
for name, terms in models.items():
    X=np.c_[np.ones(len(df)),df[terms].to_numpy(dtype=float)]
    beta,*_=lstsq(X,y)
    fitted=X@beta
    loo=np.zeros(len(y))
    for i in range(len(y)):
        mask=np.arange(len(y))!=i
        coef,*_=lstsq(X[mask],y[mask])
        loo[i]=X[i]@coef
    rmse=float(np.sqrt(np.mean((y-fitted)**2)))
    cv=float(np.sqrt(np.mean((y-loo)**2)))
    model_rows.append({'model':name,'n_observations':len(df),'n_parameters':X.shape[1], 'residual_df':len(df)-X.shape[1], 'training_rmse_pp':rmse,'leave_one_out_rmse_pp':cv})
    for i,row in df.iterrows():
        pred.append({'model':name,'sample':row['sample'],'observed_release_30min_pct':y[i], 'fitted_release_30min_pct':fitted[i], 'loocv_prediction_pct':loo[i], 'loocv_error_pp':y[i]-loo[i]})
modelsdf=pd.DataFrame(model_rows)
modelsdf.to_csv(DATA/'model_comparison_30min.csv',index=False,float_format='%.5f')
pd.DataFrame(pred).to_csv(DATA/'model_predictions_30min.csv',index=False,float_format='%.5f')
df[['sample','premix','alginate_present','cacl2_present','auc_0_30_pct_min','auc_0_30_normalized_pct']].to_csv(DATA/'release_auc_summary.csv',index=False,float_format='%.4f')
plt.rcParams.update({'font.size':10,'figure.dpi':150})
# Effect trajectories
fig,ax=plt.subplots(figsize=(9,5))
for term in cols:
    pts=effects[effects.term==term]
    ax.plot(pts.time_min,pts.effect_percentage_points,marker='o',label=term)
ax.axhline(0,lw=.8,color='0.4')
ax.set(xlabel='Measurement time (min)',ylabel='High minus low contrast (percentage points)',title='Published 2³ factorial contrasts across release time')
ax.legend(ncol=4,fontsize=8);fig.tight_layout();fig.savefig(FIG/'factorial_effects_over_time.png');plt.close(fig)
# discrete categorical matrices, not false continuous contour surfaces
fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
for ax,premix in zip(axes,['II','VI']):
    sub=df[df.premix==premix]
    arr=np.array([[sub[(sub.alginate_present==b)&(sub.cacl2_present==c)].release_30min_pct.iloc[0] for c in [0,1]] for b in [0,1]])
    im=ax.imshow(arr,vmin=50,vmax=100,cmap='viridis',aspect='auto')
    for (i,j),v in np.ndenumerate(arr):ax.text(j,i,f'{v:.1f}%',ha='center',va='center',color='white' if v<72 else 'black',fontsize=13,fontweight='bold')
    ax.set_xticks([0,1],['No calcium','1% CaCl₂']);ax.set_yticks([0,1],['No alginate','2% alginate']);ax.set_title(f'Premix {premix}')
axes[0].set_ylabel('Alginate formulation');fig.colorbar(im,ax=axes,label='30-minute release (%)',shrink=.8)
fig.suptitle('Observed factorial cells — categorical heatmap, NOT response surface')
fig.subplots_adjust(left=.12,right=.86,bottom=.2,top=.80,wspace=.3)
fig.savefig(FIG/'categorical_factorial_heatmap.png',bbox_inches='tight');plt.close(fig)
# model assessment, main effects only
m='main_effects'; pr=pd.DataFrame(pred).query('model == @m')
fig,ax=plt.subplots(figsize=(6,5))
ax.scatter(pr.observed_release_30min_pct,pr.loocv_prediction_pct,s=60)
for _,r in pr.iterrows(): ax.annotate(r['sample'],(r.observed_release_30min_pct,r.loocv_prediction_pct),xytext=(4,3),textcoords='offset points',fontsize=8)
limits=[min(pr.observed_release_30min_pct.min(),pr.loocv_prediction_pct.min())-4,max(pr.observed_release_30min_pct.max(),pr.loocv_prediction_pct.max())+4]
ax.plot(limits,limits,linestyle='--',color='0.5');ax.set(xlim=limits,ylim=limits,xlabel='Observed release at 30 min (%)',ylabel='Leave-one-out predicted release (%)',title='Main-effects model: LOOCV prediction check')
fig.tight_layout();fig.savefig(FIG/'main_effects_loocv.png');plt.close(fig)
# uncertainty caution: 4 time measurements of one formulation are repeated timepoints, NOT experimental replicates.
main30=effects[effects.time_min==30].set_index('term')['effect_percentage_points']
line=lambda k:f'{main30[k]:+.2f} percentage points'
REPORT.joinpath('factorial_study.md').write_text(f'''# Independent reanalysis — 2026 public patent factorial data

**Research status:** secondary reanalysis of existing patented formulations; no new physical DOE experiments were conducted. Observations are applicant-reported; not independently reproduced.

## Source and objective

[US20260232007A1](https://patents.google.com/patent/US20260232007A1/en), Example 5M, Tables 21–22 and Example 6B. Eight reported pouch compositions constitute an apparent full 2³ factorial arrangement:

- A: premix II versus premix VI (not a single isolated chemical factor)
- B: no sodium alginate versus 2 wt% sodium alginate
- C: no CaCl₂ versus 1 wt% CaCl₂

Responses: nicotine released (%) at 2, 5, 10, 30 minutes. At 30 min, the descriptive **high minus low** contrasts are:

| Contrast | Effect (percentage points) |
|---|---:|
| A — premix VI versus II | {line('A_premix')} |
| B — alginate yes versus no | {line('B_alginate')} |
| C — CaCl₂ yes versus no | {line('C_cacl2')} |
| AB | {line('AB')} |
| AC | {line('AC')} |
| BC | {line('BC')} |
| ABC | {line('ABC')} |

These are exact arithmetic contrasts for this table, **not causal effect estimates** or validated product improvements.

## Observed release profiles and calculated AUC

Time-series values remain in `data/patent_table22_release.csv`. AUC uses linear trapezoids between reported measurements and assumes release at t=0 is 0%. This integration assumption is a derived quantity, not a new measurement.

## Prediction assessment (exploratory)

We fit a reduced categorical linear model with only three main effects, and a second prespecified model with the B×C term. The model comparison file records training and leave-one-out RMSE. These scores on eight treatment combinations do **not** constitute external validation, cannot estimate batch-to-batch error, and cannot establish formulation optimum.

{modelsdf.to_markdown(index=False,floatfmt='.2f')}

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
''',encoding='utf-8')
print(effects.query('time_min==30').to_string(index=False))
print(modelsdf.to_string(index=False))

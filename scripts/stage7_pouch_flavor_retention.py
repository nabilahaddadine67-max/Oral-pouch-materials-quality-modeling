"""Stage 7: independently reproducible descriptive analysis of US11844368B2 patent Tables 1–5.
Usage: python scripts/stage7_pouch_flavor_retention.py
Uses original source-transcribed values; no fabricated replicates. Python 3.9+.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)

with (DATA/'stage7_patent_flavor_retention.csv').open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==40
flavors=['limonene','linalyl_acetate']
orders=['No oil','1% coconut fat','5% coconut fat','1% rapeseed oil','5% rapeseed oil']
colors=plt.rcParams['axes.prop_cycle'].by_key()['color']

# plot published percentages without interpolation outside observed time range
fig,axes=plt.subplots(1,2,figsize=(12,4.6),sharey=True)
for ax,flavor in zip(axes,flavors):
    for idx,condition in enumerate(orders):
        rr=sorted((r for r in rows if r['flavor']==flavor and r['matrix_condition']==condition),key=lambda r:int(r['weeks']))
        ax.plot([int(r['weeks']) for r in rr],[float(r['reported_retention_pct']) for r in rr],marker='o',lw=2,label=condition,color=colors[idx])
    ax.set_title(flavor.replace('_',' ').title()); ax.set_xlabel('Storage (weeks)'); ax.set_xticks(range(4)); ax.grid(alpha=.25)
axes[0].set_ylabel('Reported retention (% of baseline)');axes[0].set_ylim(0,105)
axes[1].legend(bbox_to_anchor=(1.02,1),loc='upper left')
fig.suptitle('Observed flavor retention: 30 °C / 75% RH')
fig.tight_layout();fig.savefig(FIG/'stage7_measured_retention_curves.png',dpi=180,bbox_inches='tight');plt.close(fig)

# explicit descriptive comparisons at 3 weeks; zero- or 1% controls vs 5% fat conditions
summary=[]
for flavor in flavors:
    baseline=next(float(r['reported_retention_pct']) for r in rows if r['flavor']==flavor and r['matrix_condition']=='No oil' and r['weeks']=='3')
    for condition in orders:
        p=next(float(r['reported_retention_pct']) for r in rows if r['flavor']==flavor and r['matrix_condition']==condition and r['weeks']=='3')
        summary.append(dict(flavor=flavor,matrix_condition=condition,retention_week3_pct=p,absolute_change_vs_no_oil_pp=p-baseline))
with (DATA/'stage7_week3_descriptive_comparisons.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
fig,axes=plt.subplots(1,2,figsize=(11,4.4),sharey=True)
for ax,flavor in zip(axes,flavors):
    d=[r for r in summary if r['flavor']==flavor]
    ax.bar(range(5),[r['retention_week3_pct'] for r in d]);ax.set_xticks(range(5),['No oil','1% coconut','5% coconut','1% rapeseed','5% rapeseed'],rotation=30,ha='right');ax.set_title(flavor.replace('_',' ').title());ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('Reported retention after 3 weeks (%)');axes[0].set_ylim(0,105)
fig.suptitle('Measured endpoint comparison, not an optimization surface');fig.tight_layout();fig.savefig(FIG/'stage7_week3_retention_by_matrix.png',dpi=180,bbox_inches='tight');plt.close(fig)

# Honest simple predictive time model: fit to weeks 0,1,2 and forecast 3.
# Fit constrained first-order exponential R(t)=100 exp(-k*t), k>=0. Weighted equally in log space.
# Compare with simple persistence prediction at week 2; report error across 10 independent condition×flavor time-series.
forecast=[]
for flavor in flavors:
 for condition in orders:
    rr=sorted((r for r in rows if r['flavor']==flavor and r['matrix_condition']==condition),key=lambda r:int(r['weeks']))
    vals=np.array([float(r['reported_retention_pct']) for r in rr])
    times=np.array([0,1,2],dtype=float)
    logs=np.log(np.maximum(vals[:3],.001)/100)
    k=max(0.0,-float(np.dot(times,logs)/np.dot(times,times)))
    predicted=100*float(np.exp(-k*3))
    observed=float(vals[3]); last=float(vals[2]);
    forecast.append({'flavor':flavor,'matrix_condition':condition,'k_per_week':round(k,6),'predicted_week3_retention_pct':round(predicted,3),'observed_week3_retention_pct':observed,'absolute_error_pp':round(abs(predicted-observed),3),'persistence_prediction_week3_pct':last,'persistence_abs_error_pp':round(abs(last-observed),3)})
with (DATA/'stage7_holdout_forecasts.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(forecast[0]));w.writeheader();w.writerows(forecast)
mae=np.mean([r['absolute_error_pp'] for r in forecast]); baseline_mae=np.mean([r['persistence_abs_error_pp'] for r in forecast])
fig,ax=plt.subplots(figsize=(6.6,5.5))
for flavor,marker in [('limonene','o'),('linalyl_acetate','s')]:
 d=[r for r in forecast if r['flavor']==flavor]
 ax.scatter([r['observed_week3_retention_pct'] for r in d],[r['predicted_week3_retention_pct'] for r in d],label=flavor.replace('_',' ').title(),s=75,marker=marker)
ax.plot([0,100],[0,100],ls='--',color='gray');ax.set_xlim(0,100);ax.set_ylim(0,100)
ax.set_xlabel('Measured week-3 retention (%)');ax.set_ylabel('Predicted week-3 retention (%)')
ax.set_title('One-step holdout prediction (weeks 0–2 → 3)');ax.legend();ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(FIG/'stage7_holdout_prediction.png',dpi=180);plt.close(fig)

print('Rows:',len(rows),'| Week 3 forecast MAE:',round(mae,2),'pp | persistence MAE:',round(baseline_mae,2),'pp')

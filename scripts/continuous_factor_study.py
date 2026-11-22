"""Regenerate Stage 2 (public patent reanalysis) figures and model metrics.
Run from repository root: python scripts/continuous_factor_study.py
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
with (DATA/'hpc_binder_patent_table4_table5.csv').open(newline='') as file: rows=list(csv.DictReader(file))
x=np.array([float(r['hpc_binder_wt_pct_of_solids']) for r in rows]);
def field(name): return np.array([float(r[name]) for r in rows])
y4=field('release_4min_pct_derived');y16=field('release_16min_pct_derived')
def loocv(z,degree):
 e=[]
 for i in range(len(x)):
  mask=np.arange(len(x))!=i
  p=np.polyfit(x[mask],z[mask],degree)
  e.append(z[i]-np.polyval(p,x[i]))
 return np.sqrt(np.mean(np.square(e)))
metrics=[]
for label,z in [('release_4min_pct',y4),('release_16min_pct',y16),('mean_particle_um',field('mean_particle_um')),('moisture_pct',field('moisture_pct')),('pH',field('measured_pH'))]:
 for deg in (1,2):
  p=np.polyfit(x,z,deg);metrics.append([label,'linear' if deg==1 else 'quadratic',round(float(loocv(z,deg)),3),round(float(np.sqrt(np.mean((z-np.polyval(p,x))**2))),3),'; '.join(f'{c:.6g}' for c in p)])
with (DATA/'hpc_model_comparison.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['response','model','loocv_rmse','in_sample_rmse','coefficients_descending_order']);w.writerows(metrics)
def curve(filename,z,title,unit):
 xx=np.linspace(x.min(),x.max(),200);fig,ax=plt.subplots(figsize=(8,5));ax.scatter(x,z,s=50,label='Published measurements',zorder=3)
 for d,sty in [(1,'--'),(2,'-')]:ax.plot(xx,np.polyval(np.polyfit(x,z,d),xx),sty,label=['','Linear','Quadratic'][d])
 ax.set(xlabel='HPC wt% of solids',ylabel=unit,title=title);ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/filename,dpi=190);plt.close(fig)
curve('hpc_vs_release4.png',y4,'Binder vs 4-min release','Nicotine released (% of assayed content)')
curve('hpc_vs_release16.png',y16,'Binder vs 16-min release','Nicotine released (% of assayed content)')
curve('hpc_vs_moisture.png',field('moisture_pct'),'Binder vs moisture','Moisture (%)')
with (DATA/'mcc_patent_table1.csv').open(newline='') as f: mr=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(8,5));xm=[float(r['mcc_wt_pct']) for r in mr]
for key,lab in [('release_4min_pct','4-min release'),('release_20min_pct','20-min release')]:ax.plot(xm,[float(r[key]) for r in mr],marker='o',label=lab)
ax.set(xlabel='MCC wt% of solids',ylabel='Cumulative release (%)',title='Independent MCC series — Table 1');ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(FIG/'mcc_vs_release.png',dpi=190);plt.close(fig)
times=['4','8','12','16'];mat=np.array([[float(r[f'release_{t}min_pct_derived']) if t in ('4','16') else 100*float(r[f'cumulative_release_{t}min_mg'])/float(r['total_nicotine_mg_per_pouch']) for t in times] for r in rows]);idx=np.argsort(x);mat=mat[idx];fig,ax=plt.subplots(figsize=(9,5));im=ax.imshow(mat,aspect='auto',cmap='viridis',vmin=0,vmax=100)
ax.set_xticks(range(4),[f'{t} min' for t in times]);ax.set_yticks(range(len(idx)),[f'{v:g}% HPC' for v in x[idx]]);ax.set_title('Measured binder levels × measurement times (NOT two-factor RSM)')
for i in range(len(idx)):
 for j in range(4):ax.text(j,i,f'{mat[i,j]:.1f}',ha='center',va='center',color='white' if mat[i,j]<55 else 'black')
fig.colorbar(im,ax=ax,label='% release derived');fig.tight_layout();fig.savefig(FIG/'hpc_time_observed_heatmap.png',dpi=190);plt.close(fig)
print('Stage 2 figures and model metrics regenerated.')

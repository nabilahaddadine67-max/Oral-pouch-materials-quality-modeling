"""Stage 6: Charts from directly published e-liquid aging summary data.
No MCC-based pouch retention data exist here; no simulated observations.
"""
from pathlib import Path
import csv
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
with (R/'data/stage6_external_aging_benchmark.csv').open(encoding='utf-8',newline='') as f:
 rows=list(csv.DictReader(f))
assert len(rows)==6
conds=['Ambient with light','Ambient dark','Cold dark']
fig,ax=plt.subplots(figsize=(8.8,5.2))
for time,offset in [(6,-.18),(24,.18)]:
 vals=[float(next(r['share_analytes_at_least_50pct_loss'] for r in rows if r['condition']==c and int(r['months'])==time)) for c in conds]
 ax.bar([i+offset for i in range(3)],vals,width=.34,label=f'{time} months')
 for i,v in enumerate(vals):ax.text(i+offset,v+1,f'{v:g}%',ha='center',fontsize=9)
ax.set_xticks(list(range(3)),conds);ax.set_ylim(0,86)
ax.set_ylabel('Share of analytes with at least 50% loss (%)')
ax.set_title('Published commercial e-liquid aging: external matrix benchmark')
ax.legend();fig.tight_layout();fig.savefig(R/'figures/stage6_external_flavor_aging_conditions.png',dpi=170);plt.close(fig)
# Two-series timeline graphic, no interpolation claim
fig,ax=plt.subplots(figsize=(8.8,4.9))
for c in conds:
 xy=sorted([(int(r['months']),float(r['share_analytes_at_least_50pct_loss'])) for r in rows if r['condition']==c])
 ax.plot([q[0] for q in xy],[q[1] for q in xy],marker='o',label=c)
ax.set_xticks([6,24]);ax.set_xlabel('Reported storage time (months)')
ax.set_ylabel('Share of analytes with >= 50% loss (%)')
ax.set_title('Two published endpoints (connecting lines are visual guides only)')
ax.legend();fig.tight_layout();fig.savefig(R/'figures/stage6_external_flavor_aging_timepoints.png',dpi=170);plt.close(fig)
print('Stage 6 plots: 6 reported aggregate values; no interpolation model or pouch claim.')

"""Stage 5: Reproduce plots from directly reported flavor evidence only. No synthetic responses."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 with (ROOT/'data'/name).open(newline='',encoding='utf-8') as fp:return list(csv.DictReader(fp))
def main():
 rows=load('stage5_published_flavor_analyte_examples.csv')
 labels=[r['analyte']+'\n'+r['product'] for r in rows]
 vals=[float(r['mean_mg_per_pouch']) for r in rows]; sd=[float(r['reported_sd_mg_per_pouch']) for r in rows]
 fig,ax=plt.subplots(figsize=(10,5));ax.bar(range(len(rows)),vals,yerr=sd,capsize=5)
 ax.set_xticks(range(len(rows)),labels,fontsize=8);ax.set_ylabel('Measured analyte (mg per pouch)')
 ax.set_title('Selected published flavor analytes (different commercial products)')
 ax.text(.5,-.31,'These are different products and analytes; this is NOT a controlled flavor-effect comparison.',transform=ax.transAxes,ha='center',fontsize=9)
 fig.subplots_adjust(bottom=.32);fig.savefig(ROOT/'figures'/'stage5_published_flavor_chemistry.png',dpi=170);plt.close(fig)
 f1=float(load('stage5_reported_flavor_dissolution_comparison.csv')[0]['reported_f1']);f2=float(load('stage5_reported_flavor_dissolution_comparison.csv')[0]['reported_f2'])
 fig,axs=plt.subplots(1,2,figsize=(9,3.5));axs[0].bar(['Reported f1'],[f1]);axs[0].axhline(15,ls='--',color='gray',label='Common comparison reference');axs[0].legend(fontsize=7);axs[0].set_ylabel('Difference factor')
 axs[1].bar(['Reported f2'],[f2]);axs[1].axhline(50,ls='--',color='gray',label='Common comparison reference');axs[1].legend(fontsize=7);axs[1].set_ylabel('Similarity factor')
 fig.suptitle('CORESTA 2025: one published flavor-pair dissolution comparison')
 fig.tight_layout();fig.savefig(ROOT/'figures'/'stage5_reported_flavor_similarity.png',dpi=170);plt.close(fig)
 print('Stage 5: plotted directly reported values; no flavor-quality model fitted.')
if __name__=='__main__':main()

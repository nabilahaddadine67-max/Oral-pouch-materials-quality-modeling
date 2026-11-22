"""Stage 9: Pore Accessibility Index, matched-geometry validity checks, and published density associations.

This code does NOT calculate PAI for published pouch brands: their matched internal
water-accessible and total pore volumes are unavailable.
Python 3.9+; uses NumPy and Matplotlib already in portfolio requirements.
"""
from pathlib import Path
import argparse
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)


def calculate_pai(accessible_ml_g, total_ml_g, *, same_pore_domain, same_material_state, compatible_methodology):
    """Calculate measured pore fraction only when pore populations are compatible.
    Reject missing/invalid values and incompatible methods. No capping to 100%.
    """
    if not (same_pore_domain and same_material_state and compatible_methodology):
        raise ValueError('PAI requires matching pore-size domain, specimen state, and compatible methods')
    if accessible_ml_g is None or total_ml_g is None:
        raise ValueError('Both independently measured pore volumes must be supplied')
    a, t = float(accessible_ml_g), float(total_ml_g)
    if not (math.isfinite(a) and math.isfinite(t) and 0 <= a <= t and t > 0):
        raise ValueError('Volumes must be finite and 0 <= accessible <= total; total > 0')
    return 100 * a / t


def evaluate_measurement_file(path):
    """Import matched values from user's optional real experiment CSV.
    Blank fields return 'NOT_CALCULABLE', not zero. Flags must be explicit 'yes'.
    """
    out=[]
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            result = {'sample_id':row['sample_id'], 'pai_pct':'', 'status':'NOT_CALCULABLE', 'reason':''}
            a=row.get('water_accessible_pore_volume_ml_g','').strip()
            t=row.get('total_pore_volume_ml_g','').strip()
            if not a or not t:
                result['reason']='Missing one or both pore-volume measurements'
            else:
                try:
                    v=calculate_pai(a,t,same_pore_domain=row.get('same_pore_size_domain','').lower()=='yes',
                        same_material_state=row.get('same_hydration_state','').lower()=='yes',
                        compatible_methodology=row.get('compatible_methods','').lower()=='yes')
                    result.update(pai_pct=f'{v:.6f}',status='MEASURED_RATIO',reason='')
                except (ValueError, TypeError) as exc:
                    result['reason']=str(exc)
            out.append(result)
    return out


def pearson(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if len(x)<3 or np.std(x)==0 or np.std(y)==0:return float('nan')
    return float(np.corrcoef(x,y)[0,1])


def associations():
    rows=list(csv.DictReader((DATA/'physical_moisture_combined.csv').open(newline='',encoding='utf8')))
    x=np.asarray([float(r['porosity_pct_recomputed']) for r in rows])
    v=np.asarray([float(r['oven_volatiles_pct']) for r in rows])
    aw=np.asarray([float(r['water_activity']) for r in rows])
    products=[r['product'] for r in rows]
    rec=[]
    for name, y in [('oven_volatiles_pct',v),('water_activity',aw)]:
        rec.append({'comparison':f'powder_bed_void_fraction_vs_{name}','n':len(rows),'pearson_r':pearson(x,y),
                    'min_leave_one_out_r':min(pearson(np.delete(x,i),np.delete(y,i)) for i in range(len(x))),
                    'max_leave_one_out_r':max(pearson(np.delete(x,i),np.delete(y,i)) for i in range(len(x))),
                    'interpretation':'EXPLORATORY; density-derived void fraction is not internal pore accessibility'})
    rec.append({'comparison':'water_activity_vs_oven_volatiles_pct','n':len(rows), 'pearson_r':pearson(aw,v),
                 'min_leave_one_out_r':min(pearson(np.delete(aw,i),np.delete(v,i)) for i in range(len(x))),
                 'max_leave_one_out_r':max(pearson(np.delete(aw,i),np.delete(v,i)) for i in range(len(x))),
                 'interpretation':'EXPLORATORY; oven volatiles are not water-specific'})
    with (DATA/'stage9_published_associations.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rec[0]));writer.writeheader();writer.writerows(rec)

    fig, axes = plt.subplots(1,2,figsize=(11,4.5))
    for ax,y,lab in [(axes[0],v,'Oven volatiles (%)'),(axes[1],aw,'Water activity')]:
        ax.scatter(x,y)
        for a,b,p in zip(x,y,products):ax.annotate(p,(a,b),xytext=(3,3),textcoords='offset points',fontsize=8)
        ax.set_xlabel('Calculated powder-bed void fraction (%)')
        ax.set_ylabel(lab)
        ax.grid(alpha=.25)
    fig.suptitle('Published pouch properties (n=7): NOT internal pore accessibility')
    fig.tight_layout();fig.savefig(FIG/'stage9_published_bed_porosity_associations.png',dpi=170);plt.close(fig)

    fig,ax=plt.subplots(figsize=(9,4.5))
    for j,item in enumerate(rec):
        ax.scatter([item['pearson_r']],[j],s=60)
        ax.plot([item['min_leave_one_out_r'],item['max_leave_one_out_r']],[j,j],linewidth=5,alpha=.5)
    ax.axvline(0,linestyle='--',linewidth=1)
    ax.set_yticks(range(len(rec)),['Bed void fraction vs oven volatiles','Bed void fraction vs water activity','Water activity vs oven volatiles'])
    ax.set_xlabel('Pearson r; line spans leave-one-product-out values')
    ax.set_xlim(-1.05,1.05);ax.grid(alpha=.2,axis='x')
    ax.set_title('Exploratory associations and dependence on the 7 products')
    fig.tight_layout();fig.savefig(FIG/'stage9_leave_one_out_correlations.png',dpi=170);plt.close(fig)
    return rec


def illustration():
    """Sensitivity example only; no published pouch/internal MCC pore volumes."""
    total=np.array([.05,.10,.15,.20],float)
    frac=np.array([0,.25,.50,.75,1.00],float)
    with (DATA/'stage9_HYPOTHETICAL_pai_sensitivity_NOT_RESULTS.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f);writer.writerow(['assumed_total_pore_volume_ml_g','assumed_accessible_pore_volume_ml_g','hypothetical_pai_pct','data_type'])
        for t in total:
            for fraction in frac:
                a=t*fraction
                writer.writerow([f'{t:.3f}',f'{a:.4f}',f'{calculate_pai(a,t,same_pore_domain=True,same_material_state=True,compatible_methodology=True):.1f}','SYNTHETIC_ILLUSTRATION'])
    fig,ax=plt.subplots(figsize=(7.5,4.5))
    for t in total:
        ax.plot(t*frac,100*frac,marker='o',label=f'Total = {t:.2f} mL/g')
    ax.set_xlabel('Assumed water-accessible pore volume (mL/g)')
    ax.set_ylabel('PAI (%)')
    ax.set_ylim(0,105);ax.set_title('Mathematical sensitivity only — synthetic inputs')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    fig.savefig(FIG/'stage9_HYPOTHETICAL_pai_sensitivity.png',dpi=170);plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--measurement-csv',help='Optional CSV of actual matched experimental pore volumes')
    args=parser.parse_args()
    rec=associations();illustration()
    if args.measurement_csv:
        results=evaluate_measurement_file(args.measurement_csv)
        with (DATA/'stage9_user_measurements_pai_results.csv').open('w',newline='',encoding='utf8') as f:
            writer=csv.DictWriter(f,fieldnames=['sample_id','pai_pct','status','reason']);writer.writeheader();writer.writerows(results)
        print(f'Evaluated {len(results)} user samples; missing/incompatible samples remain unscored')
    for row in rec:print(row['comparison'],f"r={row['pearson_r']:.3f}", f"LOO=[{row['min_leave_one_out_r']:.3f},{row['max_leave_one_out_r']:.3f}]")
    print('No published commercial PAI has been calculated.')

if __name__ == '__main__':main()

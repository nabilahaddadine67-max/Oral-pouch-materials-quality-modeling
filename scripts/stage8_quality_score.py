"""Stage 8: transparent quality scoring with strict missingness policy.

Only the flavor-marker retention subscore uses matched, published observations.
The 6-domain total is a *hypothetical worked example*, not an observed product score.
Run from repo root: python scripts/stage8_quality_score.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA, FIGS = ROOT / 'data', ROOT / 'figures'
DOMAINS = ['moisture','physical','release','flavor','chemical','aging']
WEIGHTS = np.array([.25,.20,.20,.15,.10,.10])


def weighted_geometric_score(values, weights=WEIGHTS):
    """Return total 0..100, or NaN if ANY domain is missing.

    Zero desirability is a hard gate. No silent value imputation.
    """
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    if len(v) != len(w) or np.any(~np.isfinite(v)) or np.any(~np.isfinite(w)):
        return float('nan')
    if np.any((v < 0) | (v > 1)) or np.any(w < 0) or w.sum() <= 0:
        raise ValueError('desirabilities must be 0..1 and weights nonnegative')
    w = w / w.sum()
    if np.any((v == 0) & (w > 0)):
        return 0.0
    positive = w > 0
    return float(100 * np.exp(np.dot(w[positive], np.log(v[positive]))))


def retention_subscore(retentions_pct):
    """Equal-weight geometric mean of percent retention (reported 0..100)."""
    p = np.asarray(retentions_pct, dtype=float)
    if np.any((p < 0) | (p > 100)):
        raise ValueError('retention must be 0..100 percent')
    return weighted_geometric_score(p / 100, np.ones(len(p)))


def main():
    published = pd.read_csv(DATA / 'stage7_patent_flavor_retention.csv')
    week3 = published.loc[published.weeks.eq(3)].copy()
    # Two compounds measured for the SAME formulation condition and storage settings.
    obs = (week3.pivot(index=['matrix_condition','fat_wt_pct','water_wt_pct'],
                       columns='flavor', values='reported_retention_pct')
           .reset_index())
    assert set(['limonene','linalyl_acetate']).issubset(obs.columns)
    obs['flavor_marker_subscore_0_100'] = obs.apply(
        lambda r: retention_subscore([r['limonene'], r['linalyl_acetate']]), axis=1)
    for domain in DOMAINS:
        obs[f'{domain}_desirability'] = np.nan
    # Flavor marker proxy is not equivalent to a complete flavor-quality domain.
    obs['flavor_desirability'] = obs.flavor_marker_subscore_0_100 / 100
    obs['domains_with_evidence'] = 1
    obs['total_domains'] = 6
    obs['complete_product_quality_score'] = np.nan
    obs['measurement_scope'] = '2 flavor markers, 3 weeks, 30 C, 75% RH; not total pouch quality'
    obs['provenance'] = 'US11844368B2 Tables 3b and 4b; applicant-reported'
    obs.to_csv(DATA / 'stage8_measured_flavor_partial_scores.csv', index=False, float_format='%.4f')

    # Demonstration is intentionally hypothetical and must never be joined to public samples.
    profiles = pd.DataFrame([
        ['Scenario A', .90, .80, .85, .75, .90, .85],
        ['Scenario B', .70, .90, .70, .90, .80, .75],
        ['Scenario C', .85, .78, .80, .82, .72, .80],
    ], columns=['scenario'] + DOMAINS)
    profiles['illustrative_total_score'] = profiles[DOMAINS].apply(
        lambda r: weighted_geometric_score(r.values), axis=1)
    profiles['data_status'] = 'SYNTHETIC_HYPOTHETICAL_NOT_MEASURED'
    profiles.to_csv(DATA / 'stage8_hypothetical_scenarios.csv', index=False, float_format='%.5f')

    rng = np.random.default_rng(20261122)
    # Dirichlet scale 40: illustrates weight uncertainty, not data uncertainty.
    weight_draws = rng.dirichlet(WEIGHTS * 40, size=5000)
    rows=[]
    values = profiles[DOMAINS].to_numpy()
    scores=np.array([[weighted_geometric_score(v,w) for v in values] for w in weight_draws])
    for i, label in enumerate(profiles.scenario):
        rows.append({'scenario':label,'nominal_score':float(profiles.illustrative_total_score.iloc[i]),
                     'weight_sensitivity_p05':np.quantile(scores[:,i],.05),
                     'weight_sensitivity_p50':np.quantile(scores[:,i],.50),
                     'weight_sensitivity_p95':np.quantile(scores[:,i],.95),
                     'top_rank_frequency':float(np.mean(scores.argmax(axis=1)==i)),
                     'warning':'Hypothetical-only; uncertainty from assumed weights, NOT experimental CI'})
    pd.DataFrame(rows).to_csv(DATA/'stage8_weight_sensitivity_hypothetical.csv', index=False, float_format='%.5f')

    # Explainable measured retention partial scores, not overall quality.
    fig,ax=plt.subplots(figsize=(9,4.8))
    obs=obs.sort_values('flavor_marker_subscore_0_100')
    ax.barh(obs.matrix_condition,obs.flavor_marker_subscore_0_100)
    ax.set(xlim=(0,105),xlabel='Equal-weight geometric flavor-marker retention (%)',
           title='Published 3-week flavor retention: PARTIAL subscore only')
    ax.text(.99,-.23,'Applicant data: US11844368B2; fat and water co-vary. Not pouch quality.',
            transform=ax.transAxes,ha='right',fontsize=8)
    fig.tight_layout(); fig.savefig(FIGS/'stage8_measured_flavor_partial_scores.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig,ax=plt.subplots(figsize=(9,4.6))
    order=np.argsort([r['nominal_score'] for r in rows]); sr=[rows[i] for i in order]
    y=np.arange(len(sr)); median=np.array([r['nominal_score'] for r in sr])
    lo=median-np.array([r['weight_sensitivity_p05'] for r in sr]);hi=np.array([r['weight_sensitivity_p95'] for r in sr])-median
    ax.errorbar(median,y,xerr=[lo,hi],fmt='o',capsize=4)
    ax.set_yticks(y,[r['scenario'] for r in sr]);ax.set_xlim(60,100)
    ax.set_xlabel('Hypothetical PQPS (0–100)');ax.set_title('Synthetic scenarios: sensitivity to ASSUMED weights')
    ax.text(.99,-.25,'5th–95th percentile from weight perturbations, NOT experimental intervals',
            transform=ax.transAxes,ha='right',fontsize=8)
    fig.tight_layout();fig.savefig(FIGS/'stage8_hypothetical_weight_sensitivity.png',dpi=180,bbox_inches='tight');plt.close(fig)

    fig,ax=plt.subplots(figsize=(8.4,4.2))
    ax.barh(DOMAINS,[0,0,0,1,0,0]);ax.set_xlim(0,1.12)
    ax.set_title('Stage 7 samples: availability of matched scoring inputs')
    ax.set_xlabel('Measured proxy available (1 = yes; 0 = no)')
    ax.text(.99,-.22,'Flavor: 2 reported markers only, not all sensory or flavor quality',
            transform=ax.transAxes,ha='right',fontsize=8)
    fig.tight_layout();fig.savefig(FIGS/'stage8_data_completeness.png',dpi=180,bbox_inches='tight');plt.close(fig)
    print('Stage 8 complete: measured flavor subscore for',len(obs),'conditions; full published PQPS NOT calculable.')
    print(profiles[['scenario','illustrative_total_score']].to_string(index=False))

if __name__=='__main__':main()

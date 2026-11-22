import csv
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with (r/'data/stage5_published_flavor_analyte_examples.csv').open() as f: rows=list(csv.DictReader(f))
assert len(rows)==3 and all(float(x['mean_mg_per_pouch'])>0 for x in rows)
with (r/'data/stage5_proposed_flavor_mcc_reference_DOE_BLANK.csv').open() as f: template=list(csv.DictReader(f))
assert len(template)==30 and all(not x['equilibrium_moisture_g_per_g'] for x in template)
print('Stage 5 checks passed.')

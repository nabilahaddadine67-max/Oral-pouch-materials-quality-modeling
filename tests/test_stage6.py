import csv
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with (r/'data/stage6_external_aging_benchmark.csv').open() as f:rows=list(csv.DictReader(f))
assert len(rows)==6
assert {int(q['months']) for q in rows}=={6,24}
assert float([q for q in rows if q['condition']=='Cold dark' and q['months']=='24'][0]['share_analytes_at_least_50pct_loss'])==4.3
with (r/'data/stage6_proposed_flavor_humidity_aging_DOE_BLANK.csv').open() as f:plans=list(csv.DictReader(f))
assert len(plans)==90
assert all(not q['flavor_retention_percent'] for q in plans)
print('Stage 6 numerical and blank DOE checks passed.')

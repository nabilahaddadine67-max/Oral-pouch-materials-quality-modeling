import csv, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Stage3Checks(unittest.TestCase):
 def test_design_has_81_unique_runs_and_no_fake_responses(self):
  with (ROOT/'data'/'stage3_prospective_non_nicotine_DOE_BLANK.csv').open(newline='') as f: rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),81)
  self.assertEqual(len({r['run_order_randomized'] for r in rows}),81)
  self.assertTrue(all(not r['equilibrium_moisture_pct_MEASURE'] for r in rows))
  self.assertTrue(all(not r['cohesion_metric_MEASURE'] for r in rows))
 def test_association_is_derived_not_fabricated(self):
  with (ROOT/'data'/'stage3_associations_and_sensitivity.csv').open(newline='') as f: rows=list(csv.DictReader(f))
  self.assertGreaterEqual(len(rows),6)
  self.assertEqual({int(r['n']) for r in rows},{7})
if __name__=='__main__':unittest.main()

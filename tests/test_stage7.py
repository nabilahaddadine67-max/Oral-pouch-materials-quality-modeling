import unittest,csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class Stage7Tests(unittest.TestCase):
 def test_source_rows(self):
  r=list(csv.DictReader((P/'data/stage7_patent_flavor_retention.csv').open()))
  self.assertEqual(len(r),40)
  self.assertEqual(len({(x['flavor'],x['matrix_condition']) for x in r}),10)
 def test_exact_published_endpoints(self):
  r=list(csv.DictReader((P/'data/stage7_patent_flavor_retention.csv').open()))
  lookup={(x['flavor'],x['matrix_condition'],int(x['weeks'])):float(x['reported_retention_pct']) for x in r}
  self.assertEqual(lookup['limonene','No oil',3],3)
  self.assertEqual(lookup['limonene','5% coconut fat',3],69)
  self.assertEqual(lookup['linalyl_acetate','5% coconut fat',3],95)
if __name__=='__main__':unittest.main()

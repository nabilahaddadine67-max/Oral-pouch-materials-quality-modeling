"""Standard-library integrity checks, run: python -m unittest discover -s tests"""
import csv
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
 with (ROOT/'data'/name).open(newline='') as f:return list(csv.DictReader(f))
class TestData(unittest.TestCase):
 def test_physical(self):
  rows=read('physical_properties_table6.csv')
  self.assertEqual(len(rows),7)
  for r in rows:
   por=100*(1-float(r['tapped_density_g_ml'])/float(r['true_density_g_ml']))
   self.assertLess(abs(por-float(r['porosity_pct_reported'])),0.1)
 def test_patent_design(self):
  rows=read('patent_table22_release.csv')
  self.assertEqual(len(rows),8)
  keys={(r['premix'],r['alginate_present'],r['cacl2_present']) for r in rows}
  self.assertEqual(len(keys),8)
  self.assertEqual(float(next(r for r in rows if r['sample']=='P121')['release_30min_pct']),92.2)
if __name__=='__main__':unittest.main()

import unittest
from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parents[1]/'data'
class Stage4Checks(unittest.TestCase):
 def test_zyn_within_product_has_three_media(self):
  df=pd.read_csv(P/'stage4_artificial_saliva_observations.csv');z=df[df.brand=='Zyn'];self.assertEqual(set(z.saliva),{'Buffer','Salivea','Orthana'})
  self.assertEqual(len(df),5)
  self.assertAlmostEqual(float(z[z.saliva=='Salivea'].nicotine_conc_30min_mg_ml_mean.iloc[0]),0.48)
 def test_benchmark_is_not_pouch_experiment(self):
  df=pd.read_csv(P/'stage4_neat_solution_saliva_benchmark.csv');self.assertEqual(len(df),3)
  self.assertEqual(set(df.solution_pH),{8.5})
 def test_no_artificial_contour(self):
  self.assertFalse((P/'stage4_simulated_optimum.csv').exists())
if __name__=='__main__':unittest.main()

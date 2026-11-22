import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from stage8_quality_score import weighted_geometric_score, retention_subscore

class Stage8Tests(unittest.TestCase):
    def test_all_perfect(self): self.assertAlmostEqual(weighted_geometric_score([1]*6),100)
    def test_missing_is_not_imputed(self):
        import math
        self.assertTrue(math.isnan(weighted_geometric_score([1,1,1,float('nan'),1,1])))
    def test_zero_is_hard_gate(self): self.assertEqual(weighted_geometric_score([1,1,1,0,1,1]),0)
    def test_two_marker_measured(self): self.assertAlmostEqual(retention_subscore([69,95]),(69*95)**.5)
    def test_invalid(self):
        with self.assertRaises(ValueError): weighted_geometric_score([1.2]*6)
if __name__=='__main__':unittest.main()

import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from stage9_pore_accessibility import calculate_pai, evaluate_measurement_file
class TestPAI(unittest.TestCase):
    def test_valid_ratio(self):
        self.assertAlmostEqual(calculate_pai(.06,.08,same_pore_domain=True,same_material_state=True,compatible_methodology=True),75)
    def test_invalid_volume(self):
        with self.assertRaises(ValueError):
            calculate_pai(.12,.08,same_pore_domain=True,same_material_state=True,compatible_methodology=True)
    def test_mismatched_state(self):
        with self.assertRaises(ValueError):
            calculate_pai(.05,.1,same_pore_domain=True,same_material_state=False,compatible_methodology=True)
    def test_blank_is_not_scored(self):
        path=Path(__file__).resolve().parents[1]/'data'/'stage9_PAI_measurement_TEMPLATE_BLANK.csv'
        result=evaluate_measurement_file(path)
        self.assertEqual(result[0]['status'],'NOT_CALCULABLE')
if __name__=='__main__':unittest.main()

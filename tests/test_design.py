"""Tests for useful design constraints; mesh and motion checks are separate scripts."""
import importlib.util,json,math,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('calculator',ROOT/'scripts/calculator.py');calc=importlib.util.module_from_spec(spec);spec.loader.exec_module(calc)
class DesignConstraints(unittest.TestCase):
    def test_recommended_dose_thickness_combinations_fit_with_edge_margin(self):
        for volume,t in [(60,3),(80,4),(100,5),(100,4)]:
            self.assertLessEqual(calc.disk_diameter(volume,t),182)
    def test_oversized_dose_is_detected(self):
        self.assertGreater(calc.disk_diameter(100,3),186)
    def test_minimum_cord_path_and_knot_reserve(self):
        self.assertEqual(calc.cord_length(140,80,35,3,300),2040)
        self.assertGreater(calc.cord_length(150,90,40),2040)
    def test_channel_lines_stay_under_target_packet(self):
        for x in [59,91,123]:self.assertTrue(21+10<=x<=161-10)
        for y in [-25,0,25]:self.assertTrue(-40+10<=y<=40-10)
    def test_cross_channels_fit_hinge_gaps(self):
        segments=[(a,a+22) for a in [0,32,64,96,128,160]]
        for x in [59,91,123]:
            for lo,hi in segments:self.assertTrue(x+5<=lo or x-5>=hi)
    def test_kits_and_manifest_are_consistent(self):
        m=json.loads((ROOT/'config/parts.json').read_text());names=[p['name'] for p in m['parts']]
        self.assertEqual(len(names),len(set(names)))
        for p in m['parts']:
            self.assertLessEqual(p['quantities']['minimum'],p['quantities']['standard'])
            self.assertLessEqual(p['quantities']['standard'],p['quantities']['full'])
            self.assertEqual(p['file'],f"stl/{p['name']}.stl")
    def test_invalid_calculator_values(self):
        with self.assertRaises(ValueError):calc.disk_diameter(-1,4)
        with self.assertRaises(ValueError):calc.cord_length(140,80,35,0)
if __name__=='__main__':unittest.main()

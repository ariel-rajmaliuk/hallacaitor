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
    def test_familiar_doses_fit_wide_roller(self):
        for volume in [80,100]:self.assertLessEqual(calc.disk_diameter(volume,2.5)+4,266)
        self.assertGreater(calc.disk_diameter(100,2.5),186)
    def test_two_layouts_have_enough_docks_and_joiners(self):
        m=json.loads((ROOT/'config/parts.json').read_text());p={r['name']:r['quantities'] for r in m['parts']}
        self.assertEqual(p['dock_tile']['hub'],4*2)
        self.assertEqual(p['dock_joiner']['hub'],2*((4-1)*2+(2-1)*4))
        self.assertEqual(p['dock_tile']['team'],4+5)
        self.assertEqual(p['dock_joiner']['team'],2*((2-1)*2+(2-1)*2))
        for kit in ['hub','team']:
            adapters=sum(q[kit] for n,q in p.items() if n.startswith('dock_') and n not in ['dock_tile','dock_joiner'])
            self.assertLessEqual(adapters,p['dock_tile'][kit])
    def test_familiar_channels_and_cord_match_packet(self):
        self.assertEqual(calc.cord_length(160,90,35,3,300),2220)
        for y in [-30,0,30]:self.assertTrue(-45+5<=y<=45-5)
    def test_station_labels_and_published_parts_are_resolvable(self):
        m=json.loads((ROOT/'config/parts.json').read_text());names={r['name'] for r in m['parts']}
        st=json.loads((ROOT/'config/stations.json').read_text())
        self.assertEqual(len({r['id'] for r in st['stations']}),6)
        for station in st['stations']:
            self.assertIn(station['example'],names)
            self.assertIn('station_tag_'+station['id'][1:],names)
        for r in m['parts']:
            self.assertTrue((ROOT/r['source']).exists())
            self.assertTrue((ROOT/'docs/assets/v3'/f"{r['name']}.png").exists())
    def test_invalid_calculator_values(self):
        with self.assertRaises(ValueError):calc.disk_diameter(-1,4)
        with self.assertRaises(ValueError):calc.cord_length(140,80,35,0)
if __name__=='__main__':unittest.main()

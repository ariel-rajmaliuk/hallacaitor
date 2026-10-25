#!/usr/bin/env python3
"""Boolean collision sampling, not a continuous-motion or physical certification."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
from mesh import audit
ROOT=Path(__file__).resolve().parents[1]
def run_check(part,angle,out):
    r=subprocess.run([os.environ.get('OPENSCAD','openscad'),'--export-format','binstl','-o',str(out),'-D',f'part="{part}"','-D',f'angle={angle}','-D','facets=48',str(ROOT/'cad/hallacaitor.scad')],capture_output=True,text=True,timeout=180)
    if 'Current top level object is empty.' in r.stderr:return {'pair':part,'angle_deg':angle,'intersection_empty':True,'passed':True}
    if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(r.stderr)
    row={'pair':part,'angle_deg':angle,'intersection_empty':False,'passed':False}
    if part=='collision_roller_rings':
        volume=audit(out)['volume_cm3']
        row.update(volume_cm3=volume,expected='Open rings have intentional 0.2 mm diametral interference with seats; elastic fit not simulated',passed=.12<volume<.16)
    return row
def main():
    results=[]
    with tempfile.TemporaryDirectory() as td:
        for part in ['collision_base_wing','collision_wings']:
            for a in [0,10,30,50,70,90,100]:
                row=run_check(part,a,Path(td)/f'{part}_{a}.stl');results.append(row);print(row,flush=True)
    for part in ['collision_needle_paths','collision_roller_rings']:
        with tempfile.TemporaryDirectory() as td2:
            row=run_check(part,0,Path(td2)/'check.stl');results.append(row);print(row,flush=True)
    out=ROOT/'docs/validation/motion.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'method':'OpenSCAD CGAL intersection at 48 facets; samples only','cad_sha256':hashlib.sha256((ROOT/'cad/hallacaitor.scad').read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
    if not all(r['passed'] for r in results):raise SystemExit('COLLISION: inspect motion.json')
if __name__=='__main__':main()

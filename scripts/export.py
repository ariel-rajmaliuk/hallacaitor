#!/usr/bin/env python3
"""Export selected/all parts using OpenSCAD. Standard library only; no shell execution."""
from __future__ import annotations
import argparse, concurrent.futures, json, os, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def export_part(name, output, facets=64, clearance=.5):
    part=next(p for p in json.loads((ROOT/"config/parts.json").read_text())["parts"] if p["name"]==name)
    exe=os.environ.get('OPENSCAD','openscad')
    if not shutil.which(exe): raise RuntimeError('OpenSCAD not found. Install it or set OPENSCAD to its executable path.')
    output.mkdir(parents=True, exist_ok=True)
    cmd=[exe,'--export-format','binstl','-o',str(output/f'{name}.stl'),'-D',f'part="{name}"','-D',f'facets={facets}','-D',f'clearance={clearance}',str(ROOT/part.get('source','cad/hallacaitor.scad'))]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
    if r.returncode or 'ERROR:' in r.stderr: raise RuntimeError(f'{name}: {r.stderr}')
    return name

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--part',action='append',help='Repeat to select parts; default: all')
    ap.add_argument('--kit', choices=['minimum','standard','full','hub','team'])
    ap.add_argument('--output',type=Path,default=ROOT/'stl')
    ap.add_argument('--jobs',type=int,default=2)
    ap.add_argument('--facets',type=int,default=64)
    ap.add_argument('--clearance',type=float,default=.5)
    args=ap.parse_args()
    manifest=json.loads((ROOT/'config/parts.json').read_text())
    names=args.part or [p['name'] for p in manifest['parts'] if not args.kit or p['quantities'][args.kit]>0]
    known={p['name'] for p in manifest['parts']}
    if not set(names)<=known: ap.error('Unknown part name')
    if args.jobs<1 or not .2<=args.clearance<=1 or args.facets<24:ap.error('Invalid jobs, facets or clearance')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs=[ex.submit(export_part,n,args.output,args.facets,args.clearance) for n in names]
        for f in concurrent.futures.as_completed(futs): print('exported',f.result(),flush=True)
if __name__=='__main__':main()

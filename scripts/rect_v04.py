#!/usr/bin/env python3
"""Export and audit the separate Rect 0.4 CAD prototype. No food/load claims."""
import argparse,concurrent.futures,hashlib,json,subprocess,tempfile
from pathlib import Path
from mesh import audit,read_stl
R=Path(__file__).resolve().parents[1];ROOT=R/'designs/v04';CAD=R/'cad/rectangular.scad'
NAMES='rect_tile rect_frame rect_key tower_post tower_pin short_wing_north short_wing_south dry_housing dry_lid dry_shuttle dry_shuttle_small dry_hopper dry_lid_cap dry_guide_pin guiso_body guiso_gate guiso_piston piston_stop_20 piston_stop_13 strip_magazine strip_drawer strip_lid spool_box spool_left spool_right spool_adapter spool_axle spool_cover spool_washer cutter_base cutter_cover cutter_clamp cutter_pin cutter_mount_pin cutter_pedestal blade_dummy bridge_half bridge_joiner bridge_dry_front bridge_dry_back guiso_mount funnel_quarter funnel_hanger'.split()
def export(name):
 p=ROOT/'stl'/f'{name}.stl';p.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['openscad','--export-format','binstl','-o',str(p),'-D',f'part="{name}"',str(CAD)],capture_output=True,text=True,timeout=180)
 if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(name+': '+r.stderr)
 a=audit(p)
 assert a['components']==1 and a['volume_cm3']>0,(name,a)
 assert a['nonmanifold_edges']==a['orientation_errors']==a['degenerate_triangles']==0,(name,a)
 assert all(0<v<=lim for v,lim in zip(a['bbox_mm'],[220,220,250])) and abs(a['min_z_mm'])<.001,(name,a)
 return {'name':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**a}
def check(name,a=0,t=0):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'out.stl';r=subprocess.run(['openscad','--export-format','binstl','-o',str(p),'-D',f'part="{name}"','-D',f'angle={a}','-D',f'travel={t}',str(CAD)],capture_output=True,text=True,timeout=180)
  row={'name':name,'angle':a,'travel':t}
  if 'Current top level object is empty.' in r.stderr:return dict(row,passed=True,intersection_empty=True)
  if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(r.stderr)
  v=audit(p);plane=all(any(max(p[k] for p in tri)-min(p[k] for p in tri)<.00001 for k in range(3)) for tri in read_stl(p))
  return dict(row,intersection_empty=False,volume_cm3=v['volume_cm3'],bbox_mm=v['bbox_mm'],passed=abs(v['volume_cm3'])<.000001 and plane,contact='seating planes only' if plane else 'inspect overlap')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--export-only',action='store_true');ap.add_argument('--check-only',action='store_true');ap.add_argument('--part',action='append');a=ap.parse_args()
 if not a.check_only:
  rows=[]
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
   for r in ex.map(export,a.part or NAMES):rows.append(r);print('PASS mesh',r['name'],r['bbox_mm'],flush=True)
  (ROOT/'validation/geometry.json').write_text(json.dumps({'source_sha256':hashlib.sha256(CAD.read_bytes()).hexdigest(),'dependencies_sha256':{n:hashlib.sha256((R/'cad'/n).read_bytes()).hexdigest() for n in ['hallacaitor.scad','modular.scad']},'parts':rows,'method':'STL closed oriented one-component and bed envelope audit; no physical tests'},indent=2)+'\n')
 if not a.export_only:
  pairs=[(n,0,0) for n in ['check_column_frame','check_column_upper','check_lock_pin','check_guiso_gate','check_spool_coupling','check_spool_box','check_cutter_clamps','check_guiso_mount','check_funnel_hangers','check_bridge_funnel','check_cutter_mount']]
  pairs += [(n,0,t) for n in ['check_dry_shuttle','check_dry_pin','check_hangers_dosers'] for t in [0,14,28,42,56]]
  pairs += [(n,ang,0) for n in ['check_short_base','check_short_wings','check_fold_pods','check_fold_funnel'] for ang in [0,30,70,100]]
  rows=[]
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
   for r in ex.map(lambda x:check(*x),pairs):rows.append(r);print(r,flush=True)
  (ROOT/'validation/motion.json').write_text(json.dumps({'source_sha256':hashlib.sha256(CAD.read_bytes()).hexdigest(),'dependencies_sha256':{n:hashlib.sha256((R/'cad'/n).read_bytes()).hexdigest() for n in ['hallacaitor.scad','modular.scad']},'method':'sampled OpenSCAD intersections; planar seating contacts distinguished; no load/friction/food simulation','results':rows},indent=2)+'\n')
  if not all(r['passed'] for r in rows):raise SystemExit('Inspect failed intersections')
if __name__=='__main__':main()

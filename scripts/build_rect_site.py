#!/usr/bin/env python3
"""Package the recovered Rect 0.4 manual and printable kit without external dependencies."""
from pathlib import Path
import json,shutil,zipfile
R=Path(__file__).resolve().parents[1];D=R/'designs/v04'
def build(out):
 target=out/'rect';target.mkdir(exist_ok=True)
 for f in (R/'web/rect').iterdir():
  if f.suffix in ['.html','.css']:shutil.copyfile(f,target/f.name)
 shutil.copytree(D/'assets',target/'assets',dirs_exist_ok=True)
 shutil.copytree(D/'stl',target/'stl',dirs_exist_ok=True)
 m=json.loads((D/'parts.json').read_text())
 files=[R/'LICENSE',*[R/'cad'/n for n in ['rectangular.scad','hallacaitor.scad','modular.scad']],*D.glob('*.md'),D/'parts.json',*D.glob('stl/*.stl'),*D.glob('validation/*.json'),*[p for p in (D/'assets').rglob('*') if p.is_file()],R/'scripts/rect_v04.py',R/'scripts/mesh.py']
 files += [(D/x['file']).resolve() for x in m['reused_parts']]
 with zipfile.ZipFile(target/'Hallacaitor_Rect_v04.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(set(files)):z.write(f,f.relative_to(R))

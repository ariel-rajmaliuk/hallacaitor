#!/usr/bin/env python3
"""Validate every manifest part, dimensions, topology, document links and reports."""
import argparse, hashlib, json, re
from pathlib import Path
from mesh import audit
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory',type=Path,default=ROOT/'stl')
    ap.add_argument('--report',type=Path,default=ROOT/'docs/validation/geometry.json')
    ap.add_argument('--compare',type=Path)
    a=ap.parse_args();manifest=json.loads((ROOT/'config/parts.json').read_text());rows=[]
    for p in manifest['parts']:
        path=a.directory/f"{p['name']}.stl";r=audit(path)
        assert r['nonmanifold_edges']==r['orientation_errors']==r['degenerate_triangles']==0,(p['name'],r)
        assert r['components']==1 and r['volume_cm3']>0,(p['name'],r)
        assert all(0<x<=b for x,b in zip(r['bbox_mm'],manifest['bed_mm'])),(p['name'],r)
        assert abs(r['min_z_mm'])<.001,(p['name'],r)
        rows.append(dict(name=p['name'],sku=p['sku'],sha256=sha(path),**r))
    report=dict(version=manifest['version'],cad_sha256=sha(ROOT/'cad/hallacaitor.scad'),manifest_sha256=sha(ROOT/'config/parts.json'),method='STL vertices welded at 0.0001 mm; directed/undirected edge and component audit',parts=rows)
    if a.compare:
        prev=json.loads(a.compare.read_text());prev={p['name']:p for p in prev['parts']}
        for r in rows:
            q=prev[r['name']]
            assert max(abs(x-y) for x,y in zip(r['bbox_mm'],q['bbox_mm']))<.01,r['name']
            assert abs(r['volume_cm3']-q['volume_cm3'])/q['volume_cm3']<.001,r['name']
    # Resolve repo-relative Markdown links, including anchors and percent-encoded file paths.
    from urllib.parse import unquote
    for md in [*ROOT.glob('*.md'),*ROOT.glob('docs/**/*.md')]:
        for target in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)',md.read_text()):
            if ':' in target or target.startswith('#'):continue
            target=unquote(target.split('#')[0])
            if target:assert (md.parent/target).exists(),f'Broken link: {md.relative_to(ROOT)} -> {target}'
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n')
    print(f"PASS: {len(rows)} single-component, oriented, closed meshes; bed fit; local Markdown links.")
if __name__=='__main__':main()

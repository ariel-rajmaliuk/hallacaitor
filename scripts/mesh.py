"""Minimal STL reader and topology audit. Standard library, mm and mm^3."""
from __future__ import annotations
import collections, math, re, struct
from pathlib import Path

def read_stl(path):
    data=Path(path).read_bytes()
    if len(data)>=84 and len(data)==84+50*struct.unpack_from('<I',data,80)[0]:
        return [tuple(tuple(t[3+3*j:6+3*j]) for j in range(3)) for t in struct.iter_unpack('<12fH',data[84:])]
    nums=re.findall(rb'vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)',data)
    verts=[tuple(map(float,p)) for p in nums]
    if not verts or len(verts)%3:raise ValueError(f'Not a valid STL: {path}')
    return [tuple(verts[i:i+3]) for i in range(0,len(verts),3)]

def audit(path):
    tris=read_stl(path);vertices={};faces=[];edges=collections.defaultdict(list);volume=0;area=0
    lo=[math.inf]*3;hi=[-math.inf]*3;degenerate=0
    for ti,tri in enumerate(tris):
        ids=[]
        for p in tri:
            if not all(math.isfinite(x) for x in p):raise ValueError('Non-finite vertex')
            key=tuple(round(x,4) for x in p)
            if key not in vertices:vertices[key]=len(vertices)
            ids.append(vertices[key])
            for a in range(3):lo[a]=min(lo[a],p[a]);hi[a]=max(hi[a],p[a])
        faces.append(ids)
        for i in range(3):
            a,b=ids[i],ids[(i+1)%3];edges[tuple(sorted((a,b)))].append((ti,a,b))
        a,b,c=tri
        u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        ar=math.sqrt(sum(x*x for x in cross))/2;area+=ar
        if ar<1e-8 or len(set(ids))<3:degenerate+=1
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    parent=list(range(len(tris)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    orientation=0
    for es in edges.values():
        for other in es[1:]:parent[find(other[0])]=find(es[0][0])
        if len(es)==2 and es[0][1:]==es[1][1:]:orientation+=1
    return dict(triangles=len(tris),vertices=len(vertices),nonmanifold_edges=sum(len(x)!=2 for x in edges.values()),orientation_errors=orientation,degenerate_triangles=degenerate,components=len({find(i) for i in range(len(tris))}),volume_cm3=round(volume/1000,6),surface_cm2=round(area/100,4),bbox_mm=[round(hi[i]-lo[i],4) for i in range(3)],min_z_mm=round(lo[2],4))

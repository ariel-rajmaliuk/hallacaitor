#!/usr/bin/env python3
"""Build a portable, dependency-free public manual, with one page for each STL."""
import argparse,csv,html,json,math,re,shutil,unicodedata
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parents[1];esc=html.escape
NAV=[('start','Empezar'),('layouts','Dos configuraciones'),('assembly','Montaje'),('use','Uso paso a paso'),('printing','Impresión'),('parts','Piezas y STL'),('calculator','Calculadora'),('care','Limpieza y alimentos'),('troubleshooting','Problemas'),('research','Investigación y fuentes')]
REPO='https://github.com/ariel-rajmaliuk/hallacaitor'
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=R/'build/site');a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 m=json.loads((R/'config/parts.json').read_text());stations=json.loads((R/'config/stations.json').read_text());geo={p['name']:p for p in json.loads((R/'docs/validation/geometry.json').read_text())['parts']};content=json.loads((R/'web/content.json').read_text());refs=json.loads((R/'config/references.json').read_text())
 for f in (R/'docs/assets/v3').glob('*.png'):
  raw=f.read_bytes();assert len(raw)>24 and raw[:8]==b'\x89PNG\r\n\x1a\n' and raw[12:16]==b'IHDR',f'Invalid PNG: {f}'
 shutil.copytree(R/'docs/assets/v3',out/'assets',dirs_exist_ok=True);shutil.copytree(R/'stl',out/'stl',dirs_exist_ok=True)
 for f in ['style.css','app.js']:shutil.copyfile(R/'web'/f,out/f)
 shutil.copyfile(R/'LICENSE',out/'LICENSE.txt');(out/'downloads').mkdir(exist_ok=True)
 for f in (R/'docs/manual').glob('*.pdf'):shutil.copyfile(f,out/'downloads'/f.name)
 def page(name,title,body,sidebar=False,prefix=''):
  nav=''.join(f'<a href="{prefix}{n}.html"'+(' aria-current="page"' if n==name else '')+f'>{t}</a>' for n,t in NAV)
  inner=f'<div class="doc-layout"><aside class="sidebar" aria-label="Manual">{nav}</aside><article class="article">{body}</article></div>' if sidebar else body
  (out/(name+'.html')).parent.mkdir(parents=True,exist_ok=True)
  (out/(name+'.html')).write_text(f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Hallacaitor</title><meta name="description" content="Manual abierto de Hallacaitor: estación mecánica imprimible para hallacas. Montaje, uso, impresión y catálogo ilustrado."><meta name="theme-color" content="#203e35"><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}app.js" defer></script></head><body><a class="skip" href="#main">Ir al contenido</a><header><div class="bar"><a class="brand" href="{prefix}index.html">HALLACA<span>ITOR</span></a><span class="badge">0.3 · CAD alpha</span><nav aria-label="Principal"><a href="{prefix}start.html">Empezar</a><a href="{prefix}layouts.html">Configuraciones</a><a href="{prefix}parts.html">Piezas</a><a href="{REPO}">GitHub ↗</a></nav></div></header><main id="main" class="wrap">{inner}</main><footer><div class="footer-in"><span>Hallacaitor · Ariel Rajmaliuk · <a href="{prefix}LICENSE.txt">MIT</a> · Diseño abierto, hardware imprimible.</span><span><a href="{prefix}research.html">Fuentes y límites</a> · <a href="{REPO}/issues">Reportar un problema ↗</a></span></div></footer></body></html>''')
 def image(f,caption='Ilustración propia. CAD o esquema; no es una fotografía de ensayo físico.'):
  return f'<figure><img src="assets/{f}" alt="{esc(caption)}" loading="lazy" width="1100" height="680"><figcaption class="caption">{esc(caption)}</figcaption></figure>'
 def layout_hub():
  z=stations['layouts']['hub']['zones'];s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620" width="1000" height="620"><rect width="1000" height="620" fill="#f6f3ec"/><g font-family="Arial,sans-serif" fill="#203e35"><text x="60" y="48" font-size="28" font-weight="bold">Mesa única · 800 × 400 mm</text>'
  for r in z:
   x=60+r['x'];y=90+400-r['y']-r['h'];s+=f'<rect x="{x}" y="{y}" width="{r["w"]}" height="{r["h"]}" rx="8" fill="{r["color"]}" opacity=".3" stroke="#203e35"/><text x="{x+12}" y="{y+30}" font-size="15" font-weight="bold">{esc(r["name"])}</text>'
  for x in [260,460,660]:s+=f'<path d="M{x} 90V490" stroke="#203e35" stroke-dasharray="5 5"/>'
  s+='<path d="M60 290H860" stroke="#203e35" stroke-dasharray="5 5"/><text x="60" y="540" font-size="18">8 baldosas de 200 mm · 20 llaves · alas sobresalen del contorno</text><text x="60" y="575" font-size="16">Preparar / extender a la izquierda; trasladar la hoja al plegador con ambas manos.</text></g></svg>'
  (out/'assets/layout-hub.svg').write_text(s)
  s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 680" width="1000" height="680"><rect width="1000" height="680" fill="#f6f3ec"/><g font-family="Arial,sans-serif" fill="#203e35"><text x="40" y="45" font-size="28" font-weight="bold">Estaciones repartidas · 9 baldosas en total</text>'
  zones=[(40,100,360,360,'#d7a52c','S1 / S2 · 400 × 400'),(450,100,150,150,'#b96143','S3 · guiso'),(640,100,150,150,'#8063a5','S4 · vasos'),(830,100,150,150,'#8063a5','S4 · volcar'),(450,310,150,150,'#4e81a0','S5 · plegar'),(640,310,150,150,'#ce776c','S6 · atar')]
  for x,y,w,h,c,t in zones:s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}" opacity=".3" stroke="#203e35"/><text x="{x+10}" y="{y+28}" font-size="15" font-weight="bold">{esc(t)}</text>'
  s+='<path d="M220 100V460M40 280H400" stroke="#203e35" stroke-dasharray="5 5"/><text x="40" y="540" font-size="19">3 personas: hoja/masa · relleno/adornos · plegado/pabilo</text><text x="40" y="578" font-size="19">6 personas: una función por persona; duplicar módulos por ingrediente.</text><text x="40" y="620" font-size="16">Esquema de distribución. Separación entre puestos libre; no es una cota total.</text></g></svg>'
  (out/'assets/layout-team.svg').write_text(s)
 layout_hub()
 # Keep original layout drawings in the source repository too.
 for f in ['layout-hub.svg','layout-team.svg']:shutil.copyfile(out/'assets'/f,R/'docs/assets/v3'/f)
 stationcards=''.join(f'<div class="station" style="--station:{s["color"]}"><span>{s["id"]}</span><strong>{s["name"]}</strong><span>{esc(s["purpose"])}</span></div>' for s in stations['stations'])
 page('index','Menos improvisación. Más hallacas.',f'''<div class="hero"><div><div class="eyebrow">Diseño abierto / 100% mecánico</div><h1>La hallacada,<br>bien organizada.</h1><p class="lead">Una mesa para hacerlo todo. O estaciones para compartir el trabajo. Piezas que imprimís, combinás y guardás.</p><div class="actions"><a class="button" href="start.html">Empezar paso a paso →</a><a class="button secondary" href="layouts.html">Ver las dos formas</a></div><p class="small">Sin motores ni herrajes comprados. Masa, hoja, ingredientes y pabilo; cada etapa con su ayuda manual.</p></div><figure class="hero-visual"><img src="assets/family.png" alt="Render del plegador familiar con dos alas elevadas, ejes y pasadores" width="1200" height="740"><figcaption>Piezas reales del CAD · Familiar 0.3</figcaption></figure></div><div class="notice"><strong>Prototipo sin fabricar.</strong> Hay 61 tipos de STL y comprobaciones digitales. Todavía no hay ensayos físicos, velocidad demostrada ni validación alimentaria. El cierre y el nudo se hacen a mano.</div><div class="station-line">{stationcards}</div><div class="section-head"><h2>Elegí cómo se arma tu mesa.</h2><a href="layouts.html">Comparar configuraciones →</a></div><div class="grid two"><article class="card"><img src="assets/layout-hub.svg" alt="Plano de mesa única de ocho baldosas" width="1000" height="620"><div class="card-body"><div class="eyebrow">01 / Mesa única</div><h3>Todo a mano, en un lugar.</h3><p>800 × 400 mm. Hoja y rodillo a la izquierda; ingredientes, plegado y atado a la derecha. Una o dos personas.</p><a href="layouts.html">Ver armado y cantidades →</a></div></article><article class="card"><img src="assets/layout-team.svg" alt="Estaciones separadas para producción en equipo" width="1000" height="680"><div class="card-body"><div class="eyebrow">02 / En equipo</div><h3>Un paso por estación.</h3><p>Repartí módulos entre personas. Duplicá el puesto de un ingrediente. El mismo Dock, colores e identificadores.</p><a href="layouts.html">Organizar el equipo →</a></div></article></div><div class="section-head"><h2>De la primera pieza al primer ensayo.</h2></div><div class="grid">'''+''.join(f'<article class="card"><img src="assets/{f}" alt="{t}" loading="lazy" width="520" height="380"><div class="card-body"><h3>{t}</h3><p>{d}</p><a href="{link}.html">Abrir guía →</a></div></article>' for f,t,d,link in [('wide.png','Imprimí y montá','Cupones, tolerancias, orientaciones y montaje de los conjuntos.','printing'),('use-4.png','Seguí el proceso','Cerrar masa, envolver hoja, reforzar y atar. Un dibujo por paso.','use'),('tipper_cup.png','Cada pieza, explicada','Imagen, medidas, función, cantidad y STL; catálogo con búsqueda.','parts')])+f'</div><div class="actions"><a href="{REPO}" class="button secondary">Ver fuentes y contribuir en GitHub ↗</a><a href="downloads/Hallacaitor_v03.pdf">Descargar manual PDF ↓</a><a href="research.html">Qué investigamos y qué falta comprobar →</a></div>')
 for key,doc in content.items():
  body=f'<div class="eyebrow">Manual abierto / {key}</div><h1>{esc(doc["title"])}</h1><p class="lead">{esc(doc["intro"])}</p><div class="actions"><button id="print">Imprimir guía</button><button class="button secondary" id="reset-checks">Reiniciar lista</button></div>'
  for i,s in enumerate(doc['sections']):
   body+=f'<section id="paso-{i+1}"><h2>{esc(s["title"])}</h2><p>{esc(s["text"])}</p>'
   if s.get('image'):body+=image(s['image'],s['title']+' · Ilustración propia del diseño o proceso.')
   if key in ['start','assembly','use','printing']:body+=f'<label class="stepcheck"><input type="checkbox" data-check="{key}-{i}"> Leído / comprobado en mi montaje</label>'
   body+='</section>'
  if key=='research':
   body+='<section><h2>Fuentes primarias y alcance</h2><p>Consultadas para esta revisión. No se copian recetas, fotografías ni CAD de terceros. Las fuentes enlazadas conservan sus derechos.</p><div class="table-wrap"><table><thead><tr><th>Fuente</th><th>Uso y límite</th></tr></thead><tbody>'+''.join(f'<tr><td><a href="{esc(r["url"])}">{esc(r["name"])}</a></td><td>{esc(r["used"])}</td></tr>' for r in refs)+'</tbody></table></div><h3>Verificaciones y ensayos</h3><p><a href="'+REPO+'/tree/main/docs/validation">Informes digitales</a> · <a href="'+REPO+'/blob/main/docs/testing.md">Plan de ensayos</a> · <a href="'+REPO+'/blob/main/examples/bench_log.csv">Registro vacío</a>. Las booleanas muestrean posiciones; no son un análisis continuo ni simulan carga o flexión.</p></section>'
  page(key,doc['title'],body,True)
 # Static catalog remains usable without JavaScript; JS only filters.
 body='<div class="eyebrow">Fabricación / catálogo</div><h1>Cada pieza tiene su lugar.</h1><p class="lead">61 tipos de pieza, con imagen real del STL, orientación, medidas y descarga. Los kits Familiar reutilizan algunas piezas Compact; mirá la cantidad antes de imprimir.</p><div class="toolbar"><label class="field">Buscar pieza<input type="search" id="search" placeholder="Nombre, código o función…"></label><label class="field">Configuración<select id="kit"><option value="all">Todas las piezas</option><option value="hub">Mesa única / Familiar</option><option value="team">Equipo / Familiar</option><option value="minimum">Mínimo / Compact</option><option value="standard">Estándar / Compact</option></select></label><span id="count" aria-live="polite">61 tipos de pieza</span></div><div class="actions"><a class="button secondary" href="downloads/bom-v3.csv" download>Lista de materiales CSV</a><a href="'+REPO+'/tree/main/stl">Carpeta STL en GitHub ↗</a></div><div class="grid">'
 csvrows=[]
 for p in m['parts']:
  n=p['name'];g=geo[n];dims=' × '.join(f'{v:g}' for v in g['bbox_mm']);q=p['quantities'];quant=' · '.join(f'{k}: {q[k]}' for k in ['hub','team','minimum','standard'])
  body+=f'<article class="card" data-part="{n}" data-search="{esc(norm(p["label"]+" "+p["sku"]+" "+n+" "+p["purpose"]),quote=True)}" '+ ' '.join(f'data-{k}="{q[k]}"' for k in ['hub','team','minimum','standard'])+f'><a href="parts/{n}.html"><img src="assets/{n}.png" alt="{esc(p["label"])} en orientación de impresión" loading="lazy" width="520" height="380"></a><div class="card-body"><div class="meta">{p["sku"]} · {dims} mm</div><h3 class="part-title"><a class="title" href="parts/{n}.html">{esc(p["label"])}</a></h3><p>Mesa: {q["hub"]} · Equipo: {q["team"]}</p><a href="stl/{n}.stl" download>Descargar STL ↓</a></div></article>'
  guide=p['guide'].lower()
  guideurl='../assembly.html'
  if 'uso paso' in guide:
   match=re.search(r'uso paso (\d+)',guide)
   if match:guideurl='../use.html#paso-'+match.group(1)
  elif 'archivo compact' in guide or 'compatibilidad compact' in guide:guideurl=REPO+'/blob/main/docs/compact-assembly.md'
  elif guide.startswith('inicio'):guideurl='../start.html#paso-2'
  elif guide.startswith('dock'):guideurl='../assembly.html#paso-1'
  elif guide.startswith('rodillo'):guideurl='../assembly.html#paso-4'
  elif guide.startswith('plegador'):guideurl='../assembly.html#paso-7'
  elif guide.startswith('ingredientes'):guideurl='../assembly.html#paso-9'
  elif guide.startswith('volcador'):guideurl='../assembly.html#paso-10'
  elif guide.startswith('guardado'):guideurl='../assembly.html#paso-14'
  d=f'<p><a href="../parts.html">← Catálogo</a></p><div class="part-detail"><figure><img src="../assets/{n}.png" alt="{esc(p["label"])}: vista del STL exportado" width="520" height="380"><figcaption class="caption">Orientación de exportación. Superficie inferior en z=0; revisar soportes y brim.</figcaption></figure><div><div class="eyebrow">{p["sku"]} / {p["print_profile"]}</div><h1>{esc(p["label"])}</h1><p>{esc(p["purpose"])}</p><div class="actions"><a class="button" href="../stl/{n}.stl" download>Descargar STL ↓</a><a href="{REPO}/blob/main/{p["source"]}">Fuente CAD ↗</a></div><dl class="specs"><dt>Caja de impresión</dt><dd>{dims} mm</dd><dt>Orientación</dt><dd>{esc(p["orientation"])}</dd><dt>Soportes</dt><dd>{esc(p["supports"])}</dd><dt>Mesa única</dt><dd>{q["hub"]}</dd><dt>Equipo</dt><dd>{q["team"]}</dd><dt>Compact mínimo / estándar</dt><dd>{q["minimum"]} / {q["standard"]}</dd><dt>Archivo</dt><dd><code>{n}.stl</code></dd></dl></div></div><h2>Cómo se usa</h2><p>{esc(p["use"])}</p><p>Referencia de montaje: {esc(p["guide"])}. <a href="{guideurl}">Abrir guía ilustrada</a>.</p><div class="notice">Perfil propuesto: capa 0,20 mm, boquilla 0,4 mm. {"5–6 perímetros y 40–60% de relleno para piezas mecánicas." if p["print_profile"]=="mecánica" else "4 perímetros y 5 capas superior/inferior como punto de partida."} Calibrar con muestras antes de fabricar el conjunto. No hay impresión física validada.</div><p><a href="../printing.html">Guía técnica completa</a> · <a href="../care.html">Contacto alimentario y limpieza</a></p>'
  page('parts/'+n,p['label'],d,prefix='../');csvrows.append({'sku':p['sku'],'name':n,'label':p['label'],'hub':q['hub'],'team':q['team'],'compact_minimum':q['minimum'],'compact_standard':q['standard'],'dimensions_mm':dims,'orientation':p['orientation'],'supports':p['supports']})
 body+='</div><p id="empty" class="empty" hidden>No hay piezas que coincidan. Borrá la búsqueda o elegí otra configuración.</p>';page('parts','Catálogo de piezas',body)
 with (out/'downloads/bom-v3.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=csvrows[0].keys());w.writeheader();w.writerows(csvrows)
 shutil.copyfile(out/'downloads/bom-v3.csv',R/'docs/bom-v3.csv')
 page('calculator','Porción y diámetro','''<div class="eyebrow">Herramienta / geometría</div><h1>Ajustá la porción a tu formato.</h1><p class="lead">El cálculo supone un disco uniforme. No convierte volumen a gramos ni predice el cierre con relleno.</p><div class="calc"><div class="toolbar"><label class="field">Volumen de masa (ml)<input type="number" id="volume" value="80" min="1" max="500" step="1"></label><label class="field">Espesor (mm)<input type="number" id="thickness" value="2.5" min="0.5" max="10" step="0.1"></label><label class="field">Rodillo<select id="format"><option value="family">Familiar · 266 mm útiles</option><option value="compact">Compact · 186 mm útiles</option></select></label></div><p class="result" id="diameter" aria-live="polite">202 mm de diámetro ideal</p><p id="fit">Comprobar tamaño real con masa.</p></div><p>Fórmula: <code>D = √(4000 V / (π t))</code>, V en ml y t en mm. Se deja un margen total de al menos 4 mm antes de las ranuras del rodillo.</p><div class="table-wrap"><table><thead><tr><th>Formato</th><th>Volumen</th><th>Espesor</th><th>Diámetro ideal</th></tr></thead><tbody><tr><td>Familiar</td><td>80 ml</td><td>2,5 mm</td><td>202 mm</td></tr><tr><td>Familiar</td><td>100 ml</td><td>2,5 mm</td><td>226 mm</td></tr><tr><td>Compact</td><td>80 ml</td><td>4 mm</td><td>160 mm</td></tr></tbody></table></div><h2>Pabilo: estimación inicial</h2><p>Para paquete supuesto de 160 × 90 × 35 mm, 3 vueltas por eje y 300 mm de reserva: <code>3 × 2 × (160+35) + 3 × 2 × (90+35) + 300 = 2.220 mm</code>. Empezar con unos 2,4 m, medir sobrante y ajustar. La cantidad de vueltas depende de la técnica y receta.</p><p><a href="use.html">Seguir guía de uso</a> · <a href="parts.html">Elegir piezas</a></p>''',True)
 # Rect architecture and catalog remain separate from legacy Familiar pages.
 from build_rect_site import build as build_rect
 build_rect(out)
 shutil.copyfile(out/'index.html',out/'legacy-v03.html')
 (out/'index.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=rect/index.html"><title>Hallacaitor Rect 0.4</title><h1>Hallacaitor Rect 0.4</h1><p><a href="rect/index.html">Abrir el rediseño rectangular →</a></p><p><a href="legacy-v03.html">Archivo Familiar 0.3</a></p></html>')
 # Validate every local HTML resource. External URLs are retained without network probing.
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ['src','href'] and v:self.links.append(v)
 pages=list(out.rglob('*.html'))
 for p in pages:
  parser=Links();parser.feed(p.read_text())
  for link in parser.links:
   u=urlsplit(link)
   if u.scheme or u.netloc or not u.path:continue
   assert (p.parent/unquote(u.path)).exists(),f'{p}: missing {link}'
 for p in m['parts']:
  assert (out/f'parts/{p["name"]}.html').exists() and (out/f'assets/{p["name"]}.png').exists()
 (out/'.nojekyll').touch()
 print(f'PASS: {len(pages)} HTML pages; {len(m["parts"])} illustrated part pages; all local href/src targets exist.')
if __name__=='__main__':main()

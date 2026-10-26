#!/usr/bin/env python3
"""Offline companion to the full web manual. Images are original CAD renders."""
from pathlib import Path
import json,html,os
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/v3';O=R/'docs/manual/Hallacaitor_v03.pdf'
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,str(Path(os.environ.get('HALLACAITOR_FONT_DIR','/usr/share/fonts/truetype/dejavu'))/f)))
s=getSampleStyleSheet();s['BodyText'].fontName='DV';s['BodyText'].fontSize=8.8;s['BodyText'].leading=12;s['BodyText'].spaceAfter=8
for k,z in [('Heading1',25),('Heading2',14)]:s[k].fontName='DVB';s[k].fontSize=z;s[k].leading=z*1.2;s[k].textColor=colors.HexColor('#203e35');s[k].spaceAfter=10
s.add(ParagraphStyle(name='fine',fontName='DV',fontSize=7.5,leading=10,textColor=colors.HexColor('#5d7067')))
story=[];E=lambda t:html.escape(t).replace('–','-').replace('—','-')
def p(t,style='BodyText'):story.append(Paragraph(E(t),s[style]))
def img(f,w=490):
 from PIL import Image as PI
 with PI.open(A/f) as im:h=w*im.height/im.width
 story.append(Image(str(A/f),width=w,height=h));story.append(Spacer(1,8))
def chapter(title):
 if story:story.append(PageBreak())
 p('HALLACAITOR / FAMILIAR 0.3 / CAD ALPHA','fine');p(title,'Heading1')
def secs(rows,illustrations=()):
 for i,r in enumerate(rows):
  story.append(KeepTogether([Paragraph(E(r['title']),s['Heading2']),Paragraph(E(r['text']),s['BodyText'])]))
  if i in illustrations and r.get('image','').endswith('.png'):img(r['image'],330)
c=json.loads((R/'web/content.json').read_text())
chapter('Una mesa. O todo un equipo.');p('Manual abierto de montaje, impresión y uso. Proyecto iniciado por Ariel Rajmaliuk. Hardware permanente imprimible y accionamiento manual.');img('family.png');p('Prototipo digital: todavía sin fabricar ni probar con comida. El plegado final y el nudo son manuales. Las comprobaciones digitales no validan resistencia, limpieza, inocuidad ni velocidad.');p('Manual completo y 61 fichas ilustradas: https://hallacaitor-manual.rajmaliuk.chatgpt.site');p('Fuentes y STL: https://github.com/ariel-rajmaliuk/hallacaitor');p('MIT. Fotografías, recetas y diseños de terceros no se redistribuyen.')
chapter('1 / Antes de imprimir');secs(c['start']['sections'])
chapter('2 / Dos configuraciones');secs(c['layouts']['sections'])
for title,rows,pics in [('3 / Dock200',c['assembly']['sections'][:3],(2,)),('4 / Rodillo familiar',c['assembly']['sections'][3:6],(0,2)),('5 / Plegador',c['assembly']['sections'][6:8],(0,)),('6 / Ingredientes y volcador',c['assembly']['sections'][8:12],(2,)),('7 / Atado y guardado',c['assembly']['sections'][12:],(0,))]:chapter(title);secs(rows,pics)
for k in range(0,7,2):chapter('8 / Uso paso a paso');secs(c['use']['sections'][k:k+2],tuple(range(2)))
for key,title in [('printing','9 / Impresión y ajuste'),('care','10 / Higiene y cuidado'),('troubleshooting','11 / Resolver problemas'),('research','12 / Investigación')]:chapter(title);p(c[key]['intro']);secs(c[key]['sections'])
chapter('13 / Fuentes enlazadas')
for r in json.loads((R/'config/references.json').read_text()):
 story.append(KeepTogether([Paragraph('<b>'+E(r['name'])+'</b>',s['BodyText']),Paragraph(E(r['used']),s['fine']),Paragraph(E(r['url']),s['fine']),Spacer(1,12)]))
chapter('14 / Lista de piezas')
m=json.loads((R/'config/parts.json').read_text());p('Cantidades de ejemplares de referencia. Mesa: kit hub. Equipo: kit team. Agregar un módulo completo por ingrediente adicional; no confundir tipos de STL con número de impresiones.')
rows=[['Código','Archivo sin .stl','Mesa','Equipo']]+[[r['sku'],r['name'],str(r['quantities']['hub']),str(r['quantities']['team'])] for r in m['parts']]
data=[[Paragraph(E(t),s['fine']) for t in row] for row in rows];t=Table(data,colWidths=[48,330,55,55],repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6ecdf')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f3ec')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));story.append(t)
def footer(c,d):
 c.setFont('DV',7);c.setFillColor(colors.HexColor('#5d7067'));c.drawString(48,25,'HALLACAITOR / MIT / Familiar 0.3 / sin ensayo físico');c.drawRightString(A4[0]-48,25,str(d.page))
SimpleDocTemplate(str(O),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=45,title='Hallacaitor Familiar 0.3 - Manual abierto',author='Ariel Rajmaliuk').build(story,onFirstPage=footer,onLaterPages=footer)
print(O)

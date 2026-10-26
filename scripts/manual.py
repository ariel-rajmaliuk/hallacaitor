#!/usr/bin/env python3
"""Create the illustrated manual and exact-scale four-page leaf template."""
from pathlib import Path
import json,math,os
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,Flowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/manual';OUT.mkdir(parents=True,exist_ok=True)
FD=Path(os.environ.get('HALLACAITOR_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
pdfmetrics.registerFont(TTFont('DV',str(FD/'DejaVuSans.ttf')));pdfmetrics.registerFont(TTFont('DV-B',str(FD/'DejaVuSans-Bold.ttf')))
G=colors.HexColor('#294F45');B=colors.HexColor('#F4F1E9');M=colors.HexColor('#64756D');A=colors.HexColor('#DEAD68')
st=getSampleStyleSheet()
st['BodyText'].fontName='DV';st['BodyText'].fontSize=9.2;st['BodyText'].leading=14;st['BodyText'].spaceAfter=8
for name,size,leading in [('Heading1',25,31),('Heading2',14,19)]:
 st[name].fontName='DV-B';st[name].fontSize=size;st[name].leading=leading;st[name].textColor=G;st[name].spaceAfter=9
st.add(ParagraphStyle(name='SmallH',fontName='DV',fontSize=7.7,leading=10.7,textColor=M))
story=[]
def p(t,style='BodyText'):story.append(Paragraph(t,st[style]))
def title(n,t):p('HALLACAITOR / '+n,'SmallH');p(t,'Heading1');story.append(Spacer(1,8))
def new():story.append(PageBreak())
def table(rows,widths,small=False):
 data=[[Paragraph(str(c),st['SmallH'] if small else st['BodyText']) for c in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E4E9DF')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F5F0')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,0),.5,G)]));story.append(t);story.append(Spacer(1,9))
def image(name,w):
 from PIL import Image as PImage
 with PImage.open(ROOT/'docs/assets'/name) as im:h=w*im.height/im.width
 story.append(Image(str(ROOT/'docs/assets'/name),width=w,height=h))

title('v0.2.0 / 25 OCT 2026','Hallacas, con una mesa<br/>mejor preparada.')
p('Estación manual, mecánica y con todas sus piezas permanentes imprimibles. CAD editable, útiles desmontables y un proceso de prueba por etapas.','Heading2')
image('hero.png',500)
p('<b>Prototipo CAD alpha, sin ensayo físico ni validación alimentaria.</b> Toda prestación práctica queda por comprobar. No se promete un rendimiento ni un número de hallacas por hora.')
p('Comida, hojas, cuerda y barreras alimentarias son consumibles externos. No cocina, recorta ni anuda automáticamente.','SmallH')
p('Fuente y actualizaciones: <link href="https://github.com/ariel-rajmaliuk/hallacaitor" color="#294F45">github.com/ariel-rajmaliuk/hallacaitor</link> · MIT · Copyright (c) 2026 Ariel','SmallH')
new();title('01 / EMPEZAR','Fabricar poco. Comprobar primero.')
p('El kit mínimo prueba el plegado, las posiciones de las alas y el paso del pabilo. No hace falta imprimir toda la estación para descubrir un problema de encaje o de hoja.')
table([['SKU','Pieza','Cant.'],['H01','Base de plegado y atado',1],['H02N / H02S','Ala norte y ala sur; una de cada archivo',2],['H03','Eje de bisagra',2],['H04','Chaveta; dos instaladas y una de repuesto',3],['H05','Pasador de posición',2],['T01 / T03','Aguja roma y pala de extremos',2],['C01 / C02','Cupones de diámetros y chavetas',2]],[95,345,60])
p('<b>Total: 14 piezas.</b> Referencia de impresora: 220 x 220 x 250 mm. Material estructural inicial PETG. Boquilla 0,4 mm, capa 0,2 mm, cuatro perímetros y relleno 20-30% como punto de partida; no son parámetros físicamente validados.')
p('1. Calibrar','Heading2');p('Las columnas del cupón de diámetros tienen holguras de 0,3 / 0,4 / 0,5 / 0,6 mm; filas para ejes de 4 / 8 / 12 mm. Probar un segmento corto de cada eje. El cupón de chavetas tiene tres huecos: 2,8x3,4 / 2,9x3,5 / 3,0x3,6 mm. No forzar el encaje.')
p('2. Respetar orientaciones','Heading2');p('Alas con la cara amplia sobre cama, como en STL. Ejes tumbados sobre su cara plana; el del rodillo ya va en diagonal. Chavetas con brim pequeño. El cuerpo del rodillo es vertical de 200 mm. Revisar soportes locales bajo orejas y en agujeros. La tapa opcional se invierte en el laminador.')
p('3. Probar sin comida','Heading2');p('Primero movimiento en vacío y paquetes de papel; después hojas reales sin alimento. Una pieza que encaja a golpes o que se agrieta no pasa la prueba. El siguiente paso depende del resultado físico, no del aspecto del render.')
new();title('02 / PLEGADOR','Dos alas de distinta mano')
image('exploded.png',500)
p('1. Apoyar la base con canales arriba y orejas a la derecha. Colocar H02N y H02S en sus lados: los brazos de índice deben quedar junto a las orejas, en el mismo extremo derecho.')
p('2. Alternar los nudillos e introducir un eje desde la izquierda. La cabeza retiene un extremo; una chaveta transversal en la punta retiene el otro. Comprobar la chaveta antes de usar y después de varios ciclos.')
p('3. Sostener el asa, alinear una posición y colocar el pasador corto desde la derecha. <b>Quitar el pasador antes de mover el ala.</b> Reinsertarlo para liberar una mano. No forzar la coincidencia de agujeros ni pasar de 100°.')
p('0°: presentación abierta. 70°: toma de hoja. 100°: acercamiento asistido. El doblez central sigue siendo manual; las alas no necesitan tocarse. Dedos fuera de bisagras y pasos de retención.','SmallH')
new();title('03 / EXTENDIDO','Rodillo retenido y tabla plana')
p('El eje pasante captura ambos mangos, el cuerpo y la arandela. Una chaveta evita que las piezas se salgan axialmente. Los aros abiertos se montan en ranuras y se cambian por pares iguales.')
class Roller(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=500;self.height=165
 def draw(self):
  c=self.canv;s=1.7;xo=20;cy=90;c.setFillColor(colors.HexColor('#9AB4A3'));c.rect(xo,cy-3,264*s,6,fill=1,stroke=0)
  c.setFillColor(A);c.rect(xo+28.6*s,cy-20,200*s,40,fill=1,stroke=0)
  c.setFillColor(G)
  for x in [3.8,229.4]:c.roundRect(xo+x*s,cy-15,24*s,30,4,fill=1,stroke=0)
  c.setFillColor(colors.HexColor('#C86744'))
  for x in [29.8,221.8]:c.rect(xo+x*s,cy-24,5.6*s,48,fill=1,stroke=0)
  c.setStrokeColor(M);c.line(xo,35,xo+264*s,35);c.setFont('DV',9);c.setFillColor(M);c.drawString(xo,17,'Eje 264 mm; cuerpo 200 mm; ancho útil 186 mm. Esquema longitudinal.')
story.append(Roller())
p('Orden de montaje','Heading2');p('Cabeza de eje → mango → cuerpo con dos aros → segundo mango → arandela → chaveta. El cuerpo debe girar sin atascar mientras se sostienen los mangos. Los aros parten de 0,2 mm de interferencia diametral en sus asientos; la flexión del aro abierto debe comprobarse en material real.')
p('Tabla de 360 x 360 mm','Heading2');p('Montar cuatro baldosas de 180 mm directamente en la mesa y ocho llaves mariposa por arriba de las juntas interiores. No hay pies ni tornillos. Las llaves sujetan en el plano y quedan 0,2 mm por debajo de la cara de trabajo, pero no retienen contra levantamiento: desarmar o transportar sosteniendo todo desde abajo.')
p('Sobre la hoja','Heading2');p('Masa sobre la hoja aceitada y barrera alimentaria por encima. Los dos aros deben rodar sobre una superficie de referencia equivalente: arrugas o un aro fuera de la hoja cambian el resultado. Medir espesor real; el número del aro no lo garantiza por sí solo.')
new();title('04 / DOSIFICAR','Volumen y espesor van juntos')
image('sizing.png',500)
table([['Masa nominal','Espesor','Disco ideal'],['60 ml','3 mm','159,6 mm'],['80 ml - partida','4 mm','159,6 mm'],['100 ml','5 mm','159,6 mm'],['100 ml - disco mayor','4 mm','178,4 mm']],[190,130,180])
p('Los aros de masa tienen diámetro interior de 60 mm. Alturas útiles: 21,22 / 28,29 / 35,37 mm. Los vasos de guiso tienen diámetro interior de 50 mm y volumen nominal de 40 o 60 ml. El forro resta capacidad y las arrugas afectan el enrasado. No equivalen a gramos fijos.')
p('<b>No combinar 100 ml con 3 mm:</b> el disco ideal de 206 mm no cabe entre los aros. No compensar presionando más fuerte ni dejando que la masa se monte sobre los topes.')
p('Fórmula: D = sqrt(4000 x V / (pi x t)). Geometría ideal, con V en ml y t/D en mm. Densidad, elasticidad y adherencia no están modeladas.','SmallH')
new();title('05 / ENVOLVER','Compact: la hoja manda')
for h,t in [
('Preparar por tandas','Tener masa, guiso, adornos, hojas limpias/flexibles/recortadas, refuerzos, fajas y tramos de pabilo. La receta y el tratamiento de hoja no se automatizan.'),
('Mantener la barrera','Amasar en bolsa cerrada resistente; forrar medidas y recipientes cubriendo también el borde; cubrir el empujador. En el extendido se usa una barrera superior; durante el plegado separa la hoja íntegra. Un filamento PETG no certifica el útil.'),
('Presentar y rellenar','La hoja inicial sugerida es de 350 x 350 mm para un paquete cercano a 140 x 80 x 35 mm. Aceptar que quizá necesite más margen. Servir a mano y dejar masa libre alrededor del guiso.'),
('Elevar y tomar los bordes','Fijar un ala a 70°, tomar la hoja y repetir del otro lado. Si ayuda, pasar a 100°. Juntar primero los bordes de MASA sobre el guiso; luego juntar y doblar la hoja. No tirar contra una hoja pegada.'),
('Cerrar y reforzar','Hacer el doblez central, acomodar extremos con la pala por fuera y poner hoja de refuerzo/faja. Si no alcanza la hoja, usar otra mayor o reducir carga. No comprimir para ocultar una rotura.'),
('Cuidar preparación y limpieza','No colocar impresiones en cocción, caldo/guiso calientes o lavavajillas. Las tapas no son herméticas ni sirven para conservación. Control térmico y cocción van fuera. Si falla una barrera, detener el ensayo alimentario.')]:p(h,'Heading2');p(t)
p('La combinación de barreras, hoja y limpieza necesita validación en las condiciones de uso reales. Sin barreras viables, usar solamente simulantes no destinados a consumo. Fuentes y alcance en docs/food-contact.md.','SmallH')
new();title('06 / PABILO','Seis vueltas, un tramo, nudo manual')
class Tying(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=500;self.height=210
 def draw(self):
  c=self.canv;xo=60;yo=45;s=2;c.setFillColor(colors.HexColor('#9AB4A3'));c.roundRect(xo,yo,190*s,80*s,8,fill=1,stroke=0);c.setFillColor(G);c.roundRect(xo+21*s,yo,140*s,80*s,12,fill=1,stroke=0)
  c.setLineWidth(3);c.setDash(6,4);c.setStrokeColor(A)
  for y in [-25,0,25]:c.line(xo+10*s,yo+(y+40)*s,xo+180*s,yo+(y+40)*s)
  c.setStrokeColor(colors.HexColor('#C86744'))
  for x in [59,91,123]:c.line(xo+x*s,yo-8,xo+x*s,yo+168)
  c.setDash();c.setFillColor(M);c.setFont('DV',9);c.drawString(60,16,'Líneas discontinuas: rutas inferiores. Los retornos se hacen por arriba y fuera del paquete.')
story.append(Tying())
p('1. Reservar una cola corta para el nudo y enhebrar el extremo largo en la aguja roma. Pasar por debajo a y=-25, regresar por arriba y continuar con y=0 e y=25.')
p('2. Sin cortar, cambiar de eje y repetir por x=59,91,123. Cada pasada inferior debe volver por arriba: son tres vueltas por dirección, no seis cuerdas separadas.')
p('3. Acomodar los cambios de canal por fuera, mantener libres las intersecciones, quitar aguja y tensar sin cortar la hoja. Si se traba, levantar y recolocar; nunca punzar.')
p('4. Hacer dos medios nudos de sentido opuesto para formar nudo llano. Levantar el paquete: la cuerda sale por arriba de los canales. Si rodeó una bisagra o la base, desatar y rehacer.')
p('Longitud inicial','Heading2');p('Para 140 x 80 x 35 mm y tres vueltas por eje: 2.040 mm incluyendo 300 mm de reserva. Empezar con unos <b>2,2 m</b> y ajustar desde el sobrante. El medidor da 397,7 mm por vuelta ideal: cinco vueltas son unos 1.989 mm; agregar unos 211 mm con la regla. No hay cuchilla.')
p('Comparar tiempos con el atado habitual. Si la aguja agrega trabajo, usar solo el medidor y atar de forma tradicional. La rapidez todavía no está demostrada.','SmallH')
new();title('07 / COMPROBAR','CAD no es una prueba de cocina')
table([['Comprobado digitalmente','Falta comprobar físicamente'],['Exportación de 32 tipos de STL, un componente y volumen positivo por pieza','Calidad de impresión, encaje, deformación, desgaste y retención'],['Envolventes orientadas compatibles con cama de referencia','Brim, purga y particularidades de cada impresora'],['Muestras de base/ala y ala/ala a 0,10,30,50,70,90,100 grados','Recorrido real, flexión y posiciones independientes'],['Pasos de aguja sin plástico en su ruta; interferencia de aros medida','Hoja, cuerdas, fricción y posible atasco en cruces'],['Restricciones de tamaño y fórmulas de dosis/pabilo','Consistencia de masa, sellado, pérdidas en cocción y tiempos']],[250,250])
p('El ajuste de los aros tiene una pequeña intersección intencional en CAD por su interferencia diametral de 0,2 mm. El control limita su volumen; no simula elasticidad ni afirma que el aro ya se pueda montar en una impresión real.')
p('Plan mínimo','Heading2')
for t in ['A. Cupones y segmentos cortos: giro y entrada sin golpe.','B. Veinte ciclos sin carga: no debe salir una chaveta ni aparecer roce creciente.','C. Diez paquetes simulados: seis vueltas y liberación sin capturar la base.','D. Diez hojas sin comida: observar roturas y margen de cierre.','E. Diez porciones con barrera: peso, diámetro y espesor medidos.','F. Diez hallacas de prueba: registrar fugas después de cocinar fuera de la estación.','G. Diez armados habituales frente a diez asistidos, misma persona y condiciones.']:p(t)
p('La planilla examples/bench_log.csv está vacía: no hay resultados físicos inventados. Cada archivo de validación identifica la fuente y las piezas con hashes. No se hizo FEA ni se establece una carga segura o una productividad garantizada.','SmallH')
new();title('08 / PIEZAS','Tres kits, una fuente')
m=json.loads((ROOT/'config/parts.json').read_text());m['parts']=[x for x in m['parts'] if x['source']=='cad/hallacaitor.scad'];g={r['name']:r for r in json.loads((ROOT/'docs/validation/geometry.json').read_text())['parts']}
rows=[['SKU','Nombre de archivo (sin .stl)','Mín.','Est.','Todo']]
for r in m['parts']:rows.append([r['sku'],r['name'],r['quantities']['minimum'],r['quantities']['standard'],r['quantities']['full']])
table(rows,[55,295,50,50,50],small=True)
p('14 piezas mínimo / 45 estándar / 62 completo. Incluye repuestos de chaveta según kit. Dimensiones y orientaciones detalladas en docs/bom.md y docs/bom.csv; el manifiesto config/parts.json es la fuente de cantidades.','SmallH')
new();title('09 / FUENTES Y CAMBIOS','Abierto para aprender y mejorar')
p('Archivos del proyecto bajo MIT. Podés copiar, modificar, compartir y comercializar conservando los avisos. Las referencias enlazadas mantienen sus propios derechos; no se redistribuyen recetas ni diseños ajenos.')
refs=[('R1 / GOYA - Hallacas venezolanas','https://goya.es/recetas/hallacas-venezolanas','Proceso tradicional de armado y cierre; no respalda medidas ni rendimiento de la máquina.'),('R2 / Prusa - Food safe FDM printing','https://help.prusa3d.com/article/food-safe-fdm-printing_112313','Superficies por capas, aditivos y limitaciones del contacto alimentario.'),('R3 / Prusa - PETG','https://help.prusa3d.com/article/petg_2059','Uso estructural y limitaciones de piezas impresas; no certifica este prototipo.'),('R4 / Prusa - Modeling with 3D printing in mind','https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135','Orientación, puentes y soportes.'),('R5 / USDA - Keep Your Traditions Safe at Your Next Tamalada','https://www.fsis.usda.gov/news-events/news-press-releases/keep-your-traditions-safe-your-next-tamalada','Higiene y control térmico durante la preparación, también menciona hallacas.'),('R6 / OpenSCAD - Documentation','https://openscad.org/documentation.html','Modelo paramétrico y exportación. Los cálculos de cilindros, discos y cuerda son propios de geometría elemental.')]
for h,url,t in refs:p(h,'Heading2');p(f'<link href="{url}" color="#294F45">{t}</link>')
p('Qué sigue','Heading2');p('Primero imprimir y medir el kit mínimo. Después ajustar el manejo de hojas y el paso del pabilo. El README, los STL, planos y scripts deben cambiar juntos cuando cambie la geometría. No mezclar piezas de v0.1 y v0.2.')
p('Consulta de fuentes: 25/10/2026. Guía completa de atribución: docs/references.md. Registrar datos y fotos de ensayos, incluidos fallos, mediante las plantillas de incidencias del repositorio.','SmallH')
def footer(c,d):
 c.setStrokeColor(colors.HexColor('#CCD7CC'));c.line(44,39,551,39);c.setFont('DV',7.5);c.setFillColor(M);c.drawString(44,25,'HALLACAITOR v0.2.0 / CAD alpha / sin ensayo físico');c.drawRightString(551,25,str(d.page))
doc=SimpleDocTemplate(str(OUT/'Hallacaitor_v02.pdf'),pagesize=(595.28,841.89),rightMargin=47,leftMargin=47,topMargin=40,bottomMargin=52,title='Hallacaitor v0.2 - Manual de prototipo',author='Ariel')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
# Four A4 sheets, 180x180 mm working window; 10 mm overlap -> total 350 mm.
c=canvas.Canvas(str(OUT/'Plantilla_hoja_350mm_A4.pdf'),pagesize=(210*mm,297*mm));c.setTitle('Hallacaitor - Plantilla de hoja 350 mm en cuatro A4');c.setAuthor('Ariel')
for row in range(2):
 for col in range(2):
  c.setFillColor(G);c.setFont('DV-B',16);c.drawString(15*mm,278*mm,f'HOJA 350 / cuadrante {row*2+col+1} de 4')
  c.setFont('DV',9);c.setFillColor(M);c.drawString(15*mm,270*mm,'A4 · escala 100% · sin ajustar a página · solape 10 mm')
  c.saveState();c.translate(15*mm,72*mm)
  clip=c.beginPath();clip.rect(0,0,180*mm,180*mm);c.clipPath(clip,stroke=0)
  c.translate(-col*170*mm,-(1-row)*170*mm)
  c.setStrokeColor(colors.HexColor('#CCD7CC'));c.setLineWidth(.35)
  for a in range(0,351,10):c.line(a*mm,0,a*mm,350*mm);c.line(0,a*mm,350*mm,a*mm)
  c.setStrokeColor(G);c.setLineWidth(1.3);c.rect(0,0,350*mm,350*mm)
  c.setDash(5,4);c.setStrokeColor(A);c.circle(175*mm,175*mm,80*mm,stroke=1,fill=0);c.setDash()
  c.setStrokeColor(G);c.line(165*mm,175*mm,185*mm,175*mm);c.line(175*mm,165*mm,175*mm,185*mm)
  c.restoreState()
  c.setLineWidth(.6);c.setStrokeColor(M);c.rect(15*mm,72*mm,180*mm,180*mm)
  c.setFont('DV',8.5);c.setFillColor(M)
  for i,line in enumerate(['Recortar márgenes de unión y superponer cuadrículas 10 mm.', 'Orden: 1 arriba izquierda; 2 arriba derecha; 3 abajo izquierda; 4 abajo derecha.', 'Guía de medida: no es una cuchilla. Papel fuera del contacto con alimentos.', 'Hoja sugerida, no universal. Círculo central de 160 mm: referencia de masa.']):c.drawString(15*mm,(61-i*5)*mm,line)
  c.setStrokeColor(G);c.rect(15*mm,14*mm,50*mm,25*mm);c.setFont('DV',8);c.drawString(70*mm,31*mm,'Este rectángulo debe medir 50 × 25 mm.');c.drawString(70*mm,25*mm,'Comprobar con regla antes de unir las cuatro hojas.');c.drawString(70*mm,19*mm,'Hallacaitor v0.2.0 · MIT · sin ensayo físico')
  c.showPage()
c.save();print('Manual and A4 template ready')

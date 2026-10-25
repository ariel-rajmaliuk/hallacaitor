#!/usr/bin/env python3
"""Render the actual exported meshes with an offline CPU depth buffer; draw original technical diagrams."""
from __future__ import annotations
import csv,html,json,math,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mesh import read_stl,audit
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'docs/assets';DRAW=ROOT/'docs/drawings'
GREEN='#294F45';SAGE='#9AB4A3';GOLD='#DEAD68';ORANGE='#C86744';BG='#F4F1E9';INK='#233D35';MUTED='#64756D'
FONT=Path(os.environ.get('HALLACAITOR_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
def font(size,bold=False):
    p=FONT/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    if not p.exists():raise RuntimeError('Install DejaVu Sans fonts or adjust FONT in illustrate.py')
    return ImageFont.truetype(str(p),size)
def rgb(c):return np.array(tuple(int(c[i:i+2],16) for i in (1,3,5)))/255
M={p.stem:np.array(read_stl(p)) for p in (ROOT/'stl').glob('*.stl')}
def rot(axis,a):
    a=np.radians(a);c,s=np.cos(a),np.sin(a)
    return {'x':np.array([[1,0,0],[0,c,-s],[0,s,c]]),'y':np.array([[c,0,s],[0,1,0],[-s,0,c]]),'z':np.array([[c,-s,0],[s,c,0],[0,0,1]])}[axis]
def tx(v,R=np.eye(3),t=(0,0,0)):return v@R.T+np.array(t)
def wing_n():return tx(M['fold_wing_north']-[0,127,20],rot('x',180))
def wing_s():return tx(M['fold_wing_south']-[0,7,20],rot('x',180))
def shaft_h():return M['hinge_axle']-[12,0,0]
def shaft_r():return tx(M['roller_axle']-[12,12,0],rot('z',-45))
def fold_parts(a=70,hardware=True,explode=False):
    parts=[(M['fold_base'],GREEN)];w=wing_n()
    for s in [1,-1]:
        v=tx((w if s==1 else wing_s())-[0,0,10],rot('x',s*a),[0,s*54,10])
        if explode:v+=[0,s*35,50]
        parts.append((v,GOLD))
        if hardware:
            parts.append((tx(shaft_h(),t=(-3-(35 if explode else 0),s*54,6.8)),SAGE))
            parts.append((tx(M['lock_key'],t=(205.5+(20 if explode else 0),s*54,2.1)),ORANGE))
            if a in [0,70,100]:parts.append((tx(M['index_pin'],rot('y',-90),[202+(30 if explode else 0),s*(54+22*math.cos(math.radians(a))),10+22*math.sin(math.radians(a))]),ORANGE))
    return parts

def roller_parts():
    parts=[(shaft_r(),SAGE),(tx(M['roller_body'],rot('y',90),[28.6,0,5.2]),GOLD)]
    for x in [3.8,229.4]:parts.append((tx(M['roller_grip'],rot('y',90),[x,0,5.2]),GREEN))
    for x in [29.8,221.8]:parts.append((tx(M['ring_4mm'],rot('y',90),[x,0,5.2]),ORANGE))
    parts.extend([(tx(M['roller_washer'],rot('y',90),[254.2,0,5.2]),GREEN),(tx(M['lock_key'],t=[258.5,0,-.7]),ORANGE)])
    return parts

def board_parts():
    out=[(tx(M['board_tile'],t=(x,y,0)),SAGE) for x in [0,180] for y in [0,180]]
    for y in [45,135,225,315]:out.append((tx(M['board_key'],t=(180,y,0)),GOLD))
    for x in [45,135,225,315]:out.append((tx(M['board_key'],rot('z',90),(x,180,0)),GOLD))
    return out

def render(parts,size=(900,600),view=(1,-1,.85),bg=BG):
    W,H=size;im=np.tile(rgb(bg),(H,W,1));depth=np.full((H,W),-np.inf)
    d=np.array(view,dtype=float);d/=np.linalg.norm(d);u=np.cross([0,0,1],d);u/=np.linalg.norm(u);v=np.cross(d,u);basis=np.array([u,v,d]).T
    q=np.concatenate([a for a,c in parts])@basis;lo=q.reshape(-1,3).min(0);hi=q.reshape(-1,3).max(0);center=(lo+hi)/2
    scale=min((W*.92)/(hi[0]-lo[0]),(H*.88)/(hi[1]-lo[1]));light=np.array([-.3,-.6,1]);light/=np.linalg.norm(light)
    for tris,color in parts:
        proj=(tris@basis-center);proj[:,:,0]=proj[:,:,0]*scale+W/2;proj[:,:,1]=H/2-proj[:,:,1]*scale
        norm=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1,keepdims=True),1e-12);shades=.55+.45*np.maximum(0,norm@light)
        for idx,t in enumerate(proj):
            x0,y0,z0=t[0];x1,y1,z1=t[1];x2,y2,z2=t[2];den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(den)<1e-8:continue
            xa=max(0,int(np.floor(min(x0,x1,x2))));xb=min(W-1,int(np.ceil(max(x0,x1,x2))));ya=max(0,int(np.floor(min(y0,y1,y2))));yb=min(H-1,int(np.ceil(max(y0,y1,y2))))
            if xa>xb or ya>yb:continue
            X,Y=np.meshgrid(np.arange(xa,xb+1)+.5,np.arange(ya,yb+1)+.5);a=((y1-y2)*(X-x2)+(x2-x1)*(Y-y2))/den;b=((y2-y0)*(X-x2)+(x0-x2)*(Y-y2))/den;c=1-a-b
            z=a*z0+b*z1+c*z2;sl=depth[ya:yb+1,xa:xb+1];mask=(a>=-1e-8)&(b>=-1e-8)&(c>=-1e-8)&(z>sl);sl[mask]=z[mask];im[ya:yb+1,xa:xb+1][mask]=rgb(color)*shades[idx]
    return Image.fromarray((np.clip(im,0,1)*255).astype('uint8'))

def wrap(draw,text,xy,maxw,size=20,fill=INK,bold=False,spacing=8):
    words=text.split();line='';x,y=xy;f=font(size,bold)
    for word in words:
        if draw.textlength(line+' '+word,font=f)>maxw and line:
            draw.text((x,y),line,font=f,fill=fill);line=word;y+=size+spacing
        else:line=(line+' '+word).strip()
    draw.text((x,y),line,font=f,fill=fill)
    return y+size+spacing

def make_hero():
    im=Image.new('RGB',(1600,1030),BG);d=ImageDraw.Draw(im)
    d.text((54,30),'HALLACAITOR',font=font(58,True),fill=GREEN)
    d.text((58,108),'Mecánica simple para compartir la tradición.',font=font(25),fill=MUTED)
    d.rounded_rectangle((1260,40,1544,100),radius=25,fill=GREEN);d.text((1280,57),'v0.2 / CAD ALPHA',font=font(22,True),fill=BG)
    d.rounded_rectangle((40,172,1000,792),radius=24,fill='#E4E9DF')
    main=render(fold_parts(70),size=(930,480),bg='#E4E9DF');im.paste(main,(54,205));d=ImageDraw.Draw(im)
    d.text((74,706),'Plegar y atar en la misma base',font=font(30,True),fill=GREEN)
    d.text((76,750),'Alas indexadas · ejes retenidos · aguja guiada',font=font(21),fill=MUTED)
    tiles=[('01 / ESPESOR REPETIBLE',roller_parts()),('02 / DOSIS INTERCAMBIABLES',[(tx(M['dose_60ml'],t=[0,0,0]),SAGE),(tx(M['dose_80ml'],t=[95,0,0]),GOLD),(tx(M['dose_100ml'],t=[190,0,0]),ORANGE)]),('03 / INGREDIENTES A MANO',[(M['ingredient_caddy'],GREEN)]+[(tx(M['ingredient_cup'],t=[x,y,2]),GOLD) for x in [7,69,131] for y in [6,66]])]
    for i,(label,parts) in enumerate(tiles):
        y=172+i*207;d.rounded_rectangle((1030,y,1558,y+190),radius=20,fill='#E4E9DF');im.paste(render(parts,size=(480,142),bg='#E4E9DF'),(1042,y+40));d=ImageDraw.Draw(im);d.text((1054,y+15),label,font=font(18,True),fill=GREEN)
    steps=[('1','MASA','Porcionar y extender'),('2','HOJA','Presentar y aceitar'),('3','RELLENO','Servir y decorar'),('4','PLEGADO','Elevar y doblar'),('5','PABILO','Pasar y anudar')]
    for i,(n,h,t) in enumerate(steps):
        x=44+306*i;d.rounded_rectangle((x,828,x+292,937),radius=18,fill=GREEN);d.text((x+18,846),n,font=font(36,True),fill=GOLD);d.text((x+66,848),h,font=font(19,True),fill=BG);d.text((x+66,881),t,font=font(16),fill='#D5DFD5')
    d.text((52,971),'PIEZAS REALES DEL CAD  /  Accionamiento manual  /  Sin ensayo físico ni validación alimentaria',font=font(20),fill=MUTED)
    im.save(ASSETS/'hero.png',optimize=True)

def make_exploded():
    im=Image.new('RGB',(1500,980),BG);im.paste(render(fold_parts(30,explode=True),size=(1120,760)),(30,140));d=ImageDraw.Draw(im)
    d.text((45,28),'Despiece del módulo central',font=font(40,True),fill=GREEN);d.text((48,88),'Dos alas de distinta mano. No imprimir dos copias del mismo STL.',font=font(23),fill=MUTED)
    y=250
    for h,t in [('H01','Base común'),('H02N / H02S','Ala norte / sur'),('H03 × 2','Ejes de bisagra'),('H04 × 2','Chavetas instaladas'),('H05 × 2','Pines de posición')]:
        d.text((1125,y),h,font=font(22,True),fill=GREEN);wrap(d,t,(1125,y+35),320,20,fill=MUTED);y+=112
    d.text((50,924),'Los desplazamientos separan las piezas para verlas; no son distancias de montaje.',font=font(20),fill=MUTED)
    im.save(ASSETS/'exploded.png',optimize=True)

def make_gif():
    frames=[];dur=[]
    angles=[0,0,15,30,50,70,70,85,100,100,85,70,50,30,15,0]
    for a in angles:
        im=Image.new('RGB',(820,660),BG);im.paste(render(fold_parts(a),size=(800,480)),(10,95));d=ImageDraw.Draw(im)
        d.text((28,15),'PLEGADOR / '+str(a)+'°',font=font(28,True),fill=GREEN)
        d.text((30,60),'0° abierto     70° toma de hoja     100° cierre asistido',font=font(18),fill=MUTED)
        d.text((30,575),'Retirá el pasador → mové el ala → volvé a fijarlo',font=font(21,True),fill=GREEN)
        d.text((30,617),'Animación del CAD. El doblez y el nudo son manuales.',font=font(18),fill=MUTED)
        frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=96));dur.append(900 if a in [0,70,100] else 150)
    frames[0].save(ASSETS/'folding.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0,optimize=True,disposal=2)

def svg_header(title,w=1200,h=840):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{MUTED}"/></marker></defs><rect width="100%" height="100%" fill="{BG}"/><g font-family="DejaVu Sans,Arial,sans-serif" fill="{INK}"><text x="50" y="58" font-size="30" font-weight="bold">{title}</text><text x="52" y="94" font-size="17" fill="{MUTED}">Hallacaitor v0.2.0 · mm · plano de referencia · CAD sin ensayo físico</text>'''

def txt(x,y,t,size=18,fill=INK):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">{html.escape(t)}</text>'
def line(x1,y1,x2,y2,color=MUTED,width=1.5,dash=''):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def dim(x1,y1,x2,y2,label):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'+txt((x1+x2)/2+8,(y1+y2)/2-10,label,17)
def save_svg(name,s): (DRAW/name).write_text(s+'</g></svg>')
def diagrams():
    s=svg_header('Plegado + atado / planta y posiciones',1200,920)
    # Top view: x scale 3, y scale 3; origin x=150,y=390.
    X=lambda x:150+3*x;Y=lambda y:390-3*y
    s+=f'<rect x="{X(0)}" y="{Y(40)}" width="570" height="240" rx="9" fill="{SAGE}"/>'
    for y in [-25,0,25]:s+=f'<rect x="{X(0)}" y="{Y(y+5)}" width="570" height="30" fill="{BG}"/>'+txt(750,Y(y)+6,'y='+str(y),16)
    for x in [59,91,123]:s+=f'<rect x="{X(x-5)}" y="{Y(40)}" width="30" height="240" fill="{BG}"/>'+line(X(x),Y(-40),X(x),565)+txt(X(x)-20,590,str(x),16)
    for side in [-1,1]:
        y=side*54
        for start in [0,32,64,96,128,160]:s+=f'<rect x="{X(start)}" y="{Y(y+10)}" width="66" height="60" rx="7" fill="{GREEN if start%64==0 else GOLD}"/>'
        s+=line(X(-3),Y(y),X(209),Y(y),ORANGE,2,'5 4')
    s+=dim(X(0),635,X(190),635,'190')+dim(100,Y(-40),100,Y(40),'80')
    s+=line(X(0),Y(-40),X(0),650)+line(X(190),Y(-40),X(190),650)
    s+=txt(850,225,'Ejes Ø8 / agujeros Ø8,5',18)+txt(850,260,'Centros: y = ±54, z = 10',17)+txt(850,300,'Canales: 10 × 12',18)+txt(850,335,'Aguja: 212 × 6 × 2,4',17)+txt(850,375,'Paquete de referencia:',18)+txt(850,410,'140 × 80 × 35',20)
    s+=txt(150,700,'Índice del ala / radio 22 mm',22)
    cx,cy=320,835
    for a in [0,70,100]:
        x=cx+105*math.cos(math.radians(a));y=cy-105*math.sin(math.radians(a));s+=line(cx,cy,x,y,GOLD,8)+f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{GREEN}" stroke-width="3"/>'+txt(x+12,y-10,str(a)+'°',18)
    s+=txt(580,745,'La oreja y el brazo se omiten en planta para ver los canales.',17)+txt(580,785,'Los agujeros fijan posiciones, no frenan solos el recorrido.',17)+txt(580,825,'Retirar el pin antes de girar. No forzar por encima de 100°.',17)
    save_svg('folding.svg',s)
    s=svg_header('Rodillo / montaje longitudinal',1200,760)
    xx=lambda x:90+3.7*x
    s+=line(xx(0),350,xx(264),350,SAGE,14)
    for x in [3.8,229.4]:s+=f'<rect x="{xx(x)}" y="298" width="{24*3.7}" height="104" rx="12" fill="{GREEN}"/>'
    s+=f'<rect x="{xx(28.6)}" y="276" width="740" height="148" rx="2" fill="{GOLD}"/>'
    for x in [29.8,221.8]:s+=f'<rect x="{xx(x)}" y="261.2" width="20.72" height="177.6" rx="3" fill="{ORANGE}"/>'
    s+=f'<rect x="{xx(254.2)}" y="311" width="7.4" height="78" fill="{GREEN}"/>'+line(xx(258.5),310,xx(258.5),390,ORANGE,6)
    s+=dim(xx(28.6),230,xx(228.6),230,'200 cuerpo')+dim(xx(35.6),480,xx(221.6),480,'186 útiles')+dim(xx(0),550,xx(264),550,'264 eje; se imprime diagonal')
    s+=txt(90,625,'Ø40 cuerpo · aros Ø46/48/50 → espesores 3/4/5 mm · dos mangos de 24 mm',21)
    s+=txt(90,671,'Asiento de aro Ø39,4 × 6; aro abierto Ø39,2 interior × 5,6; comprobar ajuste en PETG.',18)
    s+=txt(90,711,'Cara plana del eje hacia la cama. Arandela y chaveta retienen el extremo libre.',18)
    save_svg('roller.svg',s)
    s=svg_header('Pabilo / tres vueltas por cada eje',1200,850)
    X=lambda x:170+4*x;Y=lambda y:420-4*y
    s+=f'<rect x="{X(0)}" y="{Y(40)}" width="760" height="320" rx="15" fill="{SAGE}"/>'
    s+=f'<rect x="{X(21)}" y="{Y(40)}" width="560" height="320" rx="25" fill="{GREEN}"/>'
    for i,y in enumerate([-25,0,25]):s+=line(X(8),Y(y),X(174),Y(y),GOLD,7,'12 7')+txt(105,Y(y)+6,'A'+str(i+1),20)
    for i,x in enumerate([59,91,123]):s+=line(X(x),Y(-48),X(x),Y(48),ORANGE,6,'12 7')+txt(X(x)-13,Y(48)-18,'B'+str(i+1),20)
    s+=txt(170,175,'Vista superior del paquete. Trazos discontinuos: pasos por debajo.',19)
    s+=txt(170,650,'A1 → A2 → A3: entrar por canal, volver por arriba en cada vuelta.',20)
    s+=txt(170,692,'B1 → B2 → B3: cambiar de eje y repetir con el mismo tramo.',20)
    s+=txt(170,734,'Conectar las vueltas por fuera del paquete; luego tensar y hacer nudo llano.',19)
    s+=txt(170,780,'Las líneas son rutas, no cuerdas preinstaladas. Hoja y cruces reales requieren ensayo.',17,fill=MUTED)
    save_svg('tying.svg',s)
    s=svg_header('Flujo de trabajo / ayudas y tareas manuales',1200,770)
    steps=[('01','MASA','Amasar en bolsa y porcionar','60 / 80 / 100 ml'),('02','EXTENDIDO','Hoja + barrera superior','Rodillo 3 / 4 / 5 mm'),('03','RELLENO','Servir guiso y adornos','40 / 60 ml + seis recipientes'),('04','HOJA','Levantar alas y tomar bordes','0° / 70° / 100°'),('05','ENVOLTURA','Doblez, extremos y refuerzo','Cierre central manual'),('06','PABILO','Seis vueltas y nudo llano','Medidor + aguja roma')]
    for i,(n,h,t,sub) in enumerate(steps):
        x=50+(i%3)*375;y=150+(i//3)*260
        s+=f'<rect x="{x}" y="{y}" width="350" height="220" rx="18" fill="{GREEN}"/>'+txt(x+23,y+50,n,30,GOLD)+txt(x+23,y+95,h,24,BG)+txt(x+23,y+143,t,17,BG)+txt(x+23,y+180,sub,16,'#CAD8CA')
    s+=txt(55,735,'Preparación térmica, recorte y cocción fuera de la estación. Todo el accionamiento es manual.',18)
    save_svg('workflow.svg',s)

def sizing():
    fig,ax=plt.subplots(figsize=(10,4.8),facecolor=BG);ax.set_facecolor(BG)
    for t,c in [(3,ORANGE),(4,GREEN),(5,'#9B7B40')]:
        V=np.linspace(50,110,100);ax.plot(V,np.sqrt(4000*V/(np.pi*t)),color=c,lw=2.5,label=f'{t} mm')
    ax.axhline(186,color=MUTED,ls='--',lw=1.2);ax.text(51,189,'186 mm libres del rodillo',color=MUTED,fontsize=10)
    for vol,t in [(60,3),(80,4),(100,5)]:
        d=math.sqrt(4000*vol/(math.pi*t));ax.scatter([vol],[d],s=55,color=GREEN,zorder=5);ax.annotate(f'{vol} ml / {t} mm',(vol,d),xytext=(-25,-27),textcoords='offset points',fontsize=10,color=INK)
    ax.set(xlabel='Volumen de masa (ml nominales)',ylabel='Diámetro ideal del disco (mm)',ylim=(110,225),xlim=(50,110));ax.spines[['right','top']].set_visible(False);ax.grid(alpha=.13);ax.legend(title='Espesor',frameon=False,loc='upper left');fig.suptitle('Elegir dosis y espesor juntos',x=.10,ha='left',fontsize=18,weight='bold',color=GREEN);fig.text(.10,.015,'Geometría ideal. Forro, elasticidad, densidad y técnica no están modelados.',fontsize=10,color=MUTED);fig.tight_layout(rect=[0,.04,1,.96]);fig.savefig(ASSETS/'sizing.png',dpi=150);plt.close(fig)

def bom():
    m=json.loads((ROOT/'config/parts.json').read_text());rows=[]
    for p in m['parts']:
        a=audit(ROOT/p['file']);rows.append([p['sku'],p['name'],p['label'],*[p['quantities'][k] for k in ['minimum','standard','full']],' × '.join(f'{n:g}' for n in a['bbox_mm']),p['orientation']])
    with (ROOT/'docs/bom.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(['sku','part','description','minimum','standard','full','bbox_mm','orientation']);w.writerows(rows)
    s='# Lista de piezas y kits\n\n[Inicio](../README.md) · [Montaje](assembly.md) · [CSV](bom.csv)\n\nTodas las cotas son envolventes del STL en su orientación suministrada, en mm. No son medidas de encaje. El laminador debe centrar cada pieza; algunas llevan traslación de CAD.\n\n'
    for kit,label in [('minimum','Mínimo'),('standard','Estándar'),('full','Completo')]:
        s+=f"- **{label}: {sum(p['quantities'][kit] for p in m['parts'])} piezas.** "+{'minimum':'Plegado, atado simulado, pala y cupones; incluye una chaveta de repuesto.','standard':'Agrega tabla, rodillo con aros de 4 mm, dosis de 80 ml, medida de guiso de 60 ml y organizador.','full':'Suma otros espesores/dosis, tapas, bandeja y accesorios; cinco chavetas en total (tres instaladas y dos repuestos).'}[kit]+'\n'
    s+='\n| SKU | Archivo STL | Mín. | Est. | Comp. | X × Y × Z (mm) |\n|---|---|---:|---:|---:|---|\n'
    for r in rows:s+=f'| {r[0]} | [{r[1]}](../stl/{r[1]}.stl) | {r[3]} | {r[4]} | {r[5]} | {r[6]} |\n'
    s+='\n## Orientación y soportes\n\n| Pieza | Orientación / observación |\n|---|---|\n'
    for r in rows:s+=f'| {r[0]} | {r[-1]} |\n'
    s+='\nNo se necesitan tornillos, metal ni adhesivo. Las barreras alimentarias, hojas, cuerda y comida son consumibles externos. La regla y medidor no cortan. Herramientas de preparación (tijera, balanza, cocción) no están incluidas.\n\nNo se publican gramos ni horas sin un laminado real. Los volúmenes del informe de geometría representan sólidos cerrados, no consumo con relleno.\n'
    (ROOT/'docs/bom.md').write_text(s)

def main():
    ASSETS.mkdir(parents=True,exist_ok=True);DRAW.mkdir(parents=True,exist_ok=True)
    print('hero',flush=True);make_hero();print('exploded',flush=True);make_exploded();print('diagrams',flush=True);diagrams();sizing();bom();print('animation',flush=True);make_gif();print('illustrations ready',flush=True)
if __name__=='__main__':main()

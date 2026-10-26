#!/usr/bin/env python3
"""Original graphics from the shipped meshes; no downloaded recipe images."""
import json,math,os
from pathlib import Path
import numpy as np
from illustrate import render,M,rot,tx,wing_n,wing_s,shaft_h,font
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];A=R/'docs/assets/v3';A.mkdir(parents=True,exist_ok=True)
COL=['#588963','#d7a52c','#b96143','#8063a5','#4e81a0','#ce776c'];G='#7b8c83';BG='#f6f3ec'
def native_adapter(name,kind='plain'):
 h=9 if kind=='tipper' else 7 if kind in ['fold','tie'] else 4
 return tx(M[name]-[200,0,h],rot('y',180))
def family(a=70):
 out=[(M['fold_base_family'],COL[4])]
 for s in [1,-1]:
  out.append((tx((wing_n() if s==1 else wing_s())-[0,0,10],rot('x',s*a),[0,s*64,10]),'#88b0c5'))
  out.append((tx(shaft_h(),t=[-3,s*64,6.8]),G));out.append((tx(M['lock_key'],t=[205.5,s*64,2.1]),COL[5]))
  if a in [0,70,100]:out.append((tx(M['index_pin'],rot('y',-90),[202,s*(64+22*math.cos(math.radians(a))),10+22*math.sin(math.radians(a))]),COL[5]))
 return out
def wide(explode=0):
 out=[(M['wide_axle_left']-[0,10,0],G),(tx(M['wide_axle_right']-[0,10,0],t=[160+explode,0,0]),G)]
 out += [(tx(M['wide_roller_left'],rot('y',90),[28.6,0,5.2]),COL[1]),(tx(tx(M['wide_roller_right']-[0,0,140],rot('x',180)),rot('y',90),[168.6+explode,0,5.2]),COL[1])]
 for x in [29.8,301.8+explode]:out.append((tx(M['ring_2_5mm'],rot('y',90),[x,0,5.2]),COL[5]))
 for x in [3.8,309.4+explode]:out.append((tx(M['roller_grip'],rot('y',90),[x,0,5.2]),G))
 out += [(tx(M['roller_washer'],rot('y',90),[334.2+explode,0,5.2]),G),(tx(M['lock_key'],t=[338.5+explode,0,-.7]),COL[5]),(tx(M['axle_joint_pin'],t=[172,0,-.7]),COL[5])]
 return out
def tipper(a=0):
 out=[(native_adapter('dock_tipper_mount','tipper'),COL[3])]
 side=tx(M['tipper_side']-[0,18,8],rot('y',-90))
 for x in [48,144]:out.append((tx(side,t=[x,0,4]),COL[3]))
 cup=M['tipper_cup']-[40,28,0]
 out.append((tx(cup-[0,36,24],rot('x',a),[100,-8,104]),'#b9a0ce'))
 out.append((tx(M['tipper_axle']-[0,6,0],t=[45,-8,100.8]),G))
 out.append((tx(M['lock_key'],t=[163.5,-8,96.1]),COL[5]))
 for x in [44,140]:out.append((tx(M['tipper_foot_clip'],rot('z',180),[x+16,204,-3]),G))
 return out

def safe_save(im,path):
 tmp=path.with_name(path.stem+'.tmp.png');im.save(tmp,optimize=True);os.replace(tmp,path)
def card(name,title,parts,subtitle,size=(1200,740)):
 im=Image.new('RGB',size,BG);im.paste(render(parts,size=(size[0]-60,size[1]-180),bg=BG),(30,95));d=ImageDraw.Draw(im)
 d.text((32,20),title,font=font(30,True),fill='#203e35');d.text((32,size[1]-63),subtitle,font=font(17),fill='#455d54');d.text((32,size[1]-32),'CAD alpha · ilustración de geometría real · ensayo físico pendiente',font=font(15),fill='#62756c')
 safe_save(im,A/(name+'.png'))
def main():
 m=json.loads((R/'config/parts.json').read_text())
 for i,p in enumerate(m['parts']):
  safe_save(render([(M[p['name']],p['color'])],size=(520,380),bg=BG),A/(p['name']+'.png'))
 card('family','Plegador familiar / 70°',family(),'F01 + H02N + H02S + 2 H03 + 2 H04 + 2 H05')
 card('wide','Rodillo familiar / 266 mm útiles',wide(),'Dos camisas de 140 mm · eje partido de 344 mm · aros de 2,5 mm')
 card('wide-exploded','Unión del rodillo / separación ilustrativa',wide(50),'Acople D en camisas; solape de eje de 24 mm y pasador encerrado')
 card('tipper','Volcador / una porción precargada',tipper(0),'Eje detrás del vaso, fuera de la cavidad para alimentos; giro manual')
 card('tipper-pour','Volcador / muestra de giro a 90°',tipper(90),'Recibir sobre hoja delante de la estación. Comprobar estabilidad primero.')
 dock=[(M['dock_tile'],G),(tx(native_adapter('dock_worktop'),t=[0,0,48]),COL[1])]
 card('dock','Dock200 / montaje por gravedad',dock,'Separación vertical para mostrar tetones. No queda retenido al levantar.')
 stack=[(M['dock_tile'],G),(tx(M['dock_tile'],t=[0,0,112]),G)]
 for x in [20,180]:
  for y in [20,180]:stack.append((tx(M['stack_post'],t=[x,y,12]),COL[3]))
 card('storage','Guardado / solo módulos descargados',stack,'Cuatro postes; 96 mm libres entre pisos; solo útiles bajos y descargados.')
 # Original workflow schematic, not a photo and not a fabricated physical test.
 for i,(title,desc) in enumerate([
 ('Hoja íntegra','Preparar hoja flexible; colocar fibras y cara según la receta.'),
 ('Disco de masa','Extender 80–100 ml a 2,5 mm: diámetro ideal 202–226 mm.'),
 ('Guiso y adornos','Servir en el centro; dejar borde de masa libre para cerrar.'),
 ('Cerrar la masa','Elevar ambos lados con la hoja y juntar bordes de masa.'),
 ('Costura de hoja','Acomodar masa; juntar hoja y doblar la costura hacia abajo.'),
 ('Extremos y refuerzo','Doblar extremos; añadir segunda hoja y faja.'),
 ('Pabilo','Pasar vueltas por ambos ejes y hacer el nudo a mano.')]):
  im=Image.new('RGB',(1100,640),BG);d=ImageDraw.Draw(im);d.text((35,24),f'{i+1:02} / {title}',font=font(32,True),fill='#203e35')
  if i<3:
   d.rounded_rectangle((270,135,830,555),radius=12,fill='#abc5a4',outline='#588963',width=4)
   for y in range(150,540,23):d.line((280,y,820,y+22),fill='#8eae86',width=2)
   if i>=1:d.ellipse((390,205,710,505),fill='#f0c55a',outline='#b18c29',width=4)
   if i>=2:
    d.rounded_rectangle((465,290,635,395),radius=32,fill='#aa5b38')
    for x,y in [(490,310),(545,345),(610,320)]:d.ellipse((x,y,x+18,y+18),fill='#526d35')
  elif i in [3,4]:
   d.text((60,138),'Sección transversal',font=font(19),fill='#62756c')
   d.line([(290,420),(380,420),(475,220),(550,210),(625,220),(720,420),(810,420)],fill='#588963',width=16,joint='curve')
   d.line([(390,410),(482,239),(550,230),(618,239),(710,410)],fill='#f0c55a',width=22,joint='curve')
   d.rounded_rectangle((475,320,625,410),radius=30,fill='#aa5b38')
   if i==3:
    d.line((470,170,525,210),fill='#203e35',width=4);d.line((630,170,575,210),fill='#203e35',width=4)
    d.text((365,120),'Bordes de MASA en contacto',font=font(20,True),fill='#203e35')
   else:
    d.line([(550,210),(575,175),(610,195),(575,225)],fill='#588963',width=16,joint='curve')
    d.text((335,120),'Costura de HOJA doblada a mano',font=font(20,True),fill='#203e35')
  else:
   d.rounded_rectangle((335,220,765,440),radius=25,fill='#72986c',outline='#426b48',width=4)
   d.polygon([(335,235),(415,330),(335,425)],fill='#9dbc95');d.polygon([(765,235),(685,330),(765,425)],fill='#9dbc95')
   if i==6:
    for x in [430,550,670]:d.line((x,220,x,440),fill='#f1dec4',width=5)
    for y in [275,330,385]:d.line((335,y,765,y),fill='#f1dec4',width=5)
    d.ellipse((538,318,562,342),outline='#f1dec4',width=4)
   else:d.text((370,480),'Segunda hoja + faja, según receta',font=font(20),fill='#203e35')
  d.text((35,582),desc,font=font(18),fill='#203e35');safe_save(im,A/f'use-{i+1}.png')
 print(f'Generated {len(m["parts"])} part images + assemblies + 7 use diagrams')
if __name__=='__main__':main()

// Hallacaitor v0.2.0 | MIT | Copyright (c) 2026 Ariel
// Units: mm. Source: https://github.com/ariel-rajmaliuk/hallacaitor
// Prototype: no physical/food-contact validation. Consumable barriers required.
/* [View] */
part = "folding_assembly";
angle = 70; // [0:1:100]
/* [Calibration] */
clearance = 0.5; // DIAMETRAL, not radial
key_clearance = 0.30; // PER SIDE on flat keys
/* [Quality] */
facets = 64;
$fn = facets;
/* [Hidden] */
EPS = 0.02;
base_starts = [0,64,128];
wing_starts = [32,96,160];
index_angles = [0,70,100];
hinge_y = 54;
thread_x = [59,91,123];
thread_y = [-25,0,25];
function dose_height(v,d=60) = 4000*v/(PI*d*d);
module x_cylinder(d,l){ rotate([0,90,0]) cylinder(d=d,h=l); }
module round_rect(w,l,r=3,h=1){ linear_extrude(height=h) hull(){for(x=[r,w-r],y=[r,l-r]) translate([x,y])circle(r=r);} }
module side_disk(x,y,z,r,h){translate([x,y,z])x_cylinder(2*r,h);}
module barrel(x,y,z,l){translate([x,y,z])difference(){x_cylinder(20,l);translate([-EPS,0,0])x_cylinder(8+clearance,l+2*EPS);}}
// Fixed sector and bridge are beyond the moving wing, separated axially by 1.3 mm.
module index_ear(s,hy=54){
 difference(){union(){
  hull(){side_disk(196,s*hy,10,7,4);for(a=index_angles)side_disk(196,s*(hy+22*cos(a)),10+22*sin(a),6,4);}
  translate([184,s==1?hy-24:-hy+16,0])cube([16,8,6]);
  translate([196,s==1?hy-19:-hy+5,0])cube([4,14,14]);
 }
 for(a=index_angles)translate([195.9,s*(hy+22*cos(a)),10+22*sin(a)])x_cylinder(4+clearance,4.2);
 translate([195.9,s*hy,10])x_cylinder(8+clearance,4.2);
 }
}
module fold_base(hw=40,hy=54,ty=[-25,0,25]){difference(){union(){
 translate([0,-hw,0])round_rect(190,2*hw,3,20);
 for(s=[-1,1]){
  for(x=base_starts){translate([x,s==1?hw-2:-hy,0])cube([22,hy-hw+2,10]);barrel(x,s*hy,10,22);}
  index_ear(s,hy);
 }
 }
 // Channels align with axial GAPS in the hinge, so the needle can enter sideways.
 for(y=ty)translate([-EPS,y-5,8])cube([190+2*EPS,10,12+EPS]);
 for(x=thread_x)translate([x-5,-hw-EPS,8])cube([10,2*hw+2*EPS,12+EPS]);
 // No branding/lettering on the leaf support face.
 }}
module wing_native(){difference(){union(){
 translate([0,10,16])round_rect(190,102,4,4);
 for(x=wing_starts){translate([x,0,10])cube([22,15,10]);barrel(x,0,10,22);}
 // Hand opening stays outside the nominal 350 mm leaf.
 translate([68,108,16])round_rect(54,19,4,4);
 // Indexed radial arm. Its pivot lies exactly on the main hinge axis.
 hull(){side_disk(190.7,0,10,7,4);side_disk(190.7,22,10,6,4);}
 translate([174,10,10])cube([20.7,6,10]);
 }
 translate([190.6,0,10])x_cylinder(8+clearance,4.2);
 translate([190.6,22,10])x_cylinder(4+clearance,4.2);
 translate([78,116,-EPS])round_rect(34,6,2,20+2*EPS);
 }}
module wing_pose(s=1,a=angle,hy=54){
 if(s==1)translate([0,hy,10])rotate([a,0,0])translate([0,0,-10])wing_native();
 else translate([0,-hy,10])mirror([0,1,0])rotate([a,0,0])translate([0,0,-10])wing_native();
}
// Flat-backed shaft: axis z=d/2-.8. This avoids vertical, layer-weak long pins.
module shaft_native(d=8,l=212,head=12,slot=207){
 translate([0,0,-.8])difference(){union(){
 translate([0,0,d/2])x_cylinder(d,l);
 translate([0,0,d/2])x_cylinder(head,3);
 }
 translate([-EPS,-head,-head])cube([l+2*EPS,2*head,head+.8]);
 translate([slot,-1.75,-1])cube([3,3.5,head+2]);
 }
}
module lock_key(){union(){
 linear_extrude(height=12,scale=[1.08,1.08])square([2.5,3],center=true);
 translate([-3,-3,11.9])round_rect(6,6,1,2.1);
 }}
module index_pin(){union(){cylinder(d=7,h=2);translate([0,0,1.9])cylinder(d=4,h=13.1);}}
module folding_assembly(a=angle,hw=40,hy=54,ty=[-25,0,25]){
 color("#355e53")fold_base(hw,hy,ty);
 for(s=[-1,1]){
 color("#dfad68")wing_pose(s,a,hy);
 color("#a9bcb0")translate([-3,s*hy,6.8])shaft_native();
 color("#cb6c48")translate([205.5,s*hy,2.1])lock_key();
 color("#cb6c48")translate([202,s*(hy+22*cos(a)),10+22*sin(a)])rotate([0,-90,0])index_pin();
 }
}
module roller_body(){difference(){
 cylinder(d=40,h=200);
 translate([0,0,-EPS])cylinder(d=12+clearance,h=200+2*EPS);
 for(z=[1,193])translate([0,0,z])difference(){cylinder(d=41,h=6);translate([0,0,-EPS])cylinder(d=39.4,h=6+2*EPS);}
 }}
module roller_grip(){difference(){union(){
 cylinder(d=28,h=24);
 for(a=[0:30:330])rotate([0,0,a])translate([13,0,2])cylinder(d=3,h=20);
 }
 translate([0,0,-EPS])cylinder(d=12+clearance,h=24+2*EPS);
 }}
module roller_washer(){difference(){cylinder(d=21,h=2);translate([0,0,-EPS])cylinder(d=12+clearance,h=2+2*EPS);}}
module thickness_ring(t=4){difference(){cylinder(d=40+2*t,h=5.6);translate([0,0,-EPS])cylinder(d=39.2,h=5.6+2*EPS);translate([-2,0,-EPS])cube([4,30,6]);}}
module roller_assembly(t=4){
 color("#a9bcb0")shaft_native(12,264,20,257);
 color("#355e53")for(x=[3.8,229.4])translate([x,0,5.2])rotate([0,90,0])roller_grip();
 color("#dfad68")translate([28.6,0,5.2])rotate([0,90,0])roller_body();
 color("#cb6c48")for(x=[29.8,221.8])translate([x,0,5.2])rotate([0,90,0])thickness_ring(t);
 color("#355e53")translate([254.2,0,5.2])rotate([0,90,0])roller_washer();
 color("#cb6c48")translate([258.5,0,-.7])lock_key();
}
module bowtie_2d(){polygon([[-12,-7],[-12,7],[0,4],[12,7],[12,-7],[0,-4]]);}
module board_tile(){difference(){round_rect(180,180,3,6);
 for(y=[45,135],x=[0,180])translate([x,y,-EPS])linear_extrude(height=6+2*EPS)offset(delta=key_clearance)bowtie_2d();
 for(x=[45,135],y=[0,180])translate([x,y,-EPS])rotate([0,0,90])linear_extrude(height=6+2*EPS)offset(delta=key_clearance)bowtie_2d();
 }}
module board_key(){linear_extrude(height=5.8)bowtie_2d();}
module board_assembly(){
 color("#bec9be")for(x=[0,180],y=[0,180])translate([x,y,0])board_tile();
 color("#dfad68"){
 for(y=[45,135,225,315])translate([180,y,0])board_key();
 for(x=[45,135,225,315])translate([x,180,0])rotate([0,0,90])board_key();
 }}
module dose_ring(v=80){difference(){union(){
 cylinder(d=68,h=dose_height(v));
 translate([28,-13,0])round_rect(26,26,4,4);
 translate([36,0,4])linear_extrude(height=.6)text(str(v),size=6,halign="center",valign="center",font="DejaVu Sans:style=Bold");
 }
 translate([0,0,-EPS])cylinder(d=60,h=dose_height(v)+2*EPS);
 }}
module dose_plunger(){union(){cylinder(d=59.0,h=4);translate([0,0,3.9])cylinder(d=18,h=34.1);translate([0,0,37.9])cylinder(d=30,h=4.1);}}
module guiso_cup(v=60){difference(){union(){
 cylinder(d=58,h=3+dose_height(v,50));
 translate([24,-10,0])round_rect(42,20,4,5);
 translate([47,0,5])linear_extrude(height=.6)text(str(v),size=6,halign="center",valign="center",font="DejaVu Sans:style=Bold");
 }
 translate([0,0,3])cylinder(d=50,h=dose_height(v,50)+EPS);
 }}
module ingredient_cup(){difference(){round_rect(56,56,4,44);translate([3,3,3])round_rect(50,50,2,42);}}
module ingredient_lid(){difference(){round_rect(60,60,5,5);translate([1.65,1.65,-EPS])round_rect(56.7,56.7,4.35,3.4);}}
module ingredient_caddy(){difference(){round_rect(194,128,5,8);for(x=[7,69,131],y=[6,66])translate([x,y,2])round_rect(57,57,4.5,7);}}
module knead_tray(){difference(){round_rect(194,174,9,50);translate([4,4,4])round_rect(186,166,6,47);}}
module thread_needle(){difference(){hull(){translate([3,3,0])cylinder(d=6,h=2.4);translate([209,3,0])cylinder(d=6,h=2.4);}
 hull(){translate([9,3,-EPS])cylinder(d=2.8,h=2.5);translate([16,3,-EPS])cylinder(d=2.8,h=2.5);}
 }}
module cord_gauge(){union(){round_rect(200,36,4,5);for(x=[10,190])translate([x,18,4.9])cylinder(d=12,h=25.1);
 for(x=[40:30:160])translate([x,18,5])linear_extrude(height=.5)text(str((x-10)/30),size=6,halign="center",valign="center");
 }}
module end_paddle(){union(){round_rect(100,70,7,3);translate([34,65,0])round_rect(32,65,8,5);}}
module cord_cleat(){difference(){round_rect(50,30,4,12);linear_extrude(height=12+EPS)polygon([[14,31],[36,31],[25,5]]);}}
module fit_coupon(){difference(){round_rect(118,78,3,7);
 for(i=[0:3],j=[0:2])translate([15+i*29,15+j*24,-EPS])cylinder(d=[4,8,12][j]+[.3,.4,.5,.6][i],h=7+2*EPS);
 }}
module key_coupon(){difference(){round_rect(64,36,3,7);for(i=[0:2])translate([12+20*i,18,-EPS])cube([2.8+i*.1,3.4+i*.1,7.1],center=false);}}
module rule(){difference(){round_rect(200,24,2,3);for(x=[10:10:190])translate([x-.4,0,2.1])cube([.8,x%50==0?12:7,1]);}
 for(x=[50:50:150])translate([x,18,3])linear_extrude(height=.5)text(str(x),size=4,halign="center",valign="center");
}
module part_geometry(p=part){
 if(p=="fold_base")fold_base();
 else if(p=="fold_wing_north")translate([0,127,20])rotate([180,0,0])wing_native();
 else if(p=="fold_wing_south")translate([0,7,20])rotate([180,0,0])mirror([0,1,0])wing_native();
 else if(p=="hinge_axle")translate([12,0,0])rotate([0,0,0])shaft_native();
 else if(p=="lock_key")lock_key();else if(p=="index_pin")index_pin();
 else if(p=="roller_body")roller_body();else if(p=="roller_axle")translate([12,12,0])rotate([0,0,45])shaft_native(12,264,20,257);
 else if(p=="roller_grip")roller_grip();else if(p=="roller_washer")roller_washer();
 else if(p=="ring_3mm")thickness_ring(3);else if(p=="ring_4mm")thickness_ring(4);else if(p=="ring_5mm")thickness_ring(5);
 else if(p=="board_tile")board_tile();else if(p=="board_key")board_key();
 else if(p=="dose_60ml")dose_ring(60);else if(p=="dose_80ml")dose_ring(80);else if(p=="dose_100ml")dose_ring(100);else if(p=="dose_plunger")dose_plunger();
 else if(p=="guiso_40ml")guiso_cup(40);else if(p=="guiso_60ml")guiso_cup(60);
 else if(p=="ingredient_cup")ingredient_cup();else if(p=="ingredient_lid")ingredient_lid();else if(p=="ingredient_caddy")ingredient_caddy();
 else if(p=="knead_tray")knead_tray();else if(p=="thread_needle")thread_needle();else if(p=="cord_gauge")cord_gauge();
 else if(p=="end_paddle")end_paddle();else if(p=="cord_cleat")cord_cleat();else if(p=="fit_coupon")fit_coupon();else if(p=="key_coupon")key_coupon();else if(p=="rule")rule();
 else assert(false,str("Unknown part: ",p));
}
if(part=="folding_assembly")folding_assembly();
else if(part=="roller_assembly")roller_assembly();else if(part=="board_assembly")board_assembly();
else if(part=="collision_base_wing")intersection(){fold_base();wing_pose(1,angle);}
else if(part=="collision_needle_paths")intersection(){
 union(){fold_base();wing_pose(1,0);wing_pose(-1,0);}
 union(){
 for(x=thread_x)translate([x+3,-106,10])rotate([0,0,90])thread_needle();
 for(y=thread_y)translate([-11,y-3,10])thread_needle();
 }
}
else if(part=="collision_roller_rings")intersection(){
 translate([28.6,0,5.2])rotate([0,90,0])roller_body();
 for(x=[29.8,221.8])translate([x,0,5.2])rotate([0,90,0])thickness_ring(4);
}
else if(part=="collision_wings")intersection(){wing_pose(1,angle);wing_pose(-1,angle);}
else part_geometry();

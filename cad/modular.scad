// Hallacaitor 0.3 | MIT | all dimensions mm
// New: Dock 200, two layouts, familiar-size roller and preloaded portion tipper.
use <hallacaitor.scad>
part="dock_tile";
angle=70;
clearance=.5;
facets=64;
$fn=facets;
E=.02;
module rr(w,d,r,h){round_rect(w,d,r,h);}
module xc(d,h){rotate([0,90,0])cylinder(d=d,h=h);}
// 100-mm locator lattice permits 0/100-mm offsets on a 200-mm tile.
// Gravity registration: not a clamp, not retained against lifting.
module dock_tile(){difference(){union(){rr(200,200,4,8);for(x=[20,180],y=[20,180])translate([x,y,-8])cylinder(d=22,h=8.1);}
 for(x=[50,150],y=[50,150])translate([x,y,3])cylinder(d=8.6,h=5.1);
 for(x=[20,180],y=[20,180]){
 translate([x,y,3])cylinder(d=12.6,h=5.1);
 translate([x,y,-8.1])cylinder(d=12.6,h=4.5);
 }
 for(x=[0,200],y=[50,150])translate([x,y,-E])linear_extrude(height=8+2*E)offset(delta=.3)bowtie_2d();
 for(x=[50,150],y=[0,200])translate([x,y,-E])rotate([0,0,90])linear_extrude(height=8+2*E)offset(delta=.3)bowtie_2d();
 }}
module dock_joiner(){linear_extrude(height=7.8)bowtie_2d();}
module locator_pegs(){for(x=[50,150],y=[50,150])translate([x,y,-4.4])cylinder(d=8,h=4.5);}
module adapter_native(kind="plain"){difference(){union(){rr(200,200,3,4);locator_pegs();
 if(kind=="fold"){
  translate([.5,90,4])cube([4,20,3]);translate([195.5,90,4])cube([4,20,3]);
  for(y=[45.5,150.5])translate([100,y,4])cube([10,4,3]);
 }
 if(kind=="tie"){
  for(y=[30.5,165.5])translate([85,y,4])cube([30,4,3]);
 }
 if(kind=="tipper")for(x=[48,144]){
  translate([x-2.4,140,4])cube([2,56,5]);
  translate([x+8.4,140,4])cube([2,56,5]);
  translate([x-2.4,137.6,4])cube([12.8,2,5]);
 }
 }
 // Flush station colour/ID tile, kept outside the active food area.
 translate([79.7,4.7,1.8])cube([40.6,16.6,2.3]);
 if(kind=="guiso")for(x=[55,145])translate([x,110,2])cylinder(d=58.7,h=2.1);
 if(kind=="adornos")for(x=[8,71,134],y=[35,101])translate([x,y,2])rr(57,57,4.5,2.1);
 }}
module adapter_print(kind="plain"){h=kind=="tipper"?9:((kind=="fold"||kind=="tie")?7:4);translate([200,0,h])rotate([0,180,0])adapter_native(kind);}
// Posts only support a CLOSED, unloaded storage tier. They are not machine columns.
module stack_post(){union(){cylinder(d=12,h=4);translate([0,0,4])cylinder(d=18,h=96);translate([0,0,100])cylinder(d=12,h=4);}}
module station_tag(n=1){difference(){rr(40,16,2,2);translate([20,8,1.3])linear_extrude(height=.8)text(str("S",n),size=7,halign="center",valign="center",font="DejaVu Sans:style=Bold");}}
module family_fold(){fold_base(50,64,[-30,0,30]);}
module family_tie(){difference(){rr(200,130,4,18);
 for(x=[60,100,140])translate([x-5,-E,6])cube([10,130+2*E,12+E]);
 for(y=[40,65,90])translate([-E,y-5,6])cube([200+2*E,10,12+E]);}}
// Generic flat support covers are reversible; no mechanism underneath is pressed over.
module hub_side_native(){union(){translate([0,0,29])rr(96,200,3,3);
 for(x=[20,76],y=[20,180])translate([x,y,8])cylinder(d=14,h=21.1);
 for(y=[50,150]){
 translate([50,y,8])cylinder(d=14,h=21.1);
 translate([50,y,3.6])cylinder(d=8,h=4.5);
 }
 }}
// Wide rolling drum: D-profile alignment coupling, captured by a two-piece axle.
module d_profile(d=29.4,flat=11,h=24){intersection(){cylinder(d=d,h=h);translate([-d,-d,-E])cube([d+flat,2*d,h+2*E]);}}
module wide_roller_left(){difference(){union(){cylinder(d=40,h=140);translate([0,0,139.9])d_profile(29.4,11,24.1);}
 translate([0,0,-E])cylinder(d=12.5,h=164.1);
 translate([0,0,1])difference(){cylinder(d=41,h=6);translate([0,0,-E])cylinder(d=39.4,h=6.1);}
 }}
module wide_roller_right_native(){difference(){cylinder(d=40,h=140);
 translate([0,0,-E])cylinder(d=12.5,h=140.1);
 translate([0,0,-E])d_profile(30,11.6,24.6);
 translate([0,0,133])difference(){cylinder(d=41,h=6);translate([0,0,-E])cylinder(d=39.4,h=6.1);}
 }}
module wide_axle_left(){difference(){shaft_native(12,184,20,300);
 translate([160,-.15,-E])cube([24.1,20,20]);
 translate([172,0,-1])cylinder(d=4.4,h=20);
 }}
module wide_axle_right(){difference(){shaft_native(12,184,12,177);
 translate([-E,-20,-E])cube([24.02,20.15,20]);
 translate([12,0,-1])cylinder(d=4.4,h=20);
 }}
module axle_joint_pin(){cylinder(d=4,h=11.8);}
module wide_roller_assembly(){
 color("#637A70")wide_axle_left();color("#637A70")translate([160,0,0])wide_axle_right();
 color("#E6AE49")translate([28.6,0,5.2])rotate([0,90,0])wide_roller_left();
 color("#E6AE49")translate([168.6,0,5.2])rotate([0,90,0])wide_roller_right_native();
 color("#C76C4F")for(x=[29.8,301.8])translate([x,0,5.2])rotate([0,90,0])thickness_ring(2.5);
 color("#637A70")for(x=[3.8,309.4])translate([x,0,5.2])rotate([0,90,0])roller_grip();
 color("#637A70")translate([334.2,0,5.2])rotate([0,90,0])roller_washer();
 color("#C76C4F")translate([338.5,0,-.7])lock_key();
 color("#C76C4F")translate([172,0,-.7])axle_joint_pin();
}
// Tipping cup: ONE manually preloaded portion, never bulk counting.
module tipper_cup(){difference(){union(){difference(){translate([-28,-28,0])rr(56,56,4,44);translate([-25,-25,3])rr(50,50,2,42);}
 for(s=[-1,1]){
 translate([s==1?32:-40,36,24])difference(){xc(16,8);translate([-E,0,0])xc(8.5,8.1);}
 translate([s==1?26:-36,20,16])cube([10,22,16]);
 }
 translate([18,-59,20])rr(15,35,4,6);
 }
 translate([-41,36,24])xc(8.5,82);
 }}
module tipper_side_native(){difference(){union(){
 // Profile in YZ, X thickness 8; rear foot captured by removable C-clip.
 translate([0,140,0])cube([8,56,8]);
 hull(){translate([0,-8,100])xc(20,8);translate([0,170,100])xc(20,8);}
 hull(){translate([0,-8,100])xc(14,8);translate([0,160,15])xc(14,8);}
 translate([0,150,0])cube([8,40,105]);
 }
 translate([-E,-8,100])xc(8.5,8.1);
 }}
module tipper_side_print(){translate([0,18,8])rotate([0,90,0])tipper_side_native();}
module tipper_foot_clip(){difference(){rr(16,28,2,18.6);translate([-E,4,3])cube([16.1,24.1,12.6]);translate([-E,13.4,15.6])cube([16.1,14.7,3.1]);}}
module liner_clip(){difference(){rr(10,12,1.5,12);translate([3.2,-E,2])cube([3.6,12.1,10.1]);}}
module tipper_pose(a=0){translate([100,-8,100])rotate([a,0,0])translate([0,-36,-24])tipper_cup();}
module tipper_assembly(a=0){color("#6D5B99")adapter_native("tipper");
 for(x=[48,144])color("#6D5B99")translate([x,0,4])tipper_side_native();
 color("#A899C0")translate([0,0,4])tipper_pose(a);
 color("#637A70")translate([45,-8,100.8])shaft_native(8,122,12,117);
 color("#C76C4F")translate([163.5,-8,96.1])lock_key();
 for(x=[44,140])color("#637A70")translate([x+16,204,-3])rotate([0,0,180])tipper_foot_clip();
}
module modular_part(p=part){
 if(p=="dock_tile")translate([0,0,8])dock_tile();
 else if(p=="dock_joiner")dock_joiner();
 else if(p=="dock_worktop")adapter_print();
 else if(p=="dock_fold_mount")adapter_print("fold");
 else if(p=="dock_tie_mount")adapter_print("tie");
 else if(p=="dock_guiso_mount")adapter_print("guiso");
 else if(p=="dock_adornos_mount")adapter_print("adornos");
 else if(p=="dock_tipper_mount")adapter_print("tipper");
 else if(p=="stack_post")stack_post();
 else if(p=="hub_side_top")translate([96,0,32])rotate([0,180,0])hub_side_native();
 else if(p=="fold_base_family")family_fold();
 else if(p=="tie_base_family")family_tie();
 else if(p=="wide_roller_left")wide_roller_left();
 else if(p=="wide_roller_right")translate([0,0,140])rotate([180,0,0])wide_roller_right_native();
 else if(p=="wide_axle_left")translate([0,10,0])wide_axle_left();
 else if(p=="wide_axle_right")translate([0,10,0])wide_axle_right();
 else if(p=="axle_joint_pin")axle_joint_pin();
 else if(p=="ring_2_5mm")thickness_ring(2.5);
 else if(p=="tipper_cup")translate([40,28,0])tipper_cup();
 else if(p=="tipper_side")tipper_side_print();
 else if(p=="tipper_axle")translate([0,6,0])shaft_native(8,122,12,117);
 else if(p=="tipper_foot_clip")tipper_foot_clip();
 else if(p=="liner_clip")liner_clip();
 else if(p=="station_tag_1")station_tag(1);else if(p=="station_tag_2")station_tag(2);else if(p=="station_tag_3")station_tag(3);else if(p=="station_tag_4")station_tag(4);else if(p=="station_tag_5")station_tag(5);else if(p=="station_tag_6")station_tag(6);
 else assert(false,str("Unknown modular part ",p));
}
if(part=="family_folding_assembly")folding_assembly(angle,50,64,[-30,0,30]);
else if(part=="wide_roller_assembly")wide_roller_assembly();
else if(part=="tipper_assembly")tipper_assembly(angle);
else if(part=="check_family_base_wing")intersection(){family_fold();wing_pose(1,angle,64);}
else if(part=="check_family_wings")intersection(){wing_pose(1,angle,64);wing_pose(-1,angle,64);}
else if(part=="check_dock_adapter")intersection(){dock_tile();translate([0,0,8])adapter_native();}
else if(part=="check_drum_coupling")intersection(){wide_roller_left();translate([0,0,140])wide_roller_right_native();}
else if(part=="check_axle_lap")intersection(){wide_axle_left();translate([160,0,0])wide_axle_right();}
else if(part=="check_tipper_sides")intersection(){tipper_pose(angle);for(x=[48,144])translate([x,0,0])tipper_side_native();}
else if(part=="check_tipper_shaft_cup")intersection(){tipper_pose(angle);translate([45,-8,96.8])shaft_native(8,122,12,117);}
else if(part=="check_tipper_mount")intersection(){adapter_native("tipper");for(x=[48,144])translate([x,0,4])tipper_side_native();}
else if(part=="check_family_mount")intersection(){adapter_native("fold");translate([5,100,4])family_fold();}
else if(part=="check_tipper_clips")intersection(){union(){adapter_native("tipper");for(x=[48,144])translate([x,0,4])tipper_side_native();}for(x=[44,140])translate([x+16,204,-3])rotate([0,0,180])tipper_foot_clip();}
else if(part=="check_stack_posts")intersection(){union(){translate([0,0,8])dock_tile();translate([0,0,120])dock_tile();}for(x=[20,180],y=[20,180])translate([x,y,12])stack_post();}
else if(part=="check_family_needle")intersection(){union(){family_fold();wing_pose(1,0,64);wing_pose(-1,0,64);}union(){for(x=[59,91,123])translate([x+3,-106,10])rotate([0,0,90])thread_needle();for(y=[-30,0,30])translate([-11,y-3,10])thread_needle();}}
else if(part=="check_wide_axle_drum")intersection(){union(){wide_axle_left();translate([160,0,0])wide_axle_right();}union(){translate([28.6,0,5.2])rotate([0,90,0])wide_roller_left();translate([168.6,0,5.2])rotate([0,90,0])wide_roller_right_native();}}
else if(part=="check_wide_key_washer")intersection(){translate([334.2,0,5.2])rotate([0,90,0])roller_washer();translate([338.5,0,-.7])lock_key();}
else if(part=="check_compact_key_washer")intersection(){translate([254.2,0,5.2])rotate([0,90,0])roller_washer();translate([258.5,0,-.7])lock_key();}
else modular_part();

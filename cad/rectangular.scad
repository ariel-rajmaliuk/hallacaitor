// Hallacaitor Rect 0.4 - MIT - Copyright (c) 2026 Ariel
// New architecture prototype. Units mm. Not physically or food-contact validated.
// All structural hardware printed. Optional razor and thread are purchased consumables.
use <hallacaitor.scad>
use <modular.scad>
part="rect_tile"; facets=48; $fn=facets; angle=70; travel=0; E=.02;
module xc(d,h){rotate([0,90,0])cylinder(d=d,h=h);}
module loc_stud(){translate([4,4,12])cube([16,16,6]);}
module corner_interface_cuts(){
 translate([3.7,3.7,-E])cube([16.6,16.6,6.62]);
 for(z=[3,15])translate([-E,9.8,z-2.2])cube([24.1,4.4,4.4]);
}
module frame_quarter(solid=false){difference(){union(){
 if(solid)cube([200,150,12]);else{cube([200,24,12]);cube([24,150,12]);}
 loc_stud();
 }
 corner_interface_cuts();
 translate([200,12,-E])linear_extrude(height=12.1)offset(delta=.3)bowtie_2d();
 translate([12,150,-E])rotate([0,0,90])linear_extrude(height=12.1)offset(delta=.3)bowtie_2d();
 if(solid){translate([200,75,-E])linear_extrude(height=12.1)offset(delta=.3)bowtie_2d();translate([100,150,-E])rotate([0,0,90])linear_extrude(height=12.1)offset(delta=.3)bowtie_2d();}
}}
module frame_assembly(solid=false){
 frame_quarter(solid);translate([400,0,0])mirror([1,0,0])frame_quarter(solid);
 translate([0,300,0])mirror([0,1,0])frame_quarter(solid);translate([400,300,0])mirror([1,0,0])mirror([0,1,0])frame_quarter(solid);
}
module frame_key(){linear_extrude(height=11.8)bowtie_2d();}
// Column seated on lower rim, retained at both ends by removable transverse pins.
module tower_post(){difference(){union(){cube([24,24,174]);translate([4,4,174])cube([16,16,6]);}
 translate([3.7,3.7,-E])cube([16.6,16.6,6.62]);
 for(z=[3,177])translate([-E,9.8,z-2.2])cube([24.1,4.4,4.4]);
}}
module tower_pin(){union(){translate([0,1.7,0])cube([30,3.6,3.6]);cube([3,7,7]);}}
module tower_pin_pose(z=15){translate([-3,8.5,z-1.8])tower_pin();}
module tower_frame(){color("#588963")frame_assembly(true);color("#8063a5")translate([0,0,186])frame_assembly(false);
 for(x=[0,376],y=[0,276]){color("#7b8c83")translate([x,y,12])tower_post();color("#d7a52c")translate([x,y,0])tower_pin_pose(15);color("#d7a52c")translate([x,y,0])tower_pin_pose(189);}}
// Short wings keep the complete open folding assembly inside 400 x 300 footprint.
module short_wing(){difference(){union(){
 translate([0,10,16])round_rect(190,60,4,4);
 for(x=[32,96,160]){translate([x,0,10])cube([22,15,10]);barrel(x,0,10,22);}
 translate([68,66,16])round_rect(54,19,4,4);
 hull(){side_disk(190.7,0,10,7,4);side_disk(190.7,22,10,6,4);}
 translate([174,10,10])cube([20.7,6,10]);}
 translate([190.6,0,10])xc(8.5,4.2);translate([190.6,22,10])xc(4.5,4.2);
 translate([78,74,-E])round_rect(34,6,2,20.1);
}}
module short_wing_pose(s=1,a=70){if(s==1)translate([0,64,10])rotate([a,0,0])translate([0,0,-10])short_wing();else translate([0,-64,10])mirror([0,1,0])rotate([a,0,0])translate([0,0,-10])short_wing();}
module rect_fold(a=70){color("#4e81a0")fold_base(50,64,[-30,0,30]);for(s=[-1,1]){color("#6e9eb8")short_wing_pose(s,a);color("#7b8c83")translate([-3,s*64,6.8])shaft_native();color("#ce776c")translate([205.5,s*64,2.1])lock_key();}}
// Rectangular dry doser: chamber is isolated from hopper before reaching discharge.
// 56 mm shuttle travel, two separated 22.6 mm ports. Manual return, no spring.
module dry_housing(){difference(){union(){cube([140,70,4]);translate([0,0,4])cube([140,14.6,24.6]);translate([0,55.4,4])cube([140,14.6,24.6]);}
 translate([74.7,23.7,-E])cube([22.6,22.6,4.1]);translate([96,51,1.8])cylinder(d=4.4,h=2.3);
}}
module dry_lid(){difference(){cube([140,70,6]);translate([18.7,23.7,-E])cube([22.6,22.6,6.1]);translate([96,51,-E])cylinder(d=4.4,h=6.1);}}
module dry_shuttle(cw=22){difference(){union(){cube([120,40,24]);translate([119.9,3,0])cube([10.1,34,24]);}
 translate([30-cw/2,20-cw/2,-E])cube([cw,cw,24.1]);hull(){translate([40,36,-E])cylinder(d=4.4,h=24.1);translate([96,36,-E])cylinder(d=4.4,h=24.1);}}}
module dry_hopper(){difference(){union(){cube([70,70,6]);translate([3,3,6])cube([64,64,96]);}
 hull(){translate([23.7,23.7,-E])cube([22.6,22.6,6.1]);translate([6,6,18])cube([58,58,84.1]);}
}}
module dry_guide_pin(){union(){cylinder(d=4,h=32.6);translate([0,0,32.5])cylinder(d=7,h=2.1);}}
module dry_lid_cap(){cube([70,70,4]);}
module dry_stop(){difference(){cube([16,70,8]);translate([3,14.3,-E])cube([13.1,41.4,8.1]);}}
module dry_doser(t=0){color("#8063a5")dry_housing();color("#a58ec2")translate([t,15,4.3])dry_shuttle();color("#8063a5")translate([0,0,28.6])dry_lid();color("#8063a5")translate([-5,0,34.6])dry_hopper();color("#7b8c83")translate([96,51,2])dry_guide_pin();}
// Rectangular piston cartridge for guiso: 60 x 50 internal section, large outlet.
// Does not claim dosing repeatability or jam-free flow with arbitrary chunks.
module guiso_body(){difference(){union(){cube([70,60,12]);translate([0,0,30])cube([70,60,90]);translate([-10,-10,30])cube([90,80,6]);hull(){translate([0,0,28])cube([70,60,3]);translate([12.5,7.5,0])cube([45,45,4]);}}
 translate([5,5,32])cube([60,50,90]);hull(){translate([5,5,30])cube([60,50,3]);translate([17.5,12.5,-E])cube([35,35,4]);}
 translate([-E,5,4])cube([70.1,50,4.6]);
}}
module guiso_gate(){union(){cube([90,48.8,4]);translate([89.9,4,0])cube([8,40.8,12]);}}
module guiso_piston(){union(){cube([59,49,6]);translate([19.5,14.5,5.9])cube([20,20,110]);translate([0,0,115.8])cube([59,49,6]);}}
module piston_stop(h=20){difference(){cube([30,30,h]);translate([4.7,4.7,-E])cube([20.6,20.6,h+.1]);}}
module guiso_doser(){color("#b96143")guiso_body();color("#d58e71")translate([-2,5.6,4.3])guiso_gate();color("#d58e71")translate([5.5,5.5,85])guiso_piston();}
// Open magazine for individually separated pepper strips; manual tray, no false count.
module strip_magazine(){difference(){cube([160,80,44]);for(x=[4,43,82,121]){translate([x,4,4])cube([35,72,40.1]);translate([x,-E,4])cube([35,4.1,36]);}}}
module strip_drawer(){union(){cube([33.8,72,4]);for(x=[0,31.8])translate([x,0,0])cube([2,72,8]);translate([0,70,0])cube([33.8,2,8]);translate([0,-16,0])cube([33.8,16.1,12]);}}
module strip_lid(){difference(){cube([164,84,5]);translate([1.7,1.7,-E])cube([160.6,80.6,3.4]);}}
// Vertical bobbin pods fit left/right of the folded hallaca. Active + reserve.
// Wound diameter <=72, flange76, wound width88. Capacity is material-dependent.
module spool_box(){difference(){union(){cube([90,120,6]);cube([4,120,114]);translate([86,0,0])cube([4,120,114]);translate([0,112,0])cube([90,8,114]);for(x=[0,74],y=[0,104])translate([x,y,100])cube([16,16,14]);}
 translate([45,60,-E])cylinder(d=10.6,h=6.1);for(x=[8,82],y=[8,112])translate([x,y,107.5])cylinder(d=4.6,h=6.6);}}
module spool_cover(){difference(){union(){cube([90,120,6]);for(x=[8,82],y=[8,112])translate([x,y,-6])cylinder(d=4,h=6.1);}for(x=[17,69])translate([x,56,-E])cylinder(d=3.4,h=6.1);}}
module spool_left(){difference(){union(){cylinder(d=76,h=4);translate([0,0,3.9])cylinder(d=26,h=44.1);translate([0,0,47.9])cylinder(d=20,h=8.1);}translate([0,0,-E])cylinder(d=10.6,h=56.1);}}
module spool_right(){difference(){union(){cylinder(d=76,h=4);translate([0,0,3.9])cylinder(d=26,h=44.1);}translate([0,0,-E])cylinder(d=10.6,h=48.1);translate([0,0,39.4])cylinder(d=20.6,h=8.7);}}
module spool_adapter(){difference(){cylinder(d=25,h=20);translate([0,0,-E])cylinder(d=10.6,h=20.1);}}
module spool_axle(){union(){cylinder(d=18,h=3);translate([0,0,2.9])cylinder(d=10,h=108.1);}}
module spool_washer(){difference(){cylinder(d=18,h=2);translate([0,0,-E])cylinder(d=10.6,h=2.1);}}
module spool_set(show_thread=true){color("#ce776c")spool_box();color("#d58e82")translate([0,0,114])spool_cover();color("#7b8c83")translate([45,60,-3])spool_axle();color("#7b8c83")translate([45,60,6])spool_washer();
 color("#7b8c83")translate([45,60,8])spool_left();color("#7b8c83")translate([45,60,104])rotate([180,0,0])spool_right();
 if(show_thread)color("#d6c7a4")translate([45,60,12.1])difference(){cylinder(d=72,h=87.8);translate([0,0,-E])cylinder(d=26.4,h=87.9);}
}
// Cutter uses a replaceable DE razor as an optional purchased consumable.
// 43 x 22 x 0.1 nominal, verify actual blade. Recess 43.6 x22.6; edge recessed 10 mm.
module cutter_base(){difference(){cube([62,42,7]);translate([9.2,9.7,6.65])cube([43.6,22.6,.4]);translate([29.8,-E,5.8])cube([2.4,12.1,1.3]);for(x=[5,57])translate([x,21,-E])cylinder(d=3.4,h=7.1);}}
module cutter_cover(){difference(){cube([62,42,7]);translate([29.8,-E,-E])cube([2.4,12.1,7.1]);for(x=[5,57])translate([x,21,-E])cylinder(d=3.4,h=7.1);}}
module cutter_clamp(){difference(){cube([10,48.6,18.6]);translate([-E,3,2])cube([10.1,42.6,14.6]);translate([5,24.3,-E])cylinder(d=3.4,h=18.7);}}
module cutter_pin(){union(){cylinder(d=3,h=18.6);translate([0,0,18.5])cylinder(d=6,h=2);}}
module cutter_mount_pin(){union(){cylinder(d=3,h=25.6);translate([0,0,25.5])cylinder(d=6,h=2);}}
module cutter_pedestal(){cube([40,36,3]);}
module blade_dummy(){cube([43,22,.2]);}
module cutter_set(show_blade=false,mount=false){color("#ce776c")cutter_base();color("#d58e82")translate([0,0,7])cutter_cover();for(x=[0,52]){color("#7b8c83")translate([x,-3.3,-2.3])cutter_clamp();color("#7b8c83")translate([x+5,21,mount?-9.2:-2.2])if(mount)cutter_mount_pin();else cutter_pin();}if(show_blade)color("silver")translate([9.5,10,6.8])cube([43,22,.1]);}
// Bridge rails cross the frame; split halves share a sleeved center overlap.
module bridge_half(){cube([200,36,12]);}
module bridge_joiner(){difference(){cube([60,44.6,16]);translate([-E,4,4])cube([60.1,36.6,12.1]);}}
module bridge_dry_front(){difference(){bridge_half();translate([119.6,18.6,-E])cube([22.8,22.8,12.1]);}}
module bridge_dry_back(){difference(){bridge_half();translate([89.6,-1.4,-E])cube([22.8,22.8,12.1]);}}
module guiso_mount(){difference(){union(){translate([0,0,48])cube([100,100,8]);for(x=[0,88],y=[0,88])translate([x,y,0])cube([12,12,48.1]);}translate([14.7,19.7,47.9])cube([70.6,60.6,8.2]);}}
module funnel_body(){union(){translate([0,-4,67])cube([240,4.1,3]);difference(){hull(){translate([0,0,67])cube([240,240,3]);translate([92.5,92.5,0])cube([55,55,3]);}hull(){translate([3,3,67])cube([234,234,3.1]);translate([95.5,95.5,-E])cube([49,49,3.1]);}}}}
module funnel_quarter(){intersection(){funnel_body();translate([0,-4,-E])cube([120,124,71]);}}
module funnel_assembly(){funnel_quarter();translate([240,0,0])mirror([1,0,0])funnel_quarter();translate([0,240,0])mirror([0,1,0])funnel_quarter();translate([240,240,0])mirror([1,0,0])mirror([0,1,0])funnel_quarter();}
module funnel_hanger(){union(){cube([20,9,4]);cube([20,4,25]);translate([0,0,21])cube([20,59,4]);}}
module all_funnel_hangers(){for(x=[185,300])translate([x,21,189])funnel_hanger();for(x=[90,195])translate([x+20,279,189])rotate([0,0,180])funnel_hanger();}
module funnel_clip(){difference(){cube([30,9.6,14]);translate([-E,3,2])cube([30.1,3.6,12.1]);}}
module station_hub(){tower_frame();
 translate([100,150,12])rect_fold(angle);
 translate([0,90,12])spool_set();translate([310,90,12])spool_set();translate([333,128,132])cutter_pedestal();translate([322,125,135])cutter_set(true,true);
 color("#8063a5")translate([80,30,126])funnel_assembly();
 color("#7b8c83")translate([150,100,210])guiso_mount();translate([165,120,236])guiso_doser();
 color("#7b8c83"){for(x=[185,300])translate([x,21,189])funnel_hanger();for(x=[90,195])translate([x+20,279,189])rotate([0,0,180])funnel_hanger();for(y=[40,88,176,220])translate([170,y-4.3,194])bridge_joiner();}
 translate([45,35,210])dry_doser(travel);translate([215,195,210])dry_doser(travel);
 color("#8063a5"){
 translate([0,40,198])bridge_dry_front();translate([200,40,198])bridge_half();
 for(y=[88,176],x=[0,200])translate([x,y,198])bridge_half();
 translate([0,220,198])bridge_half();translate([200,220,198])bridge_dry_back();
 }
}
module station_twine(){color("#ce776c")frame_assembly(true);translate([0,90,12])spool_set();translate([310,90,12])spool_set();translate([333,128,132])cutter_pedestal();translate([322,125,135])cutter_set(true,true);color("#ce776c")translate([100,85,12])family_tie();}
if(part=="hub")station_hub();else if(part=="twine_station")station_twine();else if(part=="dry_assembly")dry_doser(travel);else if(part=="guiso_assembly")guiso_doser();else if(part=="cutter_assembly")cutter_set(true);else if(part=="spool_assembly")spool_set();else if(part=="fold_assembly")rect_fold(angle);
else if(part=="rect_tile")frame_quarter(true);else if(part=="rect_frame")frame_quarter();else if(part=="rect_key")frame_key();else if(part=="tower_post")tower_post();else if(part=="tower_pin")tower_pin();
else if(part=="short_wing_north")translate([0,85,20])rotate([180,0,0])short_wing();else if(part=="short_wing_south")translate([0,7,20])rotate([180,0,0])mirror([0,1,0])short_wing();
else if(part=="dry_housing")dry_housing();else if(part=="dry_lid")dry_lid();else if(part=="dry_shuttle")dry_shuttle();else if(part=="dry_shuttle_small")dry_shuttle(14);else if(part=="dry_hopper")dry_hopper();else if(part=="dry_lid_cap")dry_lid_cap();else if(part=="dry_guide_pin")dry_guide_pin();
else if(part=="guiso_body")guiso_body();else if(part=="guiso_gate")guiso_gate();else if(part=="guiso_piston")guiso_piston();else if(part=="piston_stop_20")piston_stop(20);else if(part=="piston_stop_13")piston_stop(13.3333);else if(part=="strip_drawer")strip_drawer();else if(part=="strip_magazine")strip_magazine();else if(part=="strip_lid")translate([164,0,5])rotate([0,180,0])strip_lid();
else if(part=="spool_box")spool_box();else if(part=="spool_left")spool_left();else if(part=="spool_right")spool_right();else if(part=="spool_adapter")spool_adapter();else if(part=="spool_axle")spool_axle();else if(part=="spool_cover")translate([90,0,6])rotate([0,180,0])spool_cover();else if(part=="spool_washer")spool_washer();
else if(part=="cutter_base")cutter_base();else if(part=="cutter_cover")cutter_cover();else if(part=="cutter_clamp")cutter_clamp();else if(part=="cutter_pin")cutter_pin();else if(part=="cutter_mount_pin")cutter_mount_pin();else if(part=="cutter_pedestal")cutter_pedestal();else if(part=="blade_dummy")blade_dummy();else if(part=="bridge_half")bridge_half();else if(part=="bridge_joiner")bridge_joiner();else if(part=="bridge_dry_front")bridge_dry_front();else if(part=="bridge_dry_back")bridge_dry_back();else if(part=="guiso_mount")guiso_mount();else if(part=="funnel_quarter")translate([0,0,70])rotate([180,0,0])funnel_quarter();else if(part=="funnel_clip")funnel_clip();else if(part=="funnel_hanger")funnel_hanger();
else if(part=="check_fold_pods")intersection(){translate([100,150,12])rect_fold(angle);union(){translate([0,90,12])spool_box();translate([310,90,12])spool_box();}}
else if(part=="check_fold_funnel")intersection(){translate([100,150,12])rect_fold(angle);translate([80,30,126])funnel_assembly();}
else if(part=="check_bridge_funnel")intersection(){translate([80,30,126])funnel_assembly();for(y=[40,88,176,220],x=[0,200])translate([x,y,198])bridge_half();}
else if(part=="check_cutter_mount")intersection(){translate([310,90,126])spool_cover();translate([322,125,135])cutter_set();}
else if(part=="check_column_frame")intersection(){frame_quarter();translate([0,0,12])tower_post();}
else if(part=="check_column_upper")intersection(){translate([0,0,12])tower_post();translate([0,0,186])frame_quarter();}
else if(part=="check_lock_pin")intersection(){union(){frame_quarter();translate([0,0,12])tower_post();}tower_pin_pose();}
else if(part=="check_dry_shuttle")intersection(){union(){dry_housing();translate([0,0,28.6])dry_lid();}translate([travel,15,4.3])dry_shuttle();}
else if(part=="check_guiso_gate")intersection(){guiso_body();translate([-2,5.6,4.3])guiso_gate();}
else if(part=="check_spool_coupling")intersection(){spool_left();translate([0,0,96])rotate([180,0,0])spool_right();}
else if(part=="check_spool_box")intersection(){spool_box();union(){translate([45,60,8])spool_left();translate([45,60,104])rotate([180,0,0])spool_right();}}
else if(part=="check_guiso_mount")intersection(){translate([150,100,210])guiso_mount();translate([165,120,236])guiso_body();}
else if(part=="check_funnel_hangers")intersection(){translate([80,30,126])funnel_assembly();all_funnel_hangers();}
else if(part=="check_hangers_dosers")intersection(){all_funnel_hangers();union(){translate([45,35,210])dry_doser(travel);translate([215,195,210])dry_doser(travel);}}
else if(part=="check_dry_pin")intersection(){translate([travel,15,4.3])dry_shuttle();translate([96,51,2])dry_guide_pin();}
else if(part=="check_cutter_clamps")intersection(){union(){cutter_base();translate([0,0,7])cutter_cover();}for(x=[0,52])translate([x,-3.3,-2.3])cutter_clamp();}
else if(part=="check_short_base")intersection(){fold_base(50,64,[-30,0,30]);short_wing_pose(1,angle);}
else if(part=="check_short_wings")intersection(){short_wing_pose(1,angle);short_wing_pose(-1,angle);}
else assert(false,str("Unknown Rect part: ",part));

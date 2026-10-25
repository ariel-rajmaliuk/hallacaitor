#!/usr/bin/env python3
"""Sizing helpers. Geometric estimates, not recipe or validated production rates."""
import argparse,json,math

def disk_diameter(volume_ml,thickness_mm):
    if volume_ml<=0 or thickness_mm<=0:raise ValueError('Volume and thickness must be positive')
    return math.sqrt(4000*volume_ml/(math.pi*thickness_mm))
def cord_length(length_mm,width_mm,height_mm,turns=3,tails_mm=300):
    if min(length_mm,width_mm,height_mm,turns)<=0 or tails_mm<0:raise ValueError('Invalid dimensions')
    return turns*2*(length_mm+height_mm)+turns*2*(width_mm+height_mm)+tails_mm

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--length',type=float,default=140);ap.add_argument('--width',type=float,default=80);ap.add_argument('--height',type=float,default=35);ap.add_argument('--turns',type=int,default=3);ap.add_argument('--tails',type=float,default=300);ap.add_argument('--volume',type=float,default=80);ap.add_argument('--thickness',type=float,default=4)
    a=ap.parse_args();d=disk_diameter(a.volume,a.thickness);l=cord_length(a.length,a.width,a.height,a.turns,a.tails)
    print(json.dumps({'disk_diameter_mm':round(d,1),'roller_clear_width_mm':186,'fits_with_2mm_edge_margin':d<=182,'cord_nominal_mm':round(l),'cord_initial_trial_mm':math.ceil((l+150)/100)*100,'gauge_turn_mm':round(360+12*math.pi,1),'note':'Rectangular-perimeter approximation; liners, leaf, routing and cord tension require calibration.'},indent=2))
if __name__=='__main__':main()

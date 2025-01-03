﻿;--- Start G-code Begin ---
U is the distance of the coordinates and V is 0.055 times smaller than U.
M104 S275 T1
;M140 S60
G21
G90
M82
G28
M530 S1
G1 Z10 F900
; Start change extruder
M400
M109 S275 T1
T1 R ; switch extruder
; End change extruder
G92 E0 ; reset extrusion
G92 V0 ; reset extrusion
G92 U0 ; reset extrusion
;M190 S60
M400
M106 P0 S255
M106 P1 S255
G0 Z0.675 F1500
G1 F1200 V4
G4 P0
G1	X99.15	Y102.452	F7200
;--- Start G-code End -
;Layer0
G1 Z0.25 F300
G1	X99.15	Y132.452						
G1	X97.345	Y138.966						
G1	X96.169	Y145.687						
G1	X95.65	Y152.487						
G1	X95.65	Y227.513						
G1	X96.169	Y234.313						
G1	X97.345	Y241.034						
G1	X99.15	Y247.548						
G1	X99.15	Y272.015						
G1	X80.85	Y272.15						
G1	X80.85	Y247.548						
G1	X82.655	Y241.034						
G1	X83.831	Y234.313						
G1	X84.35	Y227.513						
G1	X84.35	Y152.487						
G1	X83.831	Y145.687						
G1	X82.655	Y138.966						
G1	X80.85	Y132.452						
G1	X80.85	Y107.85						
G1	X99.15	Y107.85						
G1	X98.225	Y108.475						
G1	X98.125	Y132.367						
G1	X96.335	Y138.828						
G1	X95.149	Y145.609						
G1	X95.025	Y152.463						
G1	X95.025	Y227.537						
G1	X95.549	Y234.391						
G1	X96.435	Y241.172						
G1	X97.625	Y247.633						
G1	X97.925	Y271.39						
G1	X82.075	Y271.525						
G1	X82.075	Y247.633						
G1	X83.565	Y241.172						
G1	X84.751	Y234.391						
G1	X84.975	Y227.537						
G1	X84.975	Y152.463						
G1	X84.551	Y145.609						
G1	X83.365	Y138.828						
G1	X82.275	Y132.367						
G1	X81.775	Y108.475						
G1	X98.225	Y108.475						
G1	X97.3	Y109.1						
G1	X97.2	Y132.282						
G1	X95.725	Y138.691						
G1	X94.528	Y145.531						
G1	X94.3	Y152.439						
G1	X94.4	Y227.561						
G1	X94.928	Y234.469						
G1	X95.825	Y241.309						
G1	X96.375	Y247.718						
G1	X96.675	Y270.765						
G1	X83.3	Y270.9						
G1	X83.5	Y247.718						
G1	X84.275	Y241.309						
G1	X85.372	Y234.469						
G1	X85.6	Y227.561						
G1	X85.6	Y152.439						
G1	X85.272	Y145.531						
G1	X84.275	Y138.691						
G1	X83.595	Y132.282						
G1	X82.725	Y109.1						
G1	X97.4	Y109.1						
G1	X96.65	Y109.725						
G1	X96.15	Y132.198						
G1	X95.115	Y138.553						
G1	X93.907	Y145.453						
G1	X93.675	Y152.415						
G1	X93.775	Y227.585						
G1	X94.307	Y234.547						
G1	X95.215	Y241.447						
G1	X95.425	Y247.802						
G1	X95.725	Y270.14						
G1	X84.275	Y270.275						
G1	X84.375	Y247.802						
G1	X84.985	Y241.447						
G1	X86.093	Y234.547						
G1	X86.325	Y227.585						
G1	X86.325	Y152.415						
G1	X85.993	Y145.453						
G1	X85.285	Y138.553						
G1	X84.975	Y132.198						
G1	X84.057	Y109.725						
G1	X96.675	Y109.725						
G1	X95.4	Y110.35						
G1	X95.0	Y132.113						
G1	X94.304	Y138.415						
G1	X93.286	Y145.376						
G1	X93.05	Y152.391						
G1	X93.15	Y227.609						
G1	X93.686	Y234.624						
G1	X94.404	Y241.585						
G1	X94.5	Y247.887						
G1	X95	Y269.515						
G1	X85.5	Y269.65						
G1	X85.5	Y247.887						
G1	X85.796	Y241.585						
G1	X86.614	Y234.624						
G1	X87.15	Y227.609						
G1	X87.05	Y152.391						
G1	X86.654	Y145.376						
G1	X86.096	Y138.415						
G1	X86.125	Y132.113						
G1	X85.225	Y110.35						
G1	X95.55	Y110.35						
G1	X94.15	Y110.974						
G1	X93.95	Y132.028						
G1	X93.394	Y138.278						
G1	X92.565	Y145.298						
G1	X92.226	Y152.368						
G1	X92.226	Y227.632						
G1	X93.065	Y234.702						
G1	X93.594	Y241.722						
G1	X93.676	Y247.972						
G1	X94.076	Y269.026						
G1	X86.75	Y269.026						
G1	X86.75	Y247.972						
G1	X86.806	Y241.722						
G1	X87.435	Y234.702						
G1	X87.874	Y227.632						
G1	X87.874	Y152.368						
G1	X87.235	Y145.298						
G1	X87.006	Y138.278						
G1	X87.175	Y132.158						
G1	X86.475	Y110.974						
G1	X94.026	Y110.974						
G1	X92.9	Y111.609						
G1	X92.7	Y131.941						
G1	X92.474	Y138.138						
G1	X91.835	Y145.219						
G1	X91.391	Y152.343						
G1	X91.491	Y227.657						
G1	X92.135	Y234.781						
G1	X92.574	Y241.862						
G1	X92.541	Y248.059						
G1	X92.741	Y268.391						
G1	X87.9	Y268.391						
G1	X87.9	Y248.059						
G1	X87.825	Y241.862						
G1	X88.065	Y234.781						
G1	X88.609	Y227.657						
G1	X88.609	Y152.343						
G1	X88.065	Y145.219						
G1	X88.025	Y138.138						
G1	X88.325	Y132.071						
G1	X87.725	Y111.609						
G1	X92.391	Y111.609						
G1	X91.65	Y112.243						
G1	X91.55	Y131.855						
G1	X91.43	Y137.998						
G1	X91.005	Y145.14						
G1	X90.857	Y152.319						
G1	X90.757	Y227.681						
G1	X91.305	Y234.86						
G1	X91.455	Y242.002						
G1	X91.391	Y248.145						
G1	X91.691	Y267.757						
G1	X88.75	Y267.757						
G1	X88.95	Y248.145						
G1	X88.995	Y234.86						
G1	X89.243	Y227.681						
G1	X89.243	Y152.319						
G1	X88.995	Y145.14						
G1	X89.045	Y137.998						
G1	X89.275	Y131.985						
G1	X88.975	Y112.243						
G1	X90.757	Y112.243						
G1	X90.4	Y112.877						
G1	X90.4	Y131.769						
G1	X90.123	Y152.295						
G1	X90.123	Y227.705						
G1	X90.641	Y267.123						
G1 Z0.15							
G1	X102.123	Y275.123						
G1	Z0							
G1	X110.123	Y275.123						
G1	X110.123	Y102.452	
G1	X99.15	Y102.452						
G1	X99.15	Y107.85						
								
								
;--- End G-code Begin ---
M400
M280 P0 S30
G4 P200
M280 P0 S90
M400
M104 S0 T0
M104 S0 T1
M106 P1 S0
M140 S0
G91
G1 Z20 F900
G90
G28
M530 S0
M204 S1000
M107
M104 S0
M140 S0
G92 E0
G1 E-2 F3000
G92 E0
G28
M104 S0
;--- End G-code End ---




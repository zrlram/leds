#!/usr/bin/env python

from math import sin, cos, pi, sqrt
from numpy import arange

# radius = 3.5      # inches
radius = 1.0        # unit sphere
#led_distnace = 0.63

lengths_top = [ 9, 6, 7, 6, 8, 6, 7, 6 ] 
lengths_bottom = [5] * 8
fillers = [0, 0, 0, 0, 3, 0, 0, 30]
bottom = 4 * (pi/2) /9

angles = [x for x in arange (-pi + bottom, 0, (pi / 2) / 9)]

lines = []
direction = 0
for slice, over in enumerate(arange(0, 2*pi, pi / 16)):
    top = lengths_top[slice % 8]
    bottom = lengths_bottom[slice%8]

    for upper_slice in range(top + bottom):
        correction = 9 - top 
        angle = angles[upper_slice]
        if direction:
            angle = angles[-(upper_slice+1+correction)]
        x = radius * cos(over) * sin(angle)
        y = radius * sin(over) * sin(angle)
        z = radius * cos(angle)
        #print angle, x, y, z
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' % 
                (x, y, z))

    for r in range(fillers[slice % 8]):
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' % 
                (0, 0, 0))

    direction ^= 1
        
print '[\n' + ',\n'.join(lines) + '\n]'


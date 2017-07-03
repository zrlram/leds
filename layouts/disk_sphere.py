#!/usr/bin/env python

from math import sin, cos, pi, sqrt

# TBD: convert into millimeters

#radiuses = [3.75, 3.65, 3.3, 2.85, 2]		# verify and convert
diameters = [194.0, 189.0, 169.0, 148.0, 106.0]		# verify and convert
radiuses = [x/2 for x in diameters]
# normed to 1!
led_distance = 16.0 / (radiuses[0])
radius_norm = [x/radiuses[0] for x in radiuses]
lines = []
lines2 = []
#height = 0.625 / (radiuses[0])				# convert
height = 16.0 / (radiuses[0])				# convert
z = height / 2	
for up in range(0, 5):

    r = radius_norm[up]
    circ = 2*pi*r
    # print circ/led_distance # how many LEDs in that row

    for led in range(1, int(round((circ / led_distance)))):
        x = r*sin(led)
        y = r*cos(led)
	
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
		(x, y, z))
        lines2.append('  {"point": [%.2f, %.2f, %.2f]}' %
		(x, y, -z))
    z = z + height

print '[\n' + ',\n'.join(lines)
print ','+ ',\n'.join(lines2) + '\n]'




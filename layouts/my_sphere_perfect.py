#!/usr/bin/env python

from math import sin, cos, pi, asin
from connection import row

# see also: http://blog.marmakoide.org/?p=1

r = 1
#row = [40, 40, 40, 32, 32, 32, 24, 24, 16, 8, 0]       # height- rows
#row = [40, 40, 32, 32, 24, 24, 24, 16, 16, 8, 0]       # 512 - multiples of 8
#row = [40, 36, 32, 32, 28, 24, 20, 16, 16, 12, 0]      
height = len(row)    # this is only half of the sphere
print row
lines = []
# Upper sphere first 
for up in range(0, height):
  z = (up+1) / float(height) - 0.07           # equidistant, not on circumference
  print z
  phi = asin(z) 
  # phi = ((pi / 2) / (height+1)) * (up+1)              # divide by 11 pieces
  for over in range(0, row[up]):                # index starts at 0
    theta = ((2 * pi) / row[up]) * over
    # print phi, theta
    x = r*cos((phi))*sin(theta)
    y = r*cos((phi))*cos(theta)
    #z = r*sin((phi)) - 0.07                    # sphere height, not equally spaced
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                (x, y, z))

# lower sphere
# MINUS one row here! We don't want the bottom one
for up in range(0, height-1):
  z = (up+1) / float(height) - 0.07           # equidistant, not on circumference
  phi = asin(z) 
  print -z
  for over in range(0, row[up]):                # index starts at 0
    theta = ((2 * pi) / row[up]) * over
    # print phi, theta
    x = r*cos((phi))*sin(theta)
    y = r*cos((phi))*cos(theta)
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                (x, y, -z))

print '[\n' + ',\n'.join(lines) + '\n]'

exit()
# lower sphere - OLD!!
for up in range(0, height):
  phi = ((pi / 2) / (height+1)) * (up+1)
  for over in range(0, row[up]):
    theta = ((2 * pi) / row[up]) * over
    # print phi, theta
    x = r*cos((phi))*sin(theta)
    y = r*cos((phi))*cos(theta)
    z = r*sin((phi)) - 0.07
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                (x, y, -z))

print '[\n' + ',\n'.join(lines) + '\n]'

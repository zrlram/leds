#!/usr/bin/env python

from math import sin, cos, pi, asin
from connection import row

# see also: http://blog.marmakoide.org/?p=1

r = 1
#row = [40, 40, 40, 32, 32, 32, 24, 24, 16, 8, 0] 	# height- rows
#row = [40, 40, 32, 32, 24, 24, 24, 16, 16, 8, 0] 	# 512 - multiples of 8
#row = [40, 36, 32, 32, 28, 24, 20, 16, 16, 12, 0] 	
height = len(row)    # this is only half of the sphere
lines = []

# z heights - measured on the orb
z_height = [ 5/8.0, 1.5, 2+2/16.0, 2+13/16.0, 3.5, 4, 4+7/16.0, 4+13/16.0 ]
# all in 16th inches, clockwise from front
row7_measures = [ [11, 13, 11, 13, 11], 
                  [13, 11, 16, 11, 14],
                  [14, 15, 11, 14, 11],
                  [15, 11, 12, 11, 15] ]
row6_measures = [ [11, 12, 10, 11, 11, 12, 11],
                  [11, 13, 11, 11, 11, 12, 11], 
                  [11, 12, 11, 11, 11, 11, 11],
                  [11, 14, 11, 11, 11, 11, 12]]
row5_measures = [ [11, 11, 11, 11],
                  [11, 13, 12, 11],
                  [11, 13, 12, 11],
                  [11, 12, 13, 11],
                  [11, 13, 13, 11],
                  [11, 11, 13, 11],
                  [11, 13, 13, 11],
                  [11, 13, 11, 14] ] 
row4_measures = [ [11, 11, 11, 11, 11, 13, 11, 11, 11],
                  [15, 11, 14, 11, 11, 11, 13, 11, 11],
                  [11, 11, 11, 13, 11, 11, 11, 13, 11], 
                  [11, 11, 13, 11, 11, 11, 12, 11, 14] ]
row3_measures = [ [11, 11, 11, 11, 11], 
                  [11, 11, 11, 11, 13],
                  [11, 12, 11, 11, 13],
                  [11, 13, 11, 11, 11],
                  [11, 12, 11, 11, 11],
                  [11, 13, 11, 11, 11],
                  [11, 12, 11, 11, 13],
                  [11, 13, 11, 11, 11] ]
row2_measures = [ [ 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], 
                  [ 11, 11, 11, 11, 13, 11, 11, 11, 11, 11, 11], 
                  [ 11, 11, 11, 11, 13, 11, 11, 11, 11, 11, 11], 
                  [ 11, 11, 11, 11, 14, 11, 11, 11, 11, 11, 10] ]
row1_measures = [ [ 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 13], 
                  [ 11, 11, 11, 11, 13, 11, 11, 11, 11, 11, 12], 
                  [ 11, 11, 11, 11, 11, 14, 11, 11, 11, 11, 11], 
                  [ 11, 11, 11, 11, 14, 11, 11, 11, 11, 11, 14] ]

def main():

    # Upper sphere first 
    for up in range(0, height):
      #z = (up+1) / float(height+1) - 0.07 		# equidistant, not on circumference
      z = z_height[up] / 5.0      # 5 being the full height
      phi = asin(z) 

      if up == 6:
          l = len(row7_measures)
          for i, quadrant in enumerate(row7_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/2) / s) * adding + i*pi/2
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 5:
          l = len(row6_measures)
          for i, quadrant in enumerate(row6_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/2) / s) * adding + i*pi/2
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 4:
          l = len(row5_measures)
          for i, quadrant in enumerate(row5_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/4) / s) * adding + i*pi/4
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 3:
          l = len(row4_measures)
          for i, quadrant in enumerate(row4_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/2) / s) * adding + i*pi/2
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 2:
          l = len(row3_measures)
          for i, quadrant in enumerate(row3_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/4) / s) * adding + i*pi/4
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 1:
          l = len(row2_measures)
          for i, quadrant in enumerate(row2_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/2) / s) * adding + i*pi/2
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      elif up == 0:
          l = len(row1_measures)
          for i, quadrant in enumerate(row1_measures):
              s = sum(quadrant) 
              adding = 0
              for distance in quadrant:
                  adding += distance
                  angle = ((pi/2) / s) * adding + i*pi/2
                  x = r*cos(phi)*sin(angle)
                  y = r*cos(phi)*cos(angle)
                  lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                                (x, y, z))
      else:

          # phi = ((pi / 2) / (height+1)) * (up+1)		# divide by 11 pieces
          for over in range(0, row[up]):		# index starts at 0
            theta = ((2 * pi) / row[up]) * over
            # print phi, theta
            x = r*cos((phi))*sin(theta)
            y = r*cos((phi))*cos(theta)
            #z = r*sin((phi)) - 0.07			# sphere height, not equally spaced
            lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                        (x, y, z))

    # lower sphere
    # MINUS one row here! We don't want the bottom one
    for up in range(0, height-1):
      z = z_height[up] / 5.0      # 5 being the full height
      phi = asin(z) 
      for over in range(0, row[up]):		# index starts at 0
        theta = ((2 * pi) / row[up]) * over
        # print phi, theta
        x = r*cos((phi))*sin(theta)
        y = r*cos((phi))*cos(theta)
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
            (x, y, -z))

    print '[\n' + ',\n'.join(lines) + '\n]'

if __name__ == "__main__":
    main()

'''
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
'''

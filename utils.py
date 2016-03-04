from connection import numLEDs, height, row
from math import pi

def get_angles(position):

    negative = False
    if position >= sum(row):     # numLeds/2 is not half the sphere!
        position = position - sum(row)
        negative = True

    up = 0
    over = 0
    remainder = 0
    for go_up in range(0, height):
        remainder += row[go_up]
        if remainder > position:
            up = go_up 
            over = position - (remainder - row[go_up])
            break

    phi = ((pi/2) / height) * up
    theta = ( 2*pi / row[up] ) * over
    if negative:
        phi = - phi - ( pi/2 / height )

    # print "phi, theta, up, over", phi, theta, up, over

    return (phi, theta)

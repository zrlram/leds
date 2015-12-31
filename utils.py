from connection import numLEDs, height, row
from math import pi

def get_angles(position):

    negative = False
    if position > (numLEDs / 2):
        position = position - (numLEDs / 2)
        negative = True

    up = 0
    over = 0
    remainder = 0
    for go_up in range(0, height + 1):
        remainder += row[go_up]
        if remainder > position:
            up = go_up 
            over = position - (remainder - row[go_up])
            break

    phi = ((pi/2) / height) * up
    theta = ( 2*pi / row[up] ) * over
    if negative:
        phi = - phi

    return (phi, theta)

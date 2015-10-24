#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from math import pi, cos, sin
from numpy import arange

#client = opc.Client('localhost:7890')
client = opc.Client('192.168.30.158:7890')

numLEDs = 512
pixels = [ (0,0,0) ] * numLEDs

# row = [40, 29, 19, 17, 16, 14, 12, 10, 8, 4, 0]    # height- rows
         # really a string of 40 -> 29 -> 19 ... -> 8 -> 4 LEDs

row = [40, 38, 35, 33, 30, 28, 24, 16, 10, 4, 0]   # height- rows
height = len(row)    # this is only half of the sphere
row.reverse()

def pixel(theta, phi):
    # LEDs are wired from top!!!

    if theta < 0 or theta > 2*pi:
        return -100
    # theta:  0, 2pi -- over
    # phi: -pi/2, pi/2 -- up

    up = int(abs(phi) / ((pi/2) / 10))           # -pi/2 --> pi/2 
        # up == 9: equator! up == 0: top - the one with 0 LEDs
    #over = int(round(theta / ((2 * pi) / row[up]) ))
    #  theta = ((2 * pi) / row[up]) * over

    over = int( round ((row[up] * theta) / (2*pi) ) )
    
    ups = 0

    if up ==1:
        print up
    for a in range(up+1):
        ups = ups + row[a]
        if up == 1: print row[a]
    position = ups + over

    if up == 1:
        print position, up, over, theta, phi
        return position
    return 0

#print pixel(0,0)
#print pixel(pi/2,0)
#print pixel(pi,0)
#print pixel(2*pi,0)
#print pixel(0,pi/2-0.001)

while True:
    # horizontally moving veritcal line :)

    for a in arange(0, 2*pi, pi/20):
        pixels = [ (0,0,0) ] * numLEDs
        for b in arange(-pi/2+0.001, pi/2-0.001, pi/10):   
            pixels[pixel(a, b)] = (190, 150, 200)

        client.put_pixels(pixels)
        time.sleep(0.2)

'''
# equator ring
for a in arange(0, 2*pi, pi/20):
    pixels = [ (0,0,0) ] * numLEDs
    #for b in arange(-pi/2+0.001, pi/2-0.001, pi/10):   
    pixels[pixel(a, pi/2-0.0001)] = (190, 50, 100)

    client.put_pixels(pixels)
    time.sleep(0.2)
'''


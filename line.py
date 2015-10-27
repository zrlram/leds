#!/usr/bin/env python

import opc, time
from sphere_pixel import *
from math import pi
from numpy import arange

#client = opc.Client('localhost:7890')
client = opc.Client('192.168.30.158:7890')

numLEDs = 513
pixels = [ (0,0,0) ] * numLEDs

#row = [40, 40, 40, 32, 32, 32, 24, 24, 16, 8, 0]  
#height = len(row) - 1    # this is only half of the sphere
                         # -1 because the height is minues one! LOL

# start with reset
client.put_pixels(pixels)

def horizontal_ring(up):
    phi = (pi/2) / height * up
    for a in arange(0,2*pi, pi/20):
        pixels[pixel(a,phi)[0]] = (200, 100, 5)

    client.put_pixels(pixels)

# horizontal_ring(2)

#for up in range(0,height):
#    horizontal_ring(up)
#    time.sleep(0.5)

def equator_pixels():
    for a in arange(0,2*pi, pi/20):
        pixels[pixel(a, 0)[0]] = (190, 150, 200)

    client.put_pixels(pixels)

#equator_pixels()

def vertical_median_line():

    for b in arange(-pi/2, pi/2, pi/20):
        pixels[pixel(0, b)[0]] = (190, 150, 200)
        client.put_pixels(pixels)

#vertical_median_line()

def vertical_ring(over, color=None):
    # over we define as seen on the equator
    theta = (2*pi)/row[0] * over
    if color: color = (color, color, color)
    else: color = (6*over, 6*(80-over), 200)
    for b in arange(-pi/2,pi/2, pi/20):
        pixels[pixel(theta,b)[0]] = color

    client.put_pixels(pixels)

vertical_ring(0)
vertical_ring(1, 180)
vertical_ring(2, 250)
vertical_ring(3, 150)
vertical_ring(4, 250)
exit()

for over in range(0,row[0]):
    vertical_ring(over)
    pixels = [ (0,0,0) ] * numLEDs
    time.sleep(0.1)

def vertical_line():
    for a in arange(0, 2*pi, pi/20):
        pixels = [ (0,0,0) ] * numLEDs
        #for b in arange(-pi/2+0.001, pi/2-0.001, pi/10):   
        for b in arange(0, pi/2-0.001, pi/20):   
            pixels[pixel(a, b)[0]] = (190, 150, 200)

        client.put_pixels(pixels)
        time.sleep(0.2)


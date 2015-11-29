#!/usr/bin/env python

from connection import pixels, row, height, numLEDs
from math import pi, ceil, floor, sqrt
import colorsys

 
def pixel_absolute(up, over):
    if up == 0: up = 1

    row_index = abs(up) - 1

    if (over < 0): over = row[row_index] + over
    if (over > row[row_index]): over = row[row_index]
    
    ups = 0
    for a in range(row_index):
        ups = ups + row[a]
    position = ups + over

    # lower half:
    if (up<0): position = position + sum(row) 
    if (position >= numLEDs): position = numLEDs-1

    #print position, up, over
    return position 

def set_pixel(theta, phi, color):
    pixel[pixel(theta,phi)] = color

def set_pixel_i(i, color):
    pixel[i] = color

def rgb_intensity(color, intensity):
    c = [x/255.0 for x in color]
    (h,s,v)= colorsys.rgb_to_hsv(c[0], c[1], c[2])
    (r, g, b) = colorsys.hsv_to_rgb(h, s, intensity)
    (r, g, b) = [int(x*255) for x in r, g, b]
    return (r,g,b)


def pixel_faded(theta, phi, color):

    #print "theta:", theta, "phi:", phi
    up = phi / (pi/2) * height     # -pi/2 --> pi/2 
    bottom = int(floor(up))
    top = int(ceil(up))

    # work on top row first
    row_index = abs(top) - 1
    if row_index<0: row_index=0
    over = (row[row_index] * theta) / (2*pi)
    left = ceil(over)
    right = floor(over)

    # top right LED
    dist_over = abs(right - over)  
    dist_up = (top - up)       
    dist = sqrt(dist_over**2 + dist_up**2)
    color = rgb_intensity(color, 1-dist)

    #print "TOP RIGHT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "row[row_index]:", row[row_index]
    #print "color" , color
    pixels[pixel_absolute(top, int(floor(over)))] = color

    # top left LED
    dist_over = abs(left - over)  # no division needed! we are already in coords
    dist = sqrt(dist_over**2 + dist_up**2)
    color = rgb_intensity(color, 1-dist)

    #print "TOP LEFT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    pixels[pixel_absolute(top, int(ceil(over)))] = color

    # work on bottom 
    row_index = abs(bottom) - 1
    if row_index<0: row_index=0
    over = (row[row_index] * theta) / (2*pi)

    # bottom right LED
    dist_over = abs(right - over)  # no division needed! we are already in coords
    dist_up = abs(bottom - up)       
    dist = sqrt(dist_over**2 + dist_up**2)
    color = rgb_intensity(color, 1-dist)

    #print "BOT RIGHT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    pixels[pixel_absolute(top, int(floor(over)))] = color

    # top left LED
    dist_over = abs(left - over)  # no division needed! we are already in coords
    dist = sqrt(dist_over**2 + dist_up**2)
    color = rgb_intensity(color, 1-dist)

    #print "BOT LEFT", "up", up, "over", over
    #print "dist_over:", dist_over, "dist_up", dist_up, "dist", dist
    #print "color" , color
    pixels[pixel_absolute(top, int(ceil(over)))] = color


def pixel(theta, phi):
    # LEDs are wired from equator up (40 -> 38 -> ... -> 4)

    # do some boundary checking on the angles
    #
    # theta:  0, 2pi -- over
    # phi: -pi/2, pi/2 -- up
    # phi = 0 is strange because we don't have an equator
    #         we could convention that to light up up=+1
    #
    # TBD
    #if (phi==0): phi=0.001
   
    up = int( round( phi / (pi/2) * (height) ) )    # -pi/2 --> pi/2 
        # up == 0: equator! (which does not exist) up == height: top - the one with 0 LEDs
    if up == 0: up = 1

    row_index = abs(up) - 1
    over = int( round( (row[row_index] * theta) / (2*pi) ) )
    # in some cases, we get over the boundary because of rounding
    # e.g., theta = 6.14, row[row_index]=20

    return pixel_absolute(up, over)


def test_pixel():

    # (theta, phi, up, over, position))

    # note: row[:2] means elements up to 2, but don't include 2
    test_tuples = [
                   (0, 0, 0, 0, 0), 
                   (0, pi/2, height, 0, sum(row)), 
                   (0, pi/4, round(float(height)/2), 0, sum(row[:int(round(float(height)/2))]) ),
                   (0, pi/20, 1, 0, row[0]),
                   (0, 2*pi/20, 2, 0, sum(row[:2])),

                  ]

    for tuple in test_tuples:
        theta = tuple[0]
        phi = tuple[1]
        up_test = tuple[2]
        over_test = tuple[3]
        position_test = tuple[4]
        (position, up, over) = pixel(theta, phi)
        print "theta: %s, phi: %s, up: %s, over: %s, position: %s, test: %s" % (
              theta, phi, up, over, position,  
              up_test==up and over_test==over and position_test==position)

#test_pixel()


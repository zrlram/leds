#!/usr/bin/env python

import model
from math import log, pi, tan
from connection import height, row, numLEDs, draw as conn_draw, pixels
import operator
from utils import get_angles
from morph import color_transition

mod = model.Model('sphere_10.json')
mod.clear()
conn_draw()

class Mercator:
    ''' Mercator works different from normal shaders. We don't want to look up 
        for each x,y,z triple what the value is from the x-y map. That won't 
        fill the sphere correclty. 
        That is, however, how the shaders work. We need the inverse of that. We 
        want to go through each point on the map and map it to the globe! Hence
        not using the shader approach. '''

    pixel_xy = [ (0,0) ] * numLEDs
    image = []
    maxx = 43           # starting at 0
    maxy = 22 
    pixel_xy2 = [[ 0 
          for c in range(maxy+1)] 
          for r in range(maxx+1)]

    ''' From: https://github.com/mbostock/d3/blob/master/src/geo/mercator.js
        
        function d3_geo_mercator(theta, phi) {
          return [theta, Math.log(Math.tan(pi / 4 + phi / 2))];
        }

        d3_geo_mercator.invert = function(x, y) {
          return [x, 2 * Math.atan(Math.exp(y)) - pi/2];
        };

    '''

    # pre-compute for each LED what coordinates it maps to
    for i, pixel in enumerate(pixel_xy):

        # phi: up | theta: around
        (phi, theta) = get_angles(i)

        # Mercator
        #phi_mapped = log ( tan ( pi/4 + phi / 2))
        phi_mapped = phi        # up
        theta_mapped = theta    # over

        # scale x and y
        up = int(phi_mapped / (pi/2/height)) 
        if up>=0:
            row_index = up 
        else:
            row_index = abs(up) - 1
        y = up + height      # move 0 point up
        x = int(theta_mapped / (2*pi/(row[0])) )
        #print "up, t, r[up]", up, theta_mapped, row[row_index]
        
        #print "x,y", x,y
        pixel_xy[i] = (x,y) 
        pixel_xy2[x][y] = i
        print i, (x,y)

        #if maxx < x: maxx=x
        #if maxy < y: maxy=y
    
    # print maxx, maxy

    @staticmethod
    def map():

        # cannot do by pixel, but have to go by coordinates in the picture 
        # and find the nearest neighbor to map to and do that 'faded'
        for x in range(Mercator.maxx):
            for y in range(Mercator.maxy):
                i = Mercator.pixel_xy2 [x] [y]

                if i>0:
                    # only divide by two if there was a dot there already!
                    if pixels[i] > (0,0,0):
                        t = color_transition(pixels[i], Mercator.image[x][y], steps=2)
                        pixels[i] = t.next()
                        pixels[i] = t.next()
                    else:
                        pixels[i] = Mercator.image[x][y]

                    print "after",i, tuple(pixels[i]), "plus", tuple(Mercator.image[x][y])

        # go through a second time and update the ones that didn't have a direct mapping
        # TBD: Somehow, one of those (4,10), (4,11), (4,12) is not mapped right?!)
        for x in range(Mercator.maxx):
            for y in range(Mercator.maxy):
                i = Mercator.pixel_xy2 [x] [y]

                if i==0:
                    print "updating in second loop: ", x, y
                    # now it's getting interesting. We don't have a pixel defined for this (x,y)
                    values = Mercator.image[x][y]           # get color at this position

                    i2 = Mercator.pixel_xy2 [x-1][y]         # try and see if we have a point for an adjacent coordinate
                    if i2>0:
                        # get the color from i2, but update pixel at position i AND i2
                        t = color_transition(pixels[i2], values, steps=2)
                        #pixels[i] = t.next()
                        #pixels[i] = t.next()
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()
                        #pixels[i] = tuple(map(operator.add, pixels[i], values))     # smear the value to the adjacent guy
                        #pixels[i] = tuple(map(operator.div, pixels[i], (2,2,2)))

                    i2 = Mercator.pixel_xy2 [x+1][y]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()

                    '''
                    i2 = Mercator.pixel_xy2 [x-1][y-1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()
                    
                    i2 = Mercator.pixel_xy2 [x][y-1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()

                    i2 = Mercator.pixel_xy2 [x+1][y-1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()

                    i2 = Mercator.pixel_xy2 [x+1][y+1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()

                    i2 = Mercator.pixel_xy2 [x][y+1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()

                    i2 = Mercator.pixel_xy2 [x-1][y+1]
                    if i2>0:
                        t = color_transition(pixels[i2], values, steps=2)
                        pixels[i2] = t.next()
                        pixels[i2] = t.next()
                    '''
                    
                    # print "pi", i, pixels[i][0], pixels[i][1], pixels[i][2]



        '''
         for i, pixel in enumerate(pixels):
             x = Mercator.pixel_xy[i][0]
             y = Mercator.pixel_xy[i][1]
             #print i, x, y
             pixels[i] = Mercator.image [ x ] [ y ]
        '''

    @staticmethod
    def read_bmp():
        f = open ('raffy.bmp', 'r')
        count = 0
        img = [[(0,0,0) for col in range(23)] for row in range(44)]
        color = ()
        red = 0 
        green=0
        blue=0
        for line in f.readline():
            for l in line:
                count = count + 1
                if count>3: 
                    if count>1630: break
                    if (count-5) % 3 == 1: red = ord(l)
                    if (count-5) % 3 == 2: green = ord(l)
                    if (count-5) % 3 == 0: 
                        blue = ord(l)
                        color=(red,green,blue)
                        #print count, count/3/17, (count/3) %17
                        img[int(count/3 / 17)][(count/3) % 17] = color
                        #print color
        #print count
        Mercator.image = img

    @staticmethod
    def draw():
        conn_draw() 

    @staticmethod
    def run():
        img = [[(0,0,0) 
                for c in range(Mercator.maxy+1)] 
                for r in range(Mercator.maxx+1)]

        #img [4][1] = (255,0,0)
        #img [4][2] = (255,0,0)
        #img [4][3] = (255,0,0)
        #img [4][4] = (255,0,0)
        #img [4][5] = (255,0,0)
        #img [4][6] = (255,0,0)
        #img [4][7] = (255,0,0)
        #img [4][8] = (255,0,0)
        #img [4][9] = (255,0,0)
        #img [4][10] = (255,0,0)
        img [4][11] = (255,0,0)
        img [4][12] = (255,0,0)
        #img [0][7] = (255,0,0)
        #img [0][8] = (255,0,0)
        #img [0][9] = (255,0,0)
        #img [0][10] = (255,0,0)
        Mercator.image = img

        # Mercator.read_bmp()
        Mercator.map()
        Mercator.draw()
        exit()

        Mercator.read_bmp()
        Mercator.map()
        Mercator.draw()
        exit()

        #print "------ angle: up and over x: over" 

        #print "0",Mercator.pixel_xy[0], get_angles(0)
        #print "1",Mercator.pixel_xy[1], get_angles(1)
        #print "10",Mercator.pixel_xy[10], get_angles(10)
        #print "32", Mercator.pixel_xy[32], get_angles(32)
        #print "33", Mercator.pixel_xy[33], get_angles(33)
        #print "34", Mercator.pixel_xy[34], get_angles(34)
        #print "64", Mercator.pixel_xy[64], get_angles(64)
        #print "65", Mercator.pixel_xy[65], get_angles(65)
        #print get_angles(0)
        #print get_angles(10)
        #print get_angles(33)
        #print get_angles(100)
        #print get_angles(300)

Mercator.run()


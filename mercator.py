#!/usr/bin/env python

import model
from math import sin, cos, log, acos, atan, pi, asin

mod = model.load_model('sphere_10.json')

class Mercator:
    ''' Mercator works different from normal shaders. We don't want to look up 
        for each x,y,z triple what the value is from the x-y map. That won't 
        fill the sphere correclty. 
        That is, however, how the shaders work. We need the inverse of that. We 
        want to go through each point on the map and map it to the globe! Hence
        not using the shader approach. '''

    image = []

    def mercator_shader(self, p):

        # maps (x,y,z) => (x,y) for the lookup in the image

        # 1. compute theta and phi from (x,y,z)

        x_ = p['point'][0]
        y_ = p['point'][1]
        z_ = p['point'][2]

        # go to spherical coordinateu
        phi = asin(z_)              # acos this maps from [-1,1] -> [pi,0]
                                    # need to map [-1,1] -> [-pi/2,pi/2] --> asin
        if x_ == 0: x_ = 0.00001
        theta = atan(y_/x_)

        # mercator
        # x = phi

        #x = (0.5 * log ( ( 1 + sin (theta)) / (1 - sin (theta))) + 2*pi) / (4*pi)
        #x = min(x, 1)
        # PROBLEM: with this math, we don't hit all the points on the x-y map!
        # pre-compute for each point on the map what the point on the globe is!
        x = (theta + pi/2) / (pi)
        y = (phi + (pi/2)) / pi              # normalize to [0,1]

        #print "x", theta, phi, "from:",x_,y_,z_

        # scale to the size of the image projected
        x = x * len(self.image)   # cols
        y = y * len(self.image[0])      # rows

        #if self.image[int(x)][int(y)][0] > 0:
        print x_, y_, z_, '->', int(x), int(y), '(', theta, phi, ')'

        return self.image[int(x)-1][int(y)-1]

    def box(self):

        img = [[(0,0,0) for col in range(17)] for row in range(32)]
        img [0][0] = (255,0,0)
        img [0][1] = (255,0,0)
        img [1][5] = (255,0,0)
        #img [15][3] = (255,0,0)
        img [5][5] = (255,0,0)
        img [1][1] = (255,0,0)
        #img [2][2] = (255,0,0)
        #img [3][3] = (255,0,0)
        #img [4][4] = (255,0,0)
        #img [6][6] = (255,0,0)
        self.image = img
            
    def draw(self):
        model.map_pixels(mod)

mercator = Mercator()
model.register_shader(mercator.mercator_shader)
mercator.box()
mercator.draw()


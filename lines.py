#!/usr/bin/env python

import model
#from sphere_pixel import *
from connection import pixels, draw
from numpy import arange
import numpy as np
from math import sin, cos, pi, sqrt, exp, log
from matplotlib.pyplot import cm
from matplotlib import colors
import time, copy

mod = model.load_model('sphere_10.json')

class Lines:

    @staticmethod 
    def hor_line_shader(p, **kwargs):

        z = p['point'][2]
        dz = kwargs.get('dz',0)
        dist_z = 5 * abs(z - dz)   # trail - small is large tail

        hue = 0.7
        sat = 0.8
        value = dist_z

        return model.hsv(hue, sat, 1-value)

    @staticmethod 
    def vert_line_shader_additive(p, **kwargs):

        x = p['point'][0]
        dx = kwargs.get('dx',0)
        dist_x = 10 * abs(x - dx)   # trail - small is large tail
                                    # 10 * [-1-1, 1+1]

        if (dist_x < 1):
            hue = dx
            sat = 0.8
            value = dist_x
            return model.hsv(hue, sat, 1-value)
        else:
            return (0,0,0)


    @staticmethod 
    def vert_line_shader(p, **kwargs):

        x = p['point'][0]
        dx = kwargs.get('dx',0)
        dist_x = 10 * abs(x - dx)   # trail - small is large tail

        hue = dx
        sat = 0.8
        value = dist_x

        return model.hsv(hue, sat, 1-value)

    @staticmethod 
    def plane_shader(p, **kwargs):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]
        dist_in = kwargs.get('dist',0)
        #print dist_in

        # Ax+By+Cz+D = 0 --> plane
        # a bit of math: http://mathworld.wolfram.com/Plane.html
        dist = 0
        (A, B, C, D) = (dist_in, dist_in, 1, dist_in)
        actual_dist = (A*x+B*y+C*z+D) / sqrt(A**2+B**2+C**2)
        if abs(actual_dist) < 0.2:         # to give it some margin
            dist = actual_dist * 10

        hue = 0.5
        sat = 0.8
        value = abs(dist)

        return model.hsv(hue, sat, value)

    def __init__(self):
        # for gravity 
        self.y = 1     #initial high of the ball
        self.v = 1     #initial velocity of the ball
        self.e = 0.9   #coef. lost of energy in each bounce
        self.k = 0.2   #friction with air
        self.g = -9.81 #aceleration of gravity
        self.previous_t = 0
        
    def gravity_hor_falling(self):

        now = time.time() * 1000      # millis
        if self.previous_t==0:
            self.previous_t = now
        # dt = 0.006  increase of time for each iteration
        dt = (now - self.previous_t) / 1000.0
        #print dt

        dv = self.g*dt - self.k*self.v*dt
        self.v = self.v + dv

        dy = self.v * dt
        self.y = self.y + dy

        #Bounce conditions
        if  self.y < -1:
            self.v = -self.v*self.e

        #print y
        model.map_pixels(Lines.hor_line_shader, mod, dz=self.y)

        self.previous_t = now


    @staticmethod 
    def faded_hor_line():
        # updated to work with model and time-based!

        speed = 1000.0                # 2 seconds for -1 to 1 (entire pheree)
        now = int(time.time() * 1000)     # millis
        dist = cos(now/speed) 
        model.map_pixels(Lines.hor_line_shader, mod, dz=dist)

    @staticmethod 
    def faded_vert_line():
        speed = 500.0                
        now = int(time.time() * 1000)     
        dist = cos(now/speed) 
        model.map_pixels(Lines.vert_line_shader_additive, mod, dx=dist)

    @staticmethod 
    def plane_angles():
        speed = 1000.0                
        now = int(time.time() * 1000)     
        #dist = cos(now/speed)
        dist = abs((now/speed % 4)-2) - 1
        model.map_pixels(Lines.plane_shader, mod, dist=dist)
        
#iterations = 10000
#for i in range(iterations):
    #Lines.faded_vert_line()
    #Lines.plane_angles()
    #time.sleep(0.02)



m = cm.ScalarMappable(cmap=cm.rainbow)
rainbow_scale = [x for x in m.to_rgba(np.linspace(0,1,18))]
rainbow = []
for el in rainbow_scale:
    rainbow.append(tuple([int(x*256) for x in el][:3]))

    @staticmethod
    def sine_wave(color=(90,150,200)):
        amplitude = 1.8 
        frequency = 4
        for phi in arange(0,2*pi+0.001, pi/22):
            #pixels[pixel(phi,sin(phi*frequency)/amplitude)] = color
            pixel_faded(phi,sin(phi*frequency)/amplitude, color)
            draw()

    @staticmethod
    def moving_sine_wave(color=(90,150,255), iterations=20):
        amplitude = 1.8
        frequency = 4
        for offset in arange(0, iterations, 0.05):
            for phi in arange(0,2*pi+0.001, 2*pi/row[0]):
                #pixels[pixel(phi,sin(phi*frequency)/amplitude)] = color
                pixel_faded(phi,sin((phi+offset)*frequency)/amplitude, color)
            draw()
            for pixel in range(numLEDs):
                pixels[pixel] = (0,0,0)
            time.sleep(0.05)

    @staticmethod
    def laser_sine_wave(color=(90,150,255), iterations=20):
        amplitude = 1.8
        frequency = 4
        for phi in arange(0,2*pi+0.001, 2*pi/row[0]):
            #pixels[pixel(phi,sin(phi*frequency)/amplitude)] = color
            color_laser = (255,255,0)
            pixel_faded(phi-2*pi/row[0],sin((phi-2*pi/row[0])*frequency)/amplitude, color)
            pixel_faded(phi,sin((phi)*frequency)/amplitude, color_laser)
            draw()
            time.sleep(0.1)


    @staticmethod
    def sine2():
        millis = int(round(time.time() * 1000))

        pixel = 0
        for up in range(2*height):
            for i in range (0, row[up % 2]):
                t = i * 0.2 + millis * 0.002
                red = int(128 + 96 * sin(t))
                green = int(128 + 96 * sin(t + 0.1))
                blue = int(128 + 96 * sin(t + 0.3))
                if pixel >= numLEDs: break
                pixels[pixel] = (red, green, blue)
                pixel += 1 

        draw()

    @staticmethod
    def black_fade_white_pole_rings(color = (0,0,0), wait=0.07, center=True):

        for iteration in range(len(row)):
            ring = len(row)-iteration
            if center:
                ring = iteration
            Lines.horizontal_ring(ring, color)
            Lines.horizontal_ring(-ring, color)
            time.sleep(wait)


    @staticmethod
    #def put_pattern(pattern, iterations=numLEDs, wait=0.05):
    def put_pattern(pattern, iterations=496, wait=0.05):
        ''' put the pattern on the sphere and run it up '''
        memory = copy.copy(pixels)    # remember initial state

        for iterate in range(iterations+1):
            # reset
            for (i, p) in enumerate(memory):
                pixels[i] = p

            # put pattern on
            for (i, element) in enumerate(pattern):
                pixels[iterate+i] = element

            draw()
            time.sleep(wait)

    @staticmethod
    #def count_up(color=(190,150,200), wait=0.05, dots=numLEDs, fade=0, iterations=20):     
    def count_up(color=(190,150,200), wait=0.05, dots=496, fade=0, iterations=20):     
        # build a color pattern as a line and put it on sphere
        # dots: how many dots should be lit up? numLEDs meaning don't remove any, but fill sphere
        # fade: how many pixels in beginning and end should be faded out 
        
        pattern = [color] * dots      # the final pattern / line

        # build colors for fading
        black = (0,0,0)
        cols=[black, [c/256.0 for c in color]]
        m = colors.LinearSegmentedColormap.from_list('ram',cols)
        cs = colors.makeMappingArray(fade+2, m)

        for (i, element) in enumerate(cs[1:-1]):      # get rid of the black and itself and the element itself too
            led = tuple([int(x*256) for x in element][:3])
            pattern[i] = led
            pattern[dots-i-1] = led

        Lines.put_pattern(pattern, wait=wait, iterations=iterations) 

    ''' move a pixel around in a circle at a certain height '''
    @staticmethod
    def go_around(up):     
        phi = (pi/2) / height * up
        for a in arange(0,2*pi,pi/22):
            pixels[pixel(a,phi)] = (90, 150, 200)
            draw()
            time.sleep(0.01)

    ''' make a ring at a certain height '''
    @staticmethod
    def horizontal_ring(up, color=(100,150,125)):

        for over in range(0, row[abs(up)-1]):
            pixels[pixel_absolute(up, over)] = color
        draw()


    @staticmethod
    def little_laser():
        color = (255,0,0)
        iterations = 20
        for iteration in range(iterations):
            for theta in arange(0, 2*pi/row[0]+0.001, 0.001):
                phi = ((pi/2 / height / (2*pi/row[0])) * theta) + 2*pi/2/height
                pixel_faded(theta, phi, color)
                draw()
                time.sleep(0.01)
            #for theta in arange(2*pi/row[0]+0.001, 0, -0.001):
                #phi = (2*pi/row[0] / pi/2 / height * theta) + 2*pi/2/height
                #pixel_faded(theta, phi, color)
                #draw()

    @staticmethod
    def color(inside, phase):

        import math
        if inside:
            phase += 1.4
        b_phi = phase

        brightness = (math.sin(b_phi*2*math.pi)+1.)**2 / 4.
        
        r, g, b = ( (math.sin((phase/3+x)*2*math.pi)+1.)/2. for x in (0./3, 1./3, 2./3) )
        r, g, b = ( x*brightness for x in (r,g,b) )

        return int(r*255),int(g*255),int(b*255)

    @staticmethod
    def vertical_median_line():
        for b in arange(-pi/2, pi/2+0.001, pi/2/height):
            pixels[pixel(0, b)] = (190, 150, 200)
            draw()

    @staticmethod
    def vertical_ring_skip(angle=pi/4):
        for theta in arange(0, 2*pi, angle):
            for phi in arange(-pi/2, pi/2+0.001, pi/2/height):
                color = (int(abs(60*phi)), int(60*(pi-phi)), 200)
                color=(200,200,200)
                pixels[pixel(theta,phi)] = color
            draw()
            time.sleep(0.2)


    @staticmethod
    def vertical_ring_skip_fade():
        ''' needs fixing  '''
        return False
        stage = 0       # we are going through 4 stages
        threshold = pi/2
        for theta in arange(0, 2*pi, pi/16):
            if (stage==0):      # just one line, erase all other
                color=(200,200,200)
                threshold = pi/2
            if (stage==1):      # keep solid line and add faded smaller line
                color = (120,120,120)
                threshold = pi/4
            if (stage==2):      # add yet another solid line
                color=(200,200,200)
                threshold = pi/2
            if (stage==3):      # fade on the back, remove first solid line
                color = (0,0,0)
                threshold = pi/2
                theta = theta - (3 * pi / 16);
                for phi in arange(-threshold, threshold, pi/22):
                    pixels[pixel(theta,phi)] = color
                draw()
                time.sleep(0.4)
                theta = theta + (3 * pi / 16);
                color=(120,120,120)
                threshold = pi/4
                
            stage = (stage + 1) % 4 

            for phi in arange(-threshold, threshold, pi/22):
                pixels[pixel(theta,phi)] = color
                
            draw()
            time.sleep(0.4)

    #vertical_ring_skip_fade()

    @staticmethod
    def vertical_ring(over, color=None):
        # over we define as seen on the equator
        theta = (2*pi)/row[0] * over
        if color: color = (color, color, color)
        else: color = (6*over, 6*(80-over), 200)
        for b in arange(-pi/2,pi/2+0.001, pi/2/height):
            pixels[pixel(theta,b)] = color

        draw()


    @staticmethod
    def vertical_line_over():
            for over in range(0,row[0]):
                try:
                    vertical_ring(over)
                    pixels = [ (0,0,0) ] * numLEDs
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    raw_input("Press Enter to continue...")
                except:
                    pass 

    @staticmethod 
    def vertical_line():
        for a in arange(0, 2*pi, pi/22):
            for b in arange(0, pi/2, pi/22):   
                pixels[pixel(a, b)] = (190, 150, 200)

            draw()
            time.sleep(0.2)

    @staticmethod 
    def faded_vert_line():

        color = (255,0,0)

        for theta in arange(0, 2*pi, 0.005):
            # arange does not include the last value!
            for phi in arange(-pi/2, pi/2+0.001, pi/2/height):   
                pixel_faded(theta % 2*pi, phi, color)

            draw()
            for pixel in range(numLEDs):
                pixels[pixel] = (0,0,0) 
            #raw_input("Press Enter to continue...")
            #time.sleep(0.05)

    @staticmethod
    def run_all():

        Lines.faded_hor_line()
        exit()
        Lines.faded_hor_line()
        for i in range(1,100):
            Lines.sine2()
            time.sleep(0.2)
        Lines.laser_sine_wave(iterations=2)
        Lines.moving_sine_wave(iterations=2)
        Lines.faded_vert_line()
        for up in range(-height,height+1):      # range does not include last
            Lines.horizontal_ring(up)
            time.sleep(0.3)
        Lines.go_around(1)
        Lines.count_up(dots=10, wait=0.1, color=(20,40,200), fade=2)
        Lines.put_pattern(Lines.rainbow, iterations=100)
        Lines.black_fade_white_pole_rings(color=(255,53,151))
        Lines.black_fade_white_pole_rings(color=(255,0,21), center=False)
        Lines.sine_wave()
        Lines.vertical_ring(1, 80)               # TBD!
        Lines.vertical_ring(2, 250)
        Lines.vertical_ring(3, 150)
        Lines.vertical_ring(3, 250)
        for i in range(1,3):
            Lines.vertical_ring_skip(pi/4)    # pi/4 is optimal for the sphere we have with skips
            #Lines.vertical_ring_skip_fade()  
        Lines.vertical_median_line()
        Lines.horizontal_ring(-10)
        Lines.horizontal_ring(-1)
        Lines.horizontal_ring(1)
        Lines.horizontal_ring(10)


#lines = Lines()
#for i in range(5000):
#    lines.gravity_hor_falling()

for i in range(1000):
    Lines.faded_vert_line()
    

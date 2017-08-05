#!/usr/bin/env python

from color import hsv, rgb_to_hsv, rainbow_
import random
from math import sin, pi, cos, sqrt

import looping_shader_show

class MultiVerticalLine(looping_shader_show.LoopingShaderShow):

    name = "Multi Vertical Line"
    controls = { 'Trail Length': [0.1, 1, 0.5, 0.01], 
                 'color': 'color',
                 'rainbow': 'checkbox'
                 }
    
    # not ready
    ok_for_random = False


    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)
        self.dx = 0
        # configurable controls
        self.trail = 1
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.rainbow = 1
        self.prog = 0
        self.sign = 1
        self.angle = 0.0

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    def shader(self, p):

        x = p[0]
        y = p[1]
        z = p[2]

        # shape tilt
        x_ = x*cos(self.angle)-z*sin(self.angle)
        y_ = z*sin(self.angle)+x*cos(self.angle)
        z_ = y

        dist = sqrt(x_**2 + y_**2 + z_**2)
        print dist

        if dist < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            #dist = dist / self.trail

            return hsv (color_hsv[0], color_hsv[1], dist)
        else:
            return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        self.angle += random.random() * 0.1 % (2 * pi)

        if (loop_instance % 2):
            # one side
            self.dx = 1 - 2 * progress
        else:
            # other side
            self.dx = - (1 - 2 * progress)

        if self.rainbow:
            self.prog = self.prog + (random.random()*0.05) % 1
            self.color = rainbow_(self.prog, loop_instance, self.cm.brightness)
            #self.color = rainbow[int(loop_instance%len(rainbow))]


__shows__ = [
              (MultiVerticalLine.name, MultiVerticalLine)
            ]


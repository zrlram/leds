#!/usr/bin/env python

from color import hsv, rgb_to_hsv

import looping_shader_show

class VerticalLine(looping_shader_show.LoopingShaderShow):

    name = "Vertical Line"
    controls = { 'Trail Length': [0, 10, 5], 'color': 'color' }


    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)
        self.dx = 0
        # configurable controls
        self.trail = 5
        self.color = (50,50,255)

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.custom_range_value

    def shader(self, p):

        x = p['point'][0]
        dist_x = self.trail * abs(x - self.dx)   # trail - small is large tail

        color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
    
        return hsv (color_hsv[0], color_hsv[1], 1-dist_x)

    def update_at_progress(self, progress, new_loop, loop_instance):

        if (loop_instance % 2):
            # one side
            self.dx = 1 - 2 * progress
        else:
            # other side
            self.dx = - (1 - 2 * progress)


__shows__ = [
              (VerticalLine.name, VerticalLine)
            ]


#!/usr/bin/env python

from color import hsv, rgb_to_hsv, rainbow

import looping_shader_show

class VerticalLine(looping_shader_show.LoopingShaderShow):

    name = "Vertical Line"
    controls = { 'Trail Length': [0.1, 1, 0.5, 0.01], 
                 'color': 'color',
                 'rainbow': 'checkbox'
                 }


    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)
        self.dx = 0
        # configurable controls
        self.trail = 0.5
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.rainbow = 0

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    def shader(self, p):

        x = p['point'][0]
        dist_x = abs(x - self.dx)   # trail - small is large tail

        if dist_x < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_x = dist_x / self.trail

            return hsv (color_hsv[0], color_hsv[1], 1-dist_x)
        else:
            return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        if (loop_instance % 2):
            # one side
            self.dx = 1 - 2 * progress
        else:
            # other side
            self.dx = - (1 - 2 * progress)

        if self.rainbow:
            self.color = rainbow[int(loop_instance%len(rainbow))]


__shows__ = [
              (VerticalLine.name, VerticalLine)
            ]


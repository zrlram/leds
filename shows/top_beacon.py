#!/usr/bin/env python

from color import hsv, rgb_to_hsv
import color as col
from collections import OrderedDict

import looping_shader_show

class Top_Beacon(looping_shader_show.LoopingShaderShow):

    name = "Top Beacon"

    controls = OrderedDict()
    controls.update( { 'Color': 'color'})
    controls.update( { 'Rainbow': 'checkbox'})
    controls.update( { 'All Sides': 'checkbox'})

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.beacon_shader)
        self.show = False
        self.color = (255, 0, 0)
        self.rainbow = 0
        self.all = 0
        col.create_rainbow()

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]
        if checkbox==1:
            self.all = self.cm.checkbox[checkbox]

    def beacon_shader(self,p):

        # use progress
        if self.show:
            color_hsv = rgb_to_hsv(self.color)  

            if self.all:
                dist_x = 1-abs(p['point'][0])
                dist_y = 1-abs(p['point'][1])
                dist_z = 1-abs(p['point'][2])
                if dist_x < 0.02:
                    return hsv (color_hsv[0], color_hsv[1], 1-dist_x)
                if dist_y < 0.02: 
                    return hsv (color_hsv[0], color_hsv[1], 1-dist_y)
                if dist_z < 0.2:
                    return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
                return (0,0,0)

            else:
                dist = abs(p['point'][2]-1)
                if dist > 0.1:
                    dist=1
                return hsv (color_hsv[0], color_hsv[1], 1-dist)
        else: 
            return (0,0,0)


    def update_at_progress(self, progress, new_loop, loop_instance):

        if progress > 0.5:
            self.show = 1
        else:
            self.show = 0

        print loop_instance % 18
        if self.rainbow:
            self.color = col.rainbow[int(loop_instance%18)]


__shows__ = [
              (Top_Beacon.name, Top_Beacon)
            ]


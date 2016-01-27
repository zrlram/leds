#!/usr/bin/env python

from color import hsv, rgb_to_hsv
from operator import xor

import looping_shader_show

class Top_Beacon(looping_shader_show.LoopingShaderShow):

    name = "Top Beacon"

    controls = { 'color': 'color' }

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.top_beacon_shader)
        self.show = False
        self.color = (255, 0, 0)

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def top_beacon_shader(self,p):

        # use progress
        if self.show:
            dist = abs(p['point'][2]-1)
            if dist > 0.1:
                dist=1
            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            return hsv (color_hsv[0], color_hsv[1], 1-dist)
        else: 
            return (0,0,0)


    def update_at_progress(self, progress, new_loop, loop_instance):

        if progress > 0.5:
            #self.show = xor(self.show, True)
            self.show = 1
        else:
            self.show = 0

        # this is done in the Looping Shader Show for us!
        # model.map_pixels(self.geometry)

__shows__ = [
              (Top_Beacon.name, Top_Beacon)
            ]


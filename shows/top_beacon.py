#!/usr/bin/env python

from color import hsv
from operator import xor
import time

import looping_shader_show

class Top_Beacon(looping_shader_show.LoopingShaderShow):

    name = "Top Beacon"

    show = False
    previous_t = 0.0

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.top_beacon_shader)

    def top_beacon_shader(self,p):

        if self.show:
            dist = abs(p['point'][2]-1)
            if dist > 0.1:
                dist=1
            return hsv(1, 0.9, 1-dist)
        else: 
            return (0,0,0)

    def update_at_progress(self, progress, new_loop, loop_instance):

        now = time.time() *1000      # millis
        if self.previous_t==0:
            self.previous_t = now

        dt = (now - self.previous_t) 
        if dt > 200:
            self.previous_t = now
            self.show = xor(self.show, True)

        # this is done in the Looping Shader Show for us!
        # model.map_pixels(self.geometry)

__shows__ = [
              (Top_Beacon.name, Top_Beacon)
            ]


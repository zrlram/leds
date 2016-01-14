#!/usr/bin/env python

from color import hsv
import time
from math import cos

import looping_shader_show

class HorizontalLine(looping_shader_show.LoopingShaderShow):

    name = "Horizontal Line"

    dz = 0

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

    def shader(self, p):

        z = p['point'][2]
        dist_z = 5 * abs(z - self.dz)   # trail - small is large tail

        hue = 0.7
        sat = 0.8
        value = dist_z

        return hsv(hue, sat, 1-value)

    def update_at_progress(self, progress, new_loop, loop_instance):

        speed = 1000.0                # 1 seconds for -1 to 1 (entire sphere)
        now = int(time.time() * 1000)     # millis
        dist = cos(now/speed) 
        self.dz = dist

__shows__ = [
              (HorizontalLine.name, HorizontalLine)
            ]


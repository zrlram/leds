#!/usr/bin/env python

from color import hsv
import time
from math import cos

import looping_shader_show

class VerticalLine(looping_shader_show.LoopingShaderShow):

    name = "Vertical Line"

    dx = 0

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

    def shader(self, p):

        x = p['point'][0]
        dist_x = 10 * abs(x - self.dx)   # trail - small is large tail

        hue = 0.6
        sat = 0.8
        value = dist_x

        return hsv(hue, sat, 1-value)

    def update_at_progress(self, progress, new_loop, loop_instance):

        speed = 1000.0                # 1 seconds for -1 to 1 (entire sphere)
        now = int(time.time() * 1000)     # millis
        dist = cos(now/speed) 
        self.dx = dist

__shows__ = [
              (VerticalLine.name, VerticalLine)
            ]


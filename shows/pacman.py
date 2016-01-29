from color import hsv, rgb_to_hsv
from math import sin, sqrt, tan, cos

import looping_shader_show

class PacMan(looping_shader_show.LoopingShaderShow):

    name = "PacMan"

    # a list signifies a range slider
    #   trail: [min, max, start]
    # controls = { 'trail': [0, 10], 'color': 'color' }
    controls = { 'color': 'color' }

    # implicitly registered in super class
    # def set_controls_model(self,cm)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.angle = 1.0

        # configurable controls
        self.color = (250,250,0)
        self.background = (0,0,0)

        self.duration = 1

    def control_color_changed(self, c_ix):
        if c_ix == 0:       
            self.color = self.cm.chosen_colors[c_ix]

    #def custom_range_value_changed(self, range):
        #self.trail = self.cm.ranges[range]

    def shader(self, p):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]

        y_ = 1 - x**2 - z**2
        z_ = tan(self.angle) * x
       
        if x < 0: return self.color

        if y_ < abs(y) and z_ < abs(z):
            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist = ((y-y_)**2 + (z-z_)**2)  * 4
            if dist > 1: dist = 1
            intensity = dist
            # intensity = cos(dist)
            return hsv (color_hsv[0], color_hsv[1], intensity)
        else:
            return self.background


    def update_at_progress(self, progress, new_loop, loop_instance):

        self.angle = sin(progress)


__shows__ = [
              (PacMan.name, PacMan)
            ]


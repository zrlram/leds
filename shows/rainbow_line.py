from color import hsv, rgb_to_hsv, rainbow_
import random

import looping_shader_show

class RainbowLine(looping_shader_show.LoopingShaderShow):

    name = "Rainbow Line"

    # a list signifies a range slider
    #   trail: [min, max, start]
    # controls = { 'trail': [0, 10], 'color': 'color' }
    controls = { 'Trail Length': [0.1, 1, 0.5, 0.01], 
                 'color': 'color'}

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.dz = 1.0
        self.mode = 0

        # configurable controls
        self.trail = 0.5
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.sign = 1
        self.progress = 0.0

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    def shader(self, p):

        z = p[2]
        y = p[1]
        x = p[0]
        dist_z = abs(z - self.dz)  

        #if dist_z < self.trail:
        if dist_z/self.trail <= 1.0 and dist_z/self.trail >= 0.0:

            if self.mode == 0:
                self.color = rainbow_(1, z*13, self.cm.brightness)
            elif self.mode == 1:
                self.color = rainbow_(self.trail, x*16, self.cm.brightness)
            elif self.mode == 2:
                self.color = rainbow_(self.progress, x*6+y*6+self.progress, self.cm.brightness)
            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        else:
            return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        self.progress = progress
        # dz is from -1 to 1
        if (loop_instance % 2):
            # up
            self.dz = 1 - 2 * progress
        else:
            # down
            self.dz = - (1 - 2 * progress)

        if loop_instance % 5 == 0 and new_loop :
            self.mode = (self.mode + 1) % 3

        '''
        if self.trail > 0.95:
            self.sign = -1
        if self.trail < 0.05:
            self.sign = 1
        '''

        #self.trail += random.random()*0.01 * self.sign

__shows__ = [
              (RainbowLine.name, RainbowLine)
            ]


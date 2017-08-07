from color import hsv, rgb_to_hsv, rainbow_
from math import sqrt
import random

import looping_shader_show

class Circle(looping_shader_show.LoopingShaderShow):

    name = "Circle"

    # a list signifies a range slider
    #   trail: [min, max, start]
    # controls = { 'trail': [0, 10], 'color': 'color' }
    controls = { 'Trail Length': [0.1, 1, 0.5, 0.01], 
                 'color': 'color',
                 'rainbow': 'checkbox'}

    # implicitly registered in super class
    # def set_controls_model(self,cm)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.dz = 0
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.direction = 0

        # configurable controls
        self.trail = 0.25
        self.rainbow = 1
        self.duration = 4
        self.z_offcenter = 0.0
        self.y_offcenter = 0.0

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    def shader(self, p):

        z = p[2]
        y = p[1]

        dist = sqrt((z-self.z_offcenter)**2 + (y-self.y_offcenter)**2)
        dist_z = abs(dist - self.dz)  
        #print dist_z

        if dist_z < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail % 1.0
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        if new_loop:
            self.direction ^= 1
            self.z_offcenter_target = random.uniform(-1,1)
            self.y_offcenter_target = random.uniform(-1,1)

        if self.direction:
            self.dz = (1.0 - progress)
        else:
            self.dz = progress

        d = self.y_offcenter_target - self.y_offcenter
        if self.y_offcenter_target > self.y_offcenter and d>0:
            self.y_offcenter += 0.01
        else:
            self.y_offcenter -= 0.01

        d = self.z_offcenter_target - self.z_offcenter
        if self.z_offcenter_target > self.z_offcenter and d>0:
            self.z_offcenter += 0.01
        else:
            self.z_offcenter -= 0.01

        if self.rainbow:
            self.color = rainbow_(progress, loop_instance, 1.0 )

__shows__ = [
              (Circle.name, Circle)
            ]


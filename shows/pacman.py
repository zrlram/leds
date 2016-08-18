from color import hsv, rgb_to_hsv
from math import sin, sqrt, tan, cos, pi
import color as col
from collections import OrderedDict

import looping_shader_show

class PacMan(looping_shader_show.LoopingShaderShow):

    name = "PacMan"

    # a list signifies a range slider
    #   trail: [min, max, start]
    # controls = { 'trail': [0, 10], 'color': 'color' }
    controls = OrderedDict()
    controls.update({ 'color': 'color'})
    controls.update({ 'rainbow': 'checkbox'})
    controls.update({ 'move': 'checkbox'})


    # implicitly registered in super class
    # def set_controls_model(self,cm)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.progress = 1.0
	self.angle = 0

        # configurable controls
        self.color = (250,250,0)
        self.background = (0,0,0)
        self.rainbow = 1
        self.move = 0

        self.duration = 8

    def control_color_changed(self, c_ix):
        if c_ix == 0:       
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]
        if checkbox==1:
            self.move = self.cm.checkbox[checkbox]

    def shader(self, p):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]
     
        x_rot = x
        # y_rot = y                   # will hold the rotated variables

        # moving packman - we need to rotate x and y
        if self.move:
            rotate = self.progress * 2*pi   # mouth opens 4 times and one
                                            # progress is one revolution
                                            # map to circle

            x_rot = x * cos(rotate) - y * sin(rotate)           
            #y_rot = y * cos(rotate) + x * sin(rotate)

        # This is PacMan, believe it or not, well, almost
        # y_ = 1 - x_rot**2 - z**2
        z_ = tan(self.angle) * x_rot

        # Learning: The perfect math does not always create the best visual representation
        # and cheating is more fun and faster too ;)

        if x_rot < 0: return self.color     # the non-mouth half of pacman
        #if y_ < abs(y_rot) and z_ < abs(z):
        if z_ < abs(z):
            color_hsv = rgb_to_hsv(self.color)  
            # -- dist = ((x_rot-x)**2 + (y_rot-y_)**2 + (z-z_)**2)  * 4
            # working: dist = ((y_rot-y_)**2 + (z-z_)**2)  * 4
            dist = abs(z-z_)
            intensity = 1
            if dist < 0.1:
                #intensity = 10*dist
                intensity = 10*dist
            #if dist > 1: dist = 1
            # intensity = cos(dist)
            return hsv (color_hsv[0], color_hsv[1], intensity)
        else:
            return self.background


    def update_at_progress(self, progress, new_loop, loop_instance):

        self.progress = progress
        self.angle = sin((self.progress*8) % 1) 
        if self.rainbow:
            self.color = col.rainbow[int(progress*len(col.rainbow))]


__shows__ = [
              (PacMan.name, PacMan)
            ]


from color import hsv, rgb_to_hsv, rainbow_
from math import pi, cos, sin, sqrt
from collections import OrderedDict

import looping_shader_show

class RotatingLine(looping_shader_show.LoopingShaderShow):

    name = "Rotating Line"

    controls = OrderedDict()
    controls.update({ 'Trail Length': [0.1, 1, 0.3, 0.01]})
    controls.update({'color': 'color'})
    controls.update({'tilt change' : [0.001, 1, 0.2, 0.001]})
    controls.update({'rainbow': 'checkbox'})
                 
    # implicitly registered in super class
    # def set_controls_model(self,cm)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.dz = 1.0
        self.dy = 1.0
        self.angle = 0

        # configurable controls
        self.trail = 0.2
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.rainbow = 1
        self.tilt = 0
        self.tilt_change = 0.2

        self.duration = 10


    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]

    def custom_range_value_changed(self, range):
        if range ==0:
            self.trail = self.cm.ranges[range]
        if range ==1:
            self.tilt_change = self.cm.ranges[range]

    def rotate_x_shader(self, p):

        y = p['point'][1]
        x = p['point'][0]


        # the shape itself
        z_ = y*sin(self.angle)+z*cos(self.angle)

        # don't change the z-position
        dist_z = abs(z_)  
        
        if dist_z < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        else:
            return self.background

    def shader_rotate_y(self, p):

        z = p['point'][2]
        y = p['point'][1]
        x = p['point'][0]

        # shape tilt
        z_ = z*sin(self.tilt)+x*cos(self.tilt)
        y_ = y

        # rotate
        z__ = y_*sin(self.angle)+z_*cos(self.angle)

        dist_z = abs(z__)  
        
        if dist_z < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        else:
            return self.background

    def shader(self, p):

        z = p['point'][2]
        y = p['point'][1]
        x = p['point'][0]

        # shape tilt
        x_ = x*cos(self.tilt)-z*sin(self.tilt)
        z_ = z*sin(self.tilt)+x*cos(self.tilt)
        y_ = y

        # rotate
        x__ = x_
        y__ = y_*cos(self.angle)-z_*sin(self.angle)
        z__ = y_*sin(self.angle)+z_*cos(self.angle)

        self.dz = 0
        dist_z = abs(z__ - self.dz)  
        

        #dist_z = abs(z_ - self.dz)  
        #dist = sqrt((z_-z) ** 2 + (y_-y) ** 2 + (x_-x) ** 2)
        #dist_2 = sqrt((z_-z) **2 + (y_-y) **2)

        #if (abs(x_)<0.3 and abs(y_)<0.6 and y_>0):
        #if (abs(x_)<self.trail and abs(y_)<self.trail and abs(z_)<self.trail):

        #if dist_z < self.trail and dist_y < self.trail:
        if dist_z < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            #return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        else:
            return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        self.angle = progress * pi * 2
        self.tilt += self.tilt_change
        #self.tilt = self.tilt % (pi / 3)

        # dz is from -1 to 1
        if (loop_instance % 2):
            # up
            self.dz = 1 - 2 * progress
            self.dy = 1 - 2 * progress
        else:
            # down
            self.dz = - (1 - 2 * progress)
            self.dy = - (1 - 2 * progress)

        if self.rainbow:
            self.color = rainbow_(progress, loop_instance, self.cm.brightness)

__shows__ = [
              (RotatingLine.name, RotatingLine)
            ]


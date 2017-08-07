from color import hsv, rgb_to_hsv, rainbow_
from math import pi, cos, sin, sqrt

import looping_shader_show

class RandomRotatingLine(looping_shader_show.LoopingShaderShow):

    name = "RandomRotating Line"

    controls = { 'Trail Length': [0.1, 1, 0.3, 0.01], 
                 'color': 'color',
                 'rainbow': 'checkbox'}

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

        self.duration = 10


    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    #def control_speed_changed(self):
    #    if (self.cm.speed_multi == 1.0): # such a hack :(
    #        self.cm.speed_change_rel(0.4)

    def shader(self, p):

        #self.angle = pi/4
        z = p[2]
        y = p[1]
        x = p[0]


        x_ = x
        y_ = y*cos(self.angle)-z*sin(self.angle)
        z_ = y*sin(self.angle)+z*cos(self.angle)

        x__ = x_*cos(self.angle)-z_*sin(self.angle)
        z__ = z_*sin(self.angle)+x_*cos(self.angle)
        y__ = y_

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

        self.angle = progress * 2*pi
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
            #self.color = rainbow[int(progress*10%len(rainbow))]
            self.color = rainbow_(progress, loop_instance+progress*10, self.cm.brightness)

__shows__ = [
              (RandomRotatingLine.name, RandomRotatingLine)
            ]


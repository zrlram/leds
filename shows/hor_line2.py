from color import hsv, rgb_to_hsv, rainbow_
import random

import looping_shader_show

class HorLines(looping_shader_show.LoopingShaderShow):

    name = "Horizontal Lines"

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

        self.dz = 1.0

        # configurable controls
        self.trail = 0.2
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.rainbow = 1
        self.area = 0

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
        dist_z = abs(z - self.dz)  
        dist_z_2 = (self.dz + 1.0)
        if dist_z_2 >= 1.0:
            dist_z_2 -= 2.0
        dist_z_2 = abs(z - dist_z_2)

        ''' trying to light up 1/8 of the sphere as glitter
        if self.dz > 0.9:
            if self.area == 0 and z<0 and p[1]>0 and p[0]>0:
                self.area += 1 % 8
                print "foo" 
                return hsv(1.0, 0.1, 1.0)
            if self.area == 1 and z>0 and p[1]>0 and p[0]>0:
                self.area += 1 % 8
                return hsv(1.0, 0.1, 1.0)
            if self.area == 2 and z<0 and p[1]<0 and p[0]>0:
                self.area += 1 % 8
                return hsv(1.0, 0.1, 1.0)
        '''

        if dist_z < self.trail:

            #print dist_z
            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        if dist_z_2 < self.trail: 

            #print dist_z_2
            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z_2 / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)

        return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        # dz is from -1 to 1
        self.dz = - (1.0 - 2 * progress)

        if self.rainbow:
            self.color = rainbow_(progress, loop_instance, 1.0)

__shows__ = [
              (HorLines.name, HorLines)
            ]


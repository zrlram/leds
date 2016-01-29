from color import hsv, rgb_to_hsv

import looping_shader_show

class HorizontalLine(looping_shader_show.LoopingShaderShow):

    name = "Horizontal Line"

    # a list signifies a range slider
    #   trail: [min, max, start]
    # controls = { 'trail': [0, 10], 'color': 'color' }
    controls = { 'Trail Length': [0.1, 1, 0.5, 0.01], 'color': 'color' }

    # implicitly registered in super class
    # def set_controls_model(self,cm)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.dz = 1.0

        # configurable controls
        self.trail = 0.5
        self.color = (50,50,255)
        self.background = (0,0,0)

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_range_value_changed(self, range):
        self.trail = self.cm.ranges[range]

    def shader(self, p):

        z = p['point'][2]
        dist_z = abs(z - self.dz)  

        if dist_z < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            dist_z = dist_z / self.trail
    
            return hsv (color_hsv[0], color_hsv[1], 1-dist_z)
            
        else:
            return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        # dz is from -1 to 1
        if (loop_instance % 2):
            # up
            self.dz = 1 - 2 * progress
        else:
            # down
            self.dz = - (1 - 2 * progress)

__shows__ = [
              (HorizontalLine.name, HorizontalLine)
            ]


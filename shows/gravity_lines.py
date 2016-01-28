from collections import OrderedDict

from color import hsv, rgb_to_hsv
import looping_shader_show

class GravityLine(looping_shader_show.LoopingShaderShow):

    name = "Gravity Line"

    controls = OrderedDict()
    controls.update( { 'Trail Length': [0, 10, 5] } )
    controls.update( { 'color': 'color' } )
    controls.update( { 'initial speed': [0, 5, 1.0] } )
    controls.update( { 'energy loss': [0, 1, 0.9] } )
    controls.update( { 'friction': [0,1,0.0] } )

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.y = 1.0     # initial high of the ball
        self.g = -9.81 # aceleration of gravity
        self.duration = 5       # this is the time that the drop is reset

        # can be controlled
        self.initial_v = 1.0        # can be set, not self.v though!
        self.v = self.initial_v     # initial velocity of the ball
        self.e = 0.9   # coef. lost of energy in each bounce
        self.k = 0.0   # friction with air


        # configurable controls
        self.trail = 5
        self.color = (50,50,255)

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]

    def custom_range_value_changed(self, range):

        if range==0:
            self.trail = self.cm.ranges[range]
        elif range==1:
            self.initial_v = self.cm.ranges[range]
            self.y = 1
            self.v = self.initial_v
        elif range==2:
            self.e = self.cm.ranges[range]
        elif range==3:
            self.k = self.cm.ranges[range]

    def shader(self, p):

        z = p['point'][2]
        dist_z = self.trail * abs(z - self.y)   # trail - small is large tail

        color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
        return hsv (color_hsv[0], color_hsv[1], 1-dist_z)


    def update_at_progress(self, progress, new_loop, loop_instance):

        dt = self.elapsed_time
        print "dt", dt

        dv = self.g * dt - self.k * self.v * dt
        self.v += dv
        self.y += self.v * dt

        # Bounce conditions
        if  self.y < -1:
            self.v = -self.v * self.e

        # TBD: Reset conditions
        if progress > 0.9:
            self.y = 1
            self.v = self.initial_v

__shows__ = [
              (GravityLine.name, GravityLine)
            ]


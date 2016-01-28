import looping_shader_show
from math import cos, sin, pi
from color import hsv

class SwissCross(looping_shader_show.LoopingShaderShow):

    name = "Swiss Cross"

    red = (255, 0, 0)
    white = (230, 230, 230)

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.geometry = geometry

        self.duration = 10
        self.angle = 0      # for rotation

    def shader(self,p):

        x = p['point'][0] 
        y = p['point'][1]
        z = p['point'][2]

        x_ = x*cos(self.angle)-y*sin(self.angle)
        y_ = x*sin(self.angle)+y*cos(self.angle)

        if (abs(x_)<0.3 and abs(z)<0.6 and y_>0):
            return hsv(0.3, 0, 1-abs(x_))
            #return hsv(0, 0, 1)
        if (abs(z)<0.2 and abs(x_)<0.6 and y_>0):
            return hsv(0.3, 0, 1-abs(z))
            #return hsv(0, 0, 1-abs(z))
            #return hsv(0, 0, 1)

        # background
        return SwissCross.red

    def update_at_progress(self, progress, new_loop, loop_instance):

        self.angle = progress * 2*pi


__shows__ = [
              (SwissCross.name, SwissCross)
            ]


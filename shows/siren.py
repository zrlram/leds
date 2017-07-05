import looping_shader_show
from math import pi, atan2
import color2


class Siren(looping_shader_show.LoopingShaderShow):

    name = "Siren"
    ok_for_random = False

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.Siren_shader)

        # for rotating
        self.shift = 0

        # configurable controls
        self.red = (200, 0, 0)
        self.blue = (50, 50, 250)

        self.duration = 5       # make the show slower!

    def Siren_shader(self, p):

        x = p[0]
        y = p[1]

        phi = atan2(y, x) + pi          # from 0 to 2pi
        phi = (phi + self.shift) % (2*pi)

        if phi < pi:
            return self.red
        else:
            return self.blue



    def update_at_progress(self, progress, new_loop, loop_instance):

        self.shift = progress * pi * 2          # one full circle rotation
        # TBD - change color to rainbow over time
        # self.color = 
        rgbTuple = color2.hsvRYB_to_rgb((progress, 0.9, 0.9))
        self.red = rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))
        rgbTuple = color2.hsvRYB_to_rgb(((progress-0.5)%1, 0.8, 0.8))
        self.blue = rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

        

__shows__ = [
              (Siren.name, Siren)
            ]

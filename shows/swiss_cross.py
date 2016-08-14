import looping_shader_show
from math import cos, sin, pi
from color import rainbow, hsv, rgb_to_hsv
from collections import OrderedDict

class SwissCross(looping_shader_show.LoopingShaderShow):

    name = "Swiss Cross"

    controls = OrderedDict()
    controls.update({'Rainbow': 'checkbox'})

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.shader)

        self.geometry = geometry

        self.duration = 10
        self.angle = 0      # for rotation
        self.rainbow = 1
        self.flag = (230, 230, 230)     # white
        self.background = (255, 0, 0)   # red
        self.duration = 2

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]
        #if checkbox==1:
            #self.laser = self.cm.checkbox[checkbox]


    def shader(self,p):

        x = p['point'][0] 
        y = p['point'][1]
        z = p['point'][2]

        x_ = x*cos(self.angle)-y*sin(self.angle)
        y_ = x*sin(self.angle)+y*cos(self.angle)

        col = rgb_to_hsv(self.flag)

        if (abs(x_)<0.3 and abs(z)<0.6 and y_>0):
            return hsv(col[0], col[1], 1-abs(x_))
            #return hsv(0.3, 0, 1-abs(x_))
        if (abs(z)<0.2 and abs(x_)<0.6 and y_>0):
            return hsv(col[0], col[1], 1-abs(z))
            #return hsv(0.3, 0, 1-abs(z))

        # background
        return self.background

    def update_at_progress(self, progress, new_loop, loop_instance):

        self.angle = progress * 2*pi

        if self.rainbow:
            self.background = rainbow[int(loop_instance % len(rainbow))]

        # print "setting bg to: %s" % str(self.background)



__shows__ = [
              (SwissCross.name, SwissCross)
            ]


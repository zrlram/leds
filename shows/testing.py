import looping_shader_show
from color import rgb_to_hsv, hsv
from math import pi, sin, cos, atan2, sqrt
from collections import OrderedDict

class Testing(looping_shader_show.LoopingShaderShow):

    name = "Testing"

    # Defining the controls themselves
    controls = OrderedDict()
    controls.update( { 'Top Position': [0, 255] } )
    controls.update( { 'Bottom Position': [0, 243] } )
    controls.update( { 'X': [-1, 1, 0] } )
    controls.update( { 'Y': [-1, 1, 0] } )
    controls.update( { 'Z': [-1, 1, 0] } )
    controls.update( { 'Trail': [0, 1, 0.5, 0.01] } )
    controls.update( { 'Theta': [-pi/2, pi/2, 0, pi/40] } )
    controls.update( { 'Phi': [0, 2*pi, 0, pi/44] } )

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.Testing_shader)

        # configurable controls
        self.color = (50,50,255)
        self.background = (10,10,10)

        self.point1 = 0
        self.point2 = 256

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.trail = 0.5

        self.phi = 0.0
        self.theta = 0.0


    def custom_range_value_changed(self, range):
        '''
            phi = around :: F=0, B=pi
            theta = up
        '''
        print "range_change",range, self.cm.ranges[range]

        if range == 0:
            self.point1 = self.cm.ranges[range]
        if range == 1:
            self.point2 = self.cm.ranges[range]

        if range == 2:
            # x^2 + y^2 = 1
            self.x = self.cm.ranges[range]
            self.y = sqrt(1 - self.x **2)
            self.phi = atan2(self.y, self.x) + pi
            print "setting x: ", self.x, "updating phi: ", self.phi
        if range == 3:
            # x^2 + y^2 = 1
            self.y = self.cm.ranges[range]
            self.x = sqrt(1 - self.y **2)
            self.phi = atan2(self.y, self.x) + pi
            print "setting y: ", self.y, "updating phi, x: ", self.phi, self.x
        if range == 4:
            self.z = self.cm.ranges[range]
        if range == 5:
            self.trail = self.cm.ranges[range]
        if range == 6:
            self.theta = self.cm.ranges[range]
            self.z = sin(self.theta)
            print "setting theta: ", self.theta, "updating z: ", self.z
        if range == 7:
            self.phi = self.cm.ranges[range]
            # have to scale to the new radius at that hight, which is 
            # cos(theta)
            self.x = cos(self.theta) * sin(self.phi)
            self.y = cos(self.theta) * cos(self.phi)
            print "setting phi: ", self.phi, "updating x,y  ", self.x, self.y

    
    def Testing_shader(self, p):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]
        #print 's', self.z

        x_ = cos(self.theta) * sin(self.phi)
        y_ = cos(self.theta) * cos(self.phi)
        z_ = sin(self.theta)
        dist = sqrt((z_-z) ** 2 + (y_-y) ** 2 + (x_-x) ** 2)

        if dist < self.trail:

            color_hsv = rgb_to_hsv(self.color)  # set the intesity to the distance
            #return hsv (color_hsv[0], color_hsv[1], 1.0-dist*1/self.trail)
            # dist = dist / self.trail
            intensity = cos(dist)
            return hsv (color_hsv[0], color_hsv[1], intensity)

        else:
            return self.background



__shows__ = [
              (Testing.name, Testing)
            ]

import looping_shader_show
from color import rainbow, set_V
from math import sin, atan2, pi, sqrt, cos
from collections import OrderedDict


class Sine(looping_shader_show.LoopingShaderShow):

    name = "Sine"

    controls = OrderedDict()
    controls.update({ 'Color': 'color'})
    controls.update({'Rainbow': 'checkbox'})
    controls.update({'Background': 'color'})
    controls.update({'Amplitude': [0,1,0.5]})
    controls.update({'Frequency': [0,10,4.0]})
    controls.update({'Laser Drawing': 'checkbox'})


    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.sine_shader)

        # for rotating
        self.shift = 0

        # configurable controls
        self.color = (50,50,255)
        self.background = (0,0,0)
        self.frequency = 4.0
        self.amplitude = 0.5
        self.rainbow = 1
        self.laser = 0          # is it drawing it slowly on the sphere?
        self.laser_pos = .0      # and what's its position?

        self.duration = 10       # make the show slower!

    def control_color_changed(self, c_ix):
        if c_ix == 0:       # use the primarty color
            self.color = self.cm.chosen_colors[c_ix]
        if c_ix == 1:  
            self.background = self.cm.chosen_colors[c_ix]

    def custom_range_value_changed(self, range):
        if range == 0:
            self.frequency = self.cm.ranges[0]
            print "freq", self.frequency
        if range == 1:
            self.amplitude = self.cm.ranges[1]
            print "amp", self.amplitude

    def custom_checkbox_value_changed(self, checkbox):
        if checkbox==0:
            self.rainbow = self.cm.checkbox[checkbox]
        #if checkbox==1:
            #self.laser = self.cm.checkbox[checkbox]

    
    def sine_shader(self, p):

        '''
            say we have a matrix (x,y,z) = intensity
            for the regular sine curve in space (x,y,z) * 100 (sample rate 100)
                x = x; 
                z = (sin(phi*f) *a)
                y = f(x,z) = 1 - x**2 - z**2;      # x^2+y^2+z^2 = 1
            for x=[0, 2pi]

            

        '''

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]

        phi = atan2(y, x) + pi      # from 0 to 2pi
        z_ = sin(phi*self.frequency) * self.amplitude

        rotate = self.shift
        x_rot = x * cos(rotate) - z_ * sin(rotate)
        z_rot = x * sin(rotate) + z_ * cos(rotate)

        #dist = sqrt( (z_rot - z)**2 + (x_rot - x)**2 )
        dist = sqrt( (z_rot - z)**2 )

        if dist < 0.2:
            intensity = 1-dist/0.2
            return set_V(self.color, absolute=intensity)  # set the intesity to the distance

        else:
            return self.background

        '''
        if dist < 0.2:

            intensity = 1 - (dist / 0.2)

            if self.laser:
                if abs(self.laser_pos - phi) < 0.08:
                    #print self.laser_pos, phi, self.laser_pos - phi
                    return set_V((255,255,0), absolute=intensity )

            # intensity = 1.0-dist*3.0
            return set_V(self.color, absolute=intensity)  # set the intesity to the distance
        # fill bottom
        #elif z<z_:
        #    return self.color
        else:
            return self.background
        '''


    def update_at_progress(self, progress, new_loop, loop_instance):

        self.shift = progress * 2 * pi
        self.laser_pos += pi/22 % (2*pi)
        self.laser_pos %= (2*pi)
        if self.rainbow:
            self.color = rainbow[int(((self.shift / (2 * pi)) * len(rainbow)) % len(rainbow))]
        

__shows__ = [
              (Sine.name, Sine)
            ]

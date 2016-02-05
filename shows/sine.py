import looping_shader_show
from color import rainbow, set_V
from math import sin, atan2, pi
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
        self.rainbow = 0
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
        if checkbox==1:
            self.laser = self.cm.checkbox[checkbox]

    
    def sine_shader(self, p):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]

        phi = atan2(y, x) + pi      # from 0 to 2pi
        if self.laser:
            dist = abs(z - sin(phi*self.frequency) * self.amplitude)
        else:
            dist = abs(z - sin((phi+self.shift)*self.frequency) * self.amplitude)
        #dist = abs(z - sin((phi)*self.frequency) * self.amplitude)
        if dist < 0.2:

            intensity = 1 - (dist / 0.2)

            if self.laser:
                if abs(self.laser_pos - phi) < 0.08:
                    #print self.laser_pos, phi, self.laser_pos - phi
                    return set_V((255,255,0), absolute=intensity )

            # intensity = 1.0-dist*3.0
            return set_V(self.color, absolute=intensity)  # set the intesity to the distance

        else:
            return self.background



    def update_at_progress(self, progress, new_loop, loop_instance):

        self.shift = progress * 2 * pi
        self.laser_pos += pi/22 % (2*pi)
        self.laser_pos %= (2*pi)
        if self.rainbow:
            self.color = rainbow[int((self.shift / (2 * pi)) *18)]
        

__shows__ = [
              (Sine.name, Sine)
            ]

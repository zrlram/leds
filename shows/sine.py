import looping_shader_show
from color import rgb_to_hsv, hsv, rainbow, create_rainbow, set_V
from math import sin, atan2, pi


class Sine(looping_shader_show.LoopingShaderShow):

    name = "Sine"

    controls = { 'Color': 'color', 
                 'Rainbow': 'checkbox',
                 'Background': 'color',
                 'Amplitude': [0,1,0.5],
                 'Frequency': [0,10,4.0]}


    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.sine_shader)

        # for rotating
        self.shift = 0

        # configurable controls
        self.color = (50,50,255)
        self.background = (10,10,10)
        self.frequency = 4.0
        self.amplitude = 0.5
        self.rainbow = 0

        self.duration = 10       # make the show slower!

        create_rainbow()

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
        self.rainbow = self.cm.checkbox[checkbox]

    
    def sine_shader(self, p):

        x = p['point'][0]
        y = p['point'][1]
        z = p['point'][2]

        phi = atan2(y, x) + pi      # from 0 to 2pi
        dist = abs(z - sin((phi+self.shift)*self.frequency) * self.amplitude)
        #dist = abs(z - sin((phi)*self.frequency) * self.amplitude)
        if dist < 0.2:

            if self.rainbow:
                self.color = rainbow[int((self.shift / (2 * pi)) *18)]

            return set_V(self.color, absolute=1.0-dist*3.0)  # set the intesity to the distance

        else:
            return self.background



    def update_at_progress(self, progress, new_loop, loop_instance):

        self.shift = progress * 2 * pi
        # TBD - change color to rainbow over time
        # self.color = 
        

__shows__ = [
              (Sine.name, Sine)
            ]

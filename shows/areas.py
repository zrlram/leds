from color import set_H, get_H
from randomcolor import random_color
import morph
import model

import looping_show

class Areas(looping_show.LoopingShow):

    name = "Areas"

    controls = { 'mode': [0,4,2,1] }

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.mode = 2
        self.foreground = random_color(luminosity="light")
        self.background = self.foreground
        fg_H = (get_H(self.foreground) + 0.5) % 1
        set_H(self.background, absolute=fg_H)

    def clear(self):
        for i in range(model.numLEDs):
            self.geometry.set_pixel(i, self.background)

        self.geometry.draw()

    def custom_range_value_changed(self, range):
        self.mode = self.cm.ranges[range]
        print "setting mode to", self.mode

    def update_at_progress(self, progress, new_loop, loop_instance):

        if new_loop:
            #self.foreground = random_color(luminosity="light")
            self.foreground = random_color()
            self.background = self.foreground
            self.background = set_H(self.background, absolute=(get_H(self.foreground) + 0.5) % 1)

            self.color_list = morph.transition_list(self.foreground, self.background, steps=16)

            self.clear()

        
        if self.mode == 0:
            _list = [[x for x in range(model.numLEDs)]]
        elif self.mode ==1:
            _list = model.HOR_RINGS_TOP_DOWN
        elif self.mode ==2:
            _list = model.HOR_RINGS_MIDDLE_OUT
        #elif self.mode ==3:
        #    _list = model.HOR_RINGS_MIDDLE_OUT
        else:
            _list = [[x for x in range(model.numLEDs)]]

        # Because progress will never actually hit 1.0, this will always
        # produce a valid list index
        to_light = int(progress * len(_list))

        for i in range(0, len(_list)):
            c = self.background

            if i <= to_light:
                x = i
                if len(_list) < len(self.color_list) / 2:
                    x = i * 2
                c_ix = x % len(self.color_list)

                #if self.cm.modifiers[2] and (loop_instance % 2 == 0):
                #    c_ix = len(self.color_list) - 1 - c_ix

                c = self.color_list[c_ix]

            for i in _list[i]:
                self.geometry.set_pixel(i, c)

        self.geometry.draw()
    

__shows__ = [
              (Areas.name, Areas)
            ]


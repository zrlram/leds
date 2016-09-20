from color2 import hsv_to_rgb
from randomcolor import random_color
import morph
import model
# import audio

import looping_show

class Areas(looping_show.LoopingShow):

    name = "Areas"

    controls = { 'mode': [0,4,2,1] }

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.mode = 2
        self.foreground = random_color(luminosity="light")
        self.background = self.foreground.copy()
        self.background.h += 0.5
        self._list = []

	# self.audio = audio.Audio()

    def clear(self):
        c = hsv_to_rgb(self.background.hsv)
        for i in range(model.numLEDs):
            self.geometry.set_pixel(i, c)

        self.geometry.draw()

    def custom_range_value_changed(self, range):
        self.mode = self.cm.ranges[range]
        print "setting mode to", self.mode

    def update_at_progress(self, progress, new_loop, loop_instance):

	# (loud, pitch) = self.audio.audio_input()

        if new_loop:
            #self.foreground = random_color(luminosity="light")
            self.foreground = random_color()
            self.background = self.foreground.copy()
            self.background.h += 0.5

            self.color_list = morph.transition_list(self.foreground, self.background, steps=16)

            self.clear()

            # udpate mode every now and then
            if (loop_instance % 5 == 0):
                self.mode = (self.mode + 1) % 4
                print "Changing mode to %s" % self.mode

            if self.mode == 0:
                self._list = [[x for x in range(model.numLEDs)]]
            elif self.mode ==1:
                self._list = model.HOR_RINGS_TOP_DOWN
            elif self.mode ==2:
                self._list = model.HOR_RINGS_MIDDLE_OUT
            elif self.mode ==3:
                self._list = model.HOR_RINGS_TOP_DOWN
                self._list.reverse()
            else:
                self._list = [[x for x in range(model.numLEDs)]]

        # Because progress will never actually hit 1.0, this will always
        # produce a valid list index
        to_light = int(progress * len(self._list))

        for i in range(0, len(self._list)):
            c = self.background

            if i <= to_light:
                x = i
                if len(self._list) < len(self.color_list) / 2:
                    x = i * 2
                c_ix = x % len(self.color_list)

                #if self.cm.modifiers[2] and (loop_instance % 2 == 0):
                #    c_ix = len(self.color_list) - 1 - c_ix

                c = self.color_list[c_ix]

	    c.v = loud
            c = hsv_to_rgb(c.hsv)
            for i in self._list[i]:
                self.geometry.set_pixel(i, c)

        self.geometry.draw()


    

__shows__ = [
              (Areas.name, Areas)
            ]


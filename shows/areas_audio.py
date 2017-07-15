from color2 import hsv_to_rgb, RGB
import color
from randomcolor import random_color
import morph
import audio
from math import ceil 

import looping_show

class AreasAudio(looping_show.LoopingShow):

    name = "Areas Audio"

    def __init__(self, geometry):
        looping_show.LoopingShow.__init__(self, geometry)

        self.background = RGB(0,0,0)
        self.mode = 2

        self.round = 0
        self.duration = 0.05
        self.clear()

	self.audio = audio.Audio()

    def clear(self):
        c = hsv_to_rgb(self.background.hsv)
        for i in range(self.geometry.numLEDs):
            self.geometry.set_pixel(i, c)

        self.geometry.draw()

    def custom_range_value_changed(self, range):
        self.mode = self.cm.ranges[range]
        print "setting mode to", self.mode

    def update_at_progress(self, progress, new_loop, loop_instance):

	(loud, pitch, yy) = self.audio.audio_input()
        if not new_loop:
            return
        #pitch = yy[3]

        if self.mode == 0:
            self._list = self.geometry.HOR_RINGS_MIDDLE_OUT
        elif self.mode in (1, 2, 3):
            self._list = self.geometry.RINGS_AROUND

        to_light = int(pitch * len(self._list))

        if self.mode == 0:
            for i in range(0, len(self._list)):

                if i <= to_light:
                    c = color.hsv(pitch,1.0,loud)
                else:
                    c = self.background.hsv

                #print self._list
                # all around
                for k in self._list[i]:
                    self.geometry.set_pixel(k, c)

        elif self.mode ==1:
            #self.round += 1
            #self.round %= max(self.geometry.row)
            if pitch == 1.0: to_light = len(self._list) / 2
            print pitch, to_light
            for round, l in enumerate(self._list):
                #print yy[round % len(l)]
                for i, k in enumerate(l):
                    if i <= to_light/2:
                        # TBD: PICK a color from a decent palette!!
                        # Use tween?
                        c = color.hsv(abs(yy[round % len(l)]) / 1.1, 1.0, loud)
                    else:
                        c = (0,0,0)
                    self.geometry.set_pixel(k, c)

        elif self.mode == 2:

            # TBD: Maybe have some kind of a correction matrix for yy
            # basically correction = [0.5, 0.4, 0.5]
            # then yy = yy - correction 
            # code, see mapping in model

            if pitch == 1.0: pitch = 0.5

            for round, l in enumerate(self._list):
                to_light = (abs(yy[round % len(yy)]) / 2.5) * len(self._list)
                # print "r", round, round % len(yy), yy[round % len(yy)]
                for i, k in enumerate(l):
                    if i <= to_light:
                        c = color.rainbow_(1, round, loud)
                    else:
                        c = (0,0,0)
                    self.geometry.set_pixel(k, c)

        elif self.mode == 3:

            # from: http://yager.io/LEDStrip/LED.html
            # TBD
            pass




        self.geometry.draw()

__shows__ = [
              (AreasAudio.name, AreasAudio)
            ]


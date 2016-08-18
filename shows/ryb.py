#import geom
import color2

import random

import looping_show
import tween
from model import HOR_RINGS_TOP_DOWN, VERT_RINGS

class RYB(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "RYB"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.duration = 2 
        self.mode = 0           # 0 by default if nobody called update_parameters()
        self.range = HOR_RINGS_TOP_DOWN

        # Setup a unique offset for each bird
        self.offsets = []
        for thing in self.range:
            self.offsets.append(random.random())
            #self.offsets.append(0.01)

        #self.was_selected_randomly()

    def update_parameters(self, state):
        # mode: 0 = self.mode=0 and HOR_RINGS, 3 = self.mode=0 and VERT_RINGS
        self.mode = state % 3
        self.range = HOR_RINGS_TOP_DOWN
        r = "HOR_RINGS_TOP_DOWN"
        if state >= 3:
            self.range = VERT_RINGS
            r = "VERT_RINGS"
        print "running %s in mode %s, range %s" % (self.name, self.mode, r)

    def was_selected_randomly(self):
        # remember the mode it played already
        print "Updating show mode to %s" % self.mode
        #self.cm.set_modifier(3, (random.randrange(10) > 4))
        #self.cm.set_intensified((random.random() * 2.0) - 1.0)


    def update_at_progress(self, progress, new_loop, loop_instance):

        if self.mode == 0:
            # Color striped from top to bottom by slices
            v_range = tween.easeInQuad(0.1, 0.98, (self.cm.brightness + 1.0)/2.0)
            per_slice = v_range / len(self.range)

            for idx, sl in enumerate(self.range):
                hue = progress - (idx * per_slice) + self.offsets[0]
                while hue > 1.0:
                    hue -= 1.0
                while hue < 0.0:
                    hue += 1.0

                hsv = (hue, 1.0, 1.0)

                rgbTuple = color2.hsvRYB_to_rgb(hsv)
                rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

                for i in sl:
                    self.geometry.set_pixel(i, rgbTuple)

            self.geometry.draw()


        elif self.mode == 1:
            # Each bird gets a unique color based on it's offset
            for idx,bird in enumerate(self.range):
                hue = progress + self.offsets[idx]
                if hue > 1.0:
                    hue -= 1.0
                hsv = (hue, 1.0, 1.0)

                rgbTuple = color2.hsvRYB_to_rgb(hsv)
                rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

                for i in bird:
                    self.geometry.set_pixel(i, rgbTuple)

            self.geometry.draw()

        else:
            # Everything the same color
            hsv = (progress + self.offsets[0], 1.0, 1.0)

            rgbTuple = color2.hsvRYB_to_rgb(hsv)
            rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

            for i in range(self.geometry.get_nof_pixels()):
                self.geometry.set_pixel(i, rgbTuple)

            self.geometry.draw()

__shows__ = [
              (RYB.name, RYB)
            ]
 

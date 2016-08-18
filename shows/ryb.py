#import geom
import color2

import random

import looping_show
import tween
from model import HOR_RINGS_TOP_DOWN

class RYB(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "RYB"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.duration = 2
        self.mode = 0

        # Setup a unique offset for each bird
        self.offsets = []
        for thing in HOR_RINGS_TOP_DOWN:
            self.offsets.append(random.random())
            #self.offsets.append(0.01)

    '''
    def was_selected_randomly(self):
        self.cm.reset_step_modifiers(random.randrange(3))
        self.cm.set_modifier(3, (random.randrange(10) > 4))
        self.cm.set_intensified((random.random() * 2.0) - 1.0)

    '''

    def update_at_progress(self, progress, new_loop, loop_instance):

        if self.mode == 0:
            # Color striped from top to bottom by slices
            v_range = tween.easeInQuad(0.1, 0.98, (self.cm.brightness + 1.0)/2.0)
            per_slice = v_range / len(HOR_RINGS_TOP_DOWN)

            for idx, sl in enumerate(HOR_RINGS_TOP_DOWN):
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
            for idx,bird in enumerate(HOR_RINGS_TOP_DOWN):
                hue = progress + self.offsets[idx]
                if hue > 1.0:
                    hue -= 1.0
                hsv = (hue, 1.0, 1.0)

                rgbTuple = color2.hsvRYB_to_rgb(hsv)
                rgbTuple = (int(rgbTuple[0]*255), int(rgbTuple[1]*255), int(rgbTuple[2]*255))

                for i in bird:
                    self.geometry.set_pixel(i, rgbTuple)

            self.geometry.draw()

        else:
            # Everything the same color
            hsv = (progress + self.offsets[0], 1.0, 1.0)

            rgbTuple = color2.hsvRYB_to_rgb(hsv)
            rgbTuple = (int(rgbTuple[0]*255), int(rgbTuple[1]*255), int(rgbTuple[2]*255))

            for i in range(self.geometry.get_nof_pixels()):
                self.geometry.set_pixel(i, rgbTuple)

            self.geometry.draw()

__shows__ = [
              (RYB.name, RYB)
            ]
 

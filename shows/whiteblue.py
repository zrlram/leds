import color, color2

import random

import looping_show
import tween
import morph

class WhiteBlue(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "WhiteBlue"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND
        self.duration = 1.0
        self.direction = 0
        self.geometry.clear()


    def update_at_progress(self, progress, new_loop, loop_instance):

        bg = color.hsv(0.0, 0.0, 0.0)
        blue = color2.HSV(0.6,0.9,1.0)      # blue
        white = color2.HSV(0,0,1.0)   # white

        if new_loop:
            self.direction ^= 1

        if self.direction:
            white_pos = int(progress * len(self.range[0])) % len(self.range[0])
            if white_pos == 0: white_pos = 1
        else:
            white_pos = int((- progress) * len(self.range[0])) % len(self.range[0])
            if white_pos == 0: white_pos = 13

        # light up all the main meridians
        for four in range(4):
            meridian = int(four*len(self.range)/4)

            for idx, led in enumerate(self.range[meridian]):
                dist = abs(idx - white_pos)
                if dist <= 2:
                    col = white.copy()
                    col.v = 1 - (dist / 2) + 0.5
                    self.geometry.set_pixel(led, col.rgb)
                else:
                    self.geometry.set_pixel(led, blue.rgb)


        self.geometry.draw()

__shows__ = [
              (WhiteBlue.name, WhiteBlue)
            ]
 

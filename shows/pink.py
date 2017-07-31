import color2
import color

import random

import looping_show
import tween

class Pink(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Pink"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND

    def update_parameters(self, state):
        # mode: 0 = self.mode=0 and HOR_RINGS, 3 = self.mode=0 and VERT_RINGS

        self.mode = state % 2

        if self.mode == 1:
            self.duration = 8.0
            self.random_end_hue = random.random() 
        else:
            self.duration = 2.0

        print "running %s in mode %s at duration %s" % (self.name, self.mode, self.duration)

    def update_at_progress(self, progress, new_loop, loop_instance):


        if self.mode == 0:

            # Color striped from top to bottom by slices
            #v_range = tween.easeInQuad(0.0, 1.0, (self.cm.brightness + 1.0)/2.0)
            v_range = tween.easeInQuad(0.0, 1.0, 1.0)
            per_slice = v_range / len(self.range)

            for idx, sl in enumerate(self.range):
                hue = progress - (idx * per_slice) + 0.01
                while hue > 1.0:
                    hue -= 1.0
                while hue < 0.0:
                    hue += 1.0

                hsv = color.hsv(hue, 1.0, 1.0)

                for i in sl:
                    self.geometry.set_pixel(i, hsv)

        elif self.mode == 1:

            hue = (loop_instance / 10.0 + progress) % 1.0
            start = color2.HSV(hue,0.0,1.0)
            end = color2.HSV(self.random_end_hue,1.0,1.0)

            # Each ring gets a unique color based on it's offset
            for idx,ring in enumerate(self.range):

                l = idx/((len(self.range))/2.0) % 1.0
                if idx >= len(self.range)/2:       # over half
                    hsv = tween.hsvLinear(start, end, l)
                else:
                    hsv = tween.hsvLinear(end, start, l)
                
                rgbTuple = color2.hsv_to_rgb(hsv)
                rgbTuple = (int(rgbTuple[0]), int(rgbTuple[1]), int(rgbTuple[2]))

                index = (idx+int(progress*len(self.range))) % len(self.range)
                for i in self.range[index]:
                    self.geometry.set_pixel(i, rgbTuple)

        self.geometry.draw()

__shows__ = [
              (Pink.name, Pink)
            ]
 

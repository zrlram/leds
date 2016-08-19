import looping_show
from color2 import hsv_to_rgb
from randomcolor import random_color
import morph
from model import VERT_RINGS, HOR_RINGS_TOP_DOWN 

class EgPanels(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Eg Panels"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.foreground = random_color(luminosity="light")
        self.background = self.foreground.copy()
        self.background.h += 0.5
        self.background.s += 0.5
        self.mode = 0           

    def clear(self):
        c = hsv_to_rgb(self.background.hsv)
        for i in range(self.geometry.get_nof_pixels()):
            self.geometry.set_pixel(i, c)

        self.geometry.draw()

    def update_at_progress(self, progress, new_loop, loop_instance):

        if new_loop:
            #if self.mode==0:
            self.foreground = random_color(luminosity="light")
            self.background = self.foreground.copy()
            self.background.h += 0.5
            self.background.s += 0.2
            '''
            else:
                # TBD
                self.background = self.cm.chosen_colors[1]
                self.foreground = self.cm.chosen_colors[0]
            '''

            self.color_list = morph.transition_list(self.foreground, self.background, steps=16)
            self.clear()


        #mode = self.step_mode(5)

        if self.mode == 1:
            _list = HOR_RINGS_TOP_DOWN
        elif self.mode == 0:
            _list = VERT_RINGS

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
                if (loop_instance % 2 == 0):
                   c_ix = len(self.color_list) - 1 - c_ix

                c = self.color_list[c_ix]

            el = _list[i]

            c = hsv_to_rgb(c.hsv)
            for i in el:
                self.geometry.set_pixel(i, c)

        self.geometry.draw()

__shows__ = [
              (EgPanels.name, EgPanels)
            ]

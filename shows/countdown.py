import color

import random
from math import sqrt

import looping_shader_show
import tween
from font import font

class CountDown(looping_shader_show.LoopingShaderShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "CountDown"

    def empty_shader(self,p):
        #return (0,0,0)
        pass

    def explosion_shader(self,p):

        z = p[2]
        y = p[1]

        #dist = sqrt(z**2 + y**2)
        dist_z = abs(z - self.dz)  
        #print dist_z

        #if z < self.dz:

        color_hsv = color.rgb_to_hsv(self.color)  # set the intesity to the distance
        #dist_z = dist_z / self.trail % 1.0

        return color.hsv (color_hsv[0], color_hsv[1], max(0.0,min(self.dz,1.0)))
            

    def __init__(self, geometry):
        looping_shader_show.LoopingShaderShow.__init__(self, geometry, self.empty_shader)
        self.range = self.geometry.RINGS_AROUND
        self.duration = 1.0
        self.trail = 1.7
        self.color = (125,00,05)
        self.bright = 0

    def digit(self,digit):

        over = 1
        dots = []

        char = ord(digit) 
        for height in range(5):
            character = font[char*5+height] 
            #print ord(digit), character

            byte = character & 0xff
            # a column in a character
            for bit in reversed(range(1,6)):
                      
                if byte & 1 == 1:
                    up = bit + 1
                    if up <= 0:             # SORRY - 0 does not exist
                        up = up -1
                    # print up, over
                    dots.append((over,up))
                            
                byte = byte >> 1
            over = over + 1

        return dots
                        

    def update_at_progress(self, progress, new_loop, loop_instance):

        fg = color.hsv(0.0, 1.0, 1.0)

        if loop_instance<9 and new_loop:
            self.geometry.clear()
            path = self.digit(str(9-(loop_instance % 10)))
            for mirror in range(1,5):
                for dot in path:
                    start = mirror * len(self.range) / 4
                    (x,y) = dot
                    y = y + 2
                    # x = x + loop_instance
                    new_x = (start + x) % len(self.range)
                    led = self.range[new_x][y]
                    self.geometry.set_pixel(led, fg)

            self.geometry.draw()

        if loop_instance == 9:

            self.bright = self.bright or self.geometry.get_brightness()     # only remember it once
            new_bright = min(self.bright+progress*6, 1.0)
            self.geometry.set_brightness(new_bright)

            self.color = color.set_V(self.color, absolute = min(0.7+progress,1.0))
            self.color = color.set_S(self.color, absolute = min(0.6+progress,1.0))

            # explode
            if progress <= 0.3:
                self.geometry.shaders = [self.explosion_shader]
                self.dz = (- 1.0 + progress * 10)
            else:
                self.geometry.shaders = []

            # move on to next show
            if progress > 0.3:
                self.geometry.clear()

        if loop_instance == 12:
            # reset brightness
            self.geometry.set_brightness(self.bright)
            self.cm.show_runner.next_show()



            '''if progress > 0.25 and not self.done:
                for led in range(0, self.geometry.numLEDs, 2):
                    # the shader color is kept less bright due to the global brightness setting
                    # let's just set it manually
                    self.geometry.set_pixel(led, (200, 200, 200))

                self.geometry.draw()
                self.done = 1
                '''

        # go to next show

__shows__ = [
              (CountDown.name, CountDown)
            ]
 

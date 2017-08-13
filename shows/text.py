import color

import random

import looping_show
import tween
from font import font

class Text(looping_show.LoopingShow):
    # Because we extend LoopingShow we must explicitly override is_show to be True
    is_show = True
    
    name = "Text"

    def __init__(self, sheep_sides):
        looping_show.LoopingShow.__init__(self, sheep_sides)
        self.range = self.geometry.RINGS_AROUND
        self.width = 0

        self.duration = 1.0
        self.text = "HELLO RAFFY"

        self.geometry.clear()

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
                        
    def rotate(self, how_much, drop_end = True):

        # read all - make a quick copy to not change in place
        pixels = []
        for idx in range(self.geometry.get_nof_pixels()):
            temp = self.geometry.pixels[idx]
            pixels.append((temp[0], temp[1],temp[2]))

        bright = self.geometry.get_brightness()
        self.geometry.set_brightness(1.0)

        korrektur = 0
        if drop_end:
            korrektur = drop_end
        for x in range(len(self.range) - korrektur):
            for y in range(14):
                try:
                    # read current value
                    led = self.range[x][y]
                    col = pixels[led]
                    # rotate x by 'how_much'
                    new_x = (x-how_much) % len(self.range)
                
                    led = self.range[new_x][y]
                    #print str(col)
                    self.geometry.set_pixel(led, col)

                except Exception as ex:
                    #import traceback
                    #traceback.print_exc()
                    continue

            self.geometry.draw()

        self.geometry.set_brightness(bright)

    def update_at_progress(self, progress, new_loop, loop_instance):

        fg_bright = color.hsv(0.1, 0.5, 1.0)
        fg = color.hsv(0.2, 0.4, 1.0)
        bg = color.hsv(0.0, 0.0, 0.0)

        if new_loop:
            #self.geometry.clear()
            #path = self.digit(str(loop_instance % 10))
            letter = loop_instance%len(self.text)
            path = self.digit(self.text[letter])

            self.rotate(self.width)

            if self.text[letter] == " ":
                self.width = 2      # for space
            else:
                self.width = max([x for (x,y) in path]) + 1

            # clear letter area
            start = len(self.range) 
            for x in range(1, self.width+1):
                for y in range(1, 7):
                    led = self.range[x][y+2]
                    self.geometry.set_pixel(led,bg)

            for (x,y) in path:
                led = self.range[x][y+2]
                self.geometry.set_pixel(led, fg)


            self.geometry.draw()

__shows__ = [
              (Text.name, Text)
            ]
 
